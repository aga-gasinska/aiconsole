from pydantic import BaseModel, EmailStr, Field

from aiconsole.core.assets.models import AssetStatus


class UserProfileSettingsData(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    avatar_path: str | None = None
    gravatar: bool = False


class PartialSettingsData(BaseModel):
    code_autorun: bool | None = None
    openai_api_key: str | None = None
    user_profile_settings: UserProfileSettingsData | None = None
    materials: dict[str, AssetStatus] = {}
    materials_to_reset: list[str] = []
    agents: dict[str, AssetStatus] = {}
    agents_to_reset: list[str] = []
    to_global: bool = False


class SettingsData(BaseModel):
    code_autorun: bool = False
    openai_api_key: str | None = None
    user_profile: UserProfileSettingsData = Field(default_factory=lambda: UserProfileSettingsData())
    materials: dict[str, AssetStatus] = {}
    agents: dict[str, AssetStatus] = {}
