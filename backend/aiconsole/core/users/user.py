import hashlib
from functools import lru_cache
from pathlib import Path

from aiconsole.consts import AICONSOLE_USER_CONFIG_DIR
from aiconsole.core.clients.gravatar import GravatarUserProfile, gravatar_client
from aiconsole.core.settings.models import PartialSettingsData
from aiconsole.core.settings.project_settings import settings
from aiconsole.core.users.models import DEFAULT_USERNAME, UserProfile
from aiconsole.utils.resource_to_path import resource_to_path

DEFAULT_AVATARS_PATH = "aiconsole.preinstalled.avatars"


class UserProfileService:
    def get_profile(self, email: str | None = None) -> UserProfile:
        if email:
            gravatar_profile = gravatar_client().get_profile(email)
            if gravatar_profile:
                return self._create_user_profile_from_gravatar(email, gravatar_profile)

        return UserProfile(
            username=email or DEFAULT_USERNAME,
            email=email,
            avatar_url=self._get_default_avatar(email) if email else self._get_default_avatar(),
            gravatar=False,
        )

    def save_avatar(self, file_path: Path) -> None:
        settings().storage.save(
            PartialSettingsData(
                user_profile_settings=UserProfile(avatar_url=f"profile_image?img_filename={file_path.name}"),
                to_global=True,
            ),
        )

    def get_avatar(self, img_filename: str) -> Path:
        return AICONSOLE_USER_CONFIG_DIR() / "avatars" / img_filename

    @staticmethod
    def get_profile_image_path(img_filename: str) -> Path:
        return resource_to_path(DEFAULT_AVATARS_PATH) / img_filename

    def _get_default_avatar(self, email: str | None = None) -> str:
        key = email or settings().settings_data.openai_api_key or "some_key"
        img_filename = self._deterministic_choice(
            blob=key, choices=list(resource_to_path(resource=DEFAULT_AVATARS_PATH).glob(pattern="*"))
        ).name
        return f"profile_image?img_filename={img_filename}"

    def _create_user_profile_from_gravatar(self, email: str, gravatar_profile: GravatarUserProfile) -> UserProfile:
        return UserProfile(
            username=gravatar_profile.preferredUsername,
            email=email,
            avatar_url=gravatar_profile.thumbnailUrl,
            gravatar=True,
        )

    def _deterministic_choice(self, blob: str, choices: list[Path]) -> Path:
        hash_value = hashlib.sha256(string=blob.encode()).hexdigest()
        choice_index = int(hash_value, base=16) % len(choices)
        return choices[choice_index]


@lru_cache
def user_profile_service() -> UserProfileService:
    return UserProfileService()
