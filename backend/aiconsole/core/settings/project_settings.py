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
from functools import lru_cache

from aiconsole.core.settings import models
from aiconsole.core.settings.base.storage import SettingsStorage

_log = logging.getLogger(__name__)


class SettingsNotConfiguredException(Exception):
    """Missing configuration of the settings. Call .configure() method."""


class Settings:
    def configure(self, storage: SettingsStorage):
        self.settings_data = models.SettingsData()
        self.storage = storage
        self._suppress_notification_until: datetime.datetime | None = None

    async def reload(self):
        if not self.storage:
            _log.exception(f"[{self.__class__.__name__}] Reload was called before configuration.")
            raise SettingsNotConfiguredException

        self.settings_data = self.storage.load()

        await self._notify()

    async def _notify(self):
        from aiconsole.api.websockets.server_messages import SettingsServerMessage

        await SettingsServerMessage(
            initial=False
            or not self._suppress_notification_until
            or self._suppress_notification_until < datetime.datetime.now()
        ).send_to_all()

        self._suppress_notification_until = None


@lru_cache
def settings() -> Settings:
    return Settings()
