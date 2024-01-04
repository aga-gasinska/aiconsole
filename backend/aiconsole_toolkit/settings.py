import asyncio
from pathlib import Path
from typing import Any
from aiconsole.core.settings.models import PartialSettingsData
from aiconsole.core.settings.observer import FileObserver

from aiconsole.core.settings.project_settings import Settings
from aiconsole.core.settings.storage import SettingsFileStorage


def set_code_autorun(autorun: bool) -> None:
    SettingsFileStorage().configure(project_path=Path("."))
    Settings().configure(storage=SettingsFileStorage())
    Settings().storage.save(PartialSettingsData(code_autorun=autorun))


def get_settings() -> dict[str, Any]:
    asyncio.run(Settings().reload())
    return Settings().settings_data.model_dump()
