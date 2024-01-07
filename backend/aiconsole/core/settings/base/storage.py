import logging
from abc import ABC, abstractmethod

import litellm
from deepmerge import Merger

from aiconsole.core.settings import models

_log = logging.getLogger(__name__)


class SettingsStorage(ABC):
    @property
    @abstractmethod
    def global_settings(self) -> dict:
        ...

    @property
    @abstractmethod
    def project_settings(self) -> dict:
        ...

    def load(self) -> models.SettingsData:
        settings = self.merge_settings()

        settings_data = models.SettingsData(
            **{
                key: settings.get(key, getattr(models.SettingsData(), key))
                for key in models.SettingsData.model_fields.keys()
            }
        )

        litellm.openai_key = settings_data.openai_api_key or "invalid key"

        _log.info("Loaded settings")
        return settings_data

    @abstractmethod
    def save(self, settings_data: models.PartialSettingsData, to_global: bool = False):
        ...

    def merge_settings(self) -> dict:
        """Recursively merge dictionaries using deepmerge."""

        dict_strategy = Merger(
            [
                (dict, ["merge"]),
                (list, ["append"]),
            ],
            # fallback strategies,
            # applied to all other types:
            ["override"],
            # conflict resolution strategies
            ["override"],
        )
        return dict_strategy.merge(self.global_settings, self.project_settings)
