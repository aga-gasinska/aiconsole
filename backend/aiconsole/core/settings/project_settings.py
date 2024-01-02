# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
import logging
import tomlkit
import litellm
from pathlib import Path
from appdirs import user_config_dir

from pydantic import BaseModel, EmailStr, validator

from watchdog.observers import Observer
from aiconsole.utils.BatchingWatchDogHandler import BatchingWatchDogHandler

from aiconsole.core.project import project
from aiconsole.core.project.paths import get_project_directory
from aiconsole.api.websockets.outgoing_messages import SettingsWSMessage
from aiconsole.core.assets.asset import AssetStatus, AssetType
from aiconsole.utils.recursive_merge import recursive_merge


_log = logging.getLogger(__name__)


class PartialSettingsData(BaseModel):
    code_autorun: bool | None = None
    openai_api_key: str | None = None
    user_profile_settings: "UserProfileSettingsData | None" = None
    materials: dict[str, AssetStatus] = {}
    materials_to_reset: list[str] = []
    agents: dict[str, AssetStatus] = {}
    agents_to_reset: list[str] = []
    to_global: bool = False


class UserProfileSettingsData(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    avatar_path: str | None = None
    gravatar: bool = False


class SettingsData(BaseModel):
    code_autorun: bool = False
    openai_api_key: str | None = None
    user_profile_settings: UserProfileSettingsData = UserProfileSettingsData()
    materials: dict[str, AssetStatus] = {}
    agents: dict[str, AssetStatus] = {}

    @validator("user_profile", pre=True, always=True)
    def create_user_profile_default(cls, v):
        return v or UserProfileSettingsData()


def _set_openai_api_key_environment(settings: SettingsData) -> None:
    litellm.openai_key = settings.openai_api_key or "invalid key"


class Settings:
    def __init__(self, project_path: Path | None = None):
        self.settings_data: SettingsData = SettingsData()
        self._global_settings_file_path: Path = Path(user_config_dir("aiconsole")) / "settings.toml"
        self._project_settings_file_path: Path | None = project_path / "settings.toml" if project_path else None
        self._observer = Observer()

        self._setup_observer(self._global_settings_file_path)
        if self._project_settings_file_path:
            self._setup_observer(self._project_settings_file_path)

        self._observer.start()

    async def reload(self, initial: bool = False):
        self._settings = await self.__load()
        await SettingsWSMessage(
            initial=initial
            or not self._suppress_notification_until
            or self._suppress_notification_until < datetime.datetime.now()
        ).send_to_all()
        self._suppress_notification_until = None

    def _setup_observer(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self._observer.schedule(
            BatchingWatchDogHandler(self.reload, path.name),
            str(path.parent),
            recursive=False,
        )

    def stop(self):
        self._observer.stop()

    def get_asset_status(self, asset_type: AssetType, id: str) -> AssetStatus:
        s = self._settings

        if asset_type == AssetType.MATERIAL:
            if id in s.materials:
                return s.materials[id]
            asset = project.get_project_materials().get_asset(id)
            default_status = asset.default_status if asset else AssetStatus.ENABLED
            return default_status
        elif asset_type == AssetType.AGENT:
            if id in s.agents:
                return s.agents[id]
            asset = project.get_project_agents().get_asset(id)
            default_status = asset.default_status if asset else AssetStatus.ENABLED
            return default_status

        else:
            raise ValueError(f"Unknown asset type {asset_type}")

    def set_asset_status(self, asset_type: AssetType, id: str, status: AssetStatus, to_global: bool = False) -> None:
        if asset_type == AssetType.MATERIAL:
            self.save(PartialSettingsData(materials={id: status}), to_global=to_global)
        elif asset_type == AssetType.AGENT:
            self.save(PartialSettingsData(agents={id: status}), to_global=to_global)
        else:
            raise ValueError(f"Unknown asset type {asset_type}")

    def rename_asset(self, asset_type: AssetType, old_id: str, new_id: str):
        if asset_type == AssetType.MATERIAL:
            partial_settings = PartialSettingsData(
                materials_to_reset=[old_id], materials={new_id: self.get_asset_status(asset_type, old_id)}
            )
        elif asset_type == AssetType.AGENT:
            partial_settings = PartialSettingsData(
                agents_to_reset=[old_id], agents={new_id: self.get_asset_status(asset_type, old_id)}
            )
        else:
            raise ValueError(f"Unknown asset type {asset_type}")

        self.save(partial_settings, to_global=True)

    async def __load(self) -> SettingsData:
        settings = {}
        for file_path in [self._global_settings_file_path, self._project_settings_file_path]:
            if file_path and file_path.exists():
                settings = recursive_merge(settings, self._load_from_path(file_path))

        settings_data = SettingsData(
            **{key: settings.get(key, getattr(SettingsData(), key)) for key in SettingsData.model_fields.keys()}
        )

        self.enforce_single_forced_agent(settings_data)
        _set_openai_api_key_environment(settings_data)

        _log.info("Loaded settings")
        return settings_data

    @staticmethod
    def enforce_single_forced_agent(settings_data: SettingsData):
        forced_agents = [agent for agent, status in settings_data.agents if status == AssetStatus.FORCED]

        if len(forced_agents) > 1:
            _log.warning(f"More than one agent is forced: {forced_agents}")
            for agent in forced_agents[1:]:
                settings_data.agents[agent] = AssetStatus.ENABLED

    @staticmethod
    def _load_from_path(file_path: Path) -> dict:
        with file_path.open() as file:
            document = tomlkit.loads(file.read())
        return dict(document)

    @staticmethod
    def _get_document(file_path: Path) -> tomlkit.TOMLDocument:
        if not file_path.exists():
            return tomlkit.document()

        with file_path.open() as file:
            return tomlkit.loads(file.read())

    @staticmethod
    def _update_document(document: tomlkit.TOMLDocument, settings_data: PartialSettingsData):
        for key in settings_data.model_dump(exclude_none=True):
            document[key] = getattr(settings_data, key)

    @staticmethod
    def _write_document(file_path: Path, document: tomlkit.TOMLDocument):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w") as file:
            file.write(document.as_string())

    def save(self, settings_data: PartialSettingsData, to_global: bool = False) -> None:
        file_path = self._global_settings_file_path if to_global else self._project_settings_file_path
        if not file_path:
            raise ValueError("Cannot save settings, path not specified")

        document = self._get_document(file_path)
        self._update_document(document, settings_data)
        self._write_document(file_path, document)
        self._suppress_notification_until = datetime.datetime.now() + datetime.timedelta(seconds=30)
        
        # TODO: disscuss forced agent logic of savings
        # TODO: disscuss logic of suppresing messages


async def init():
    # TODO: Remove global usage
    global _settings
    _settings = Settings(get_project_directory() if project.is_project_initialized() else None)
    await _settings.reload()


def get_aiconsole_settings() -> Settings:
    return _settings


async def reload_settings(initial: bool = False):
    global _settings
    _settings.stop()
    _settings = Settings(get_project_directory() if project.is_project_initialized() else None)
    await _settings.reload(initial)
