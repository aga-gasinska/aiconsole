from aiconsole.core.assets.models import AssetStatus
from pydantic import BaseModel


class StatusChangePostBody(BaseModel):
    status: AssetStatus
    to_global: bool
