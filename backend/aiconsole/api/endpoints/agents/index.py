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

from aiconsole.core.assets.models import AssetType
from aiconsole.core.project import project
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def agents_get():
    return JSONResponse(
        [
            *(
                {
                    **agent.model_dump(),
                    "status": project.get_project_agents().get_status(AssetType.AGENT, agent.id),
                }
                for agent in project.get_project_agents().all_assets()
            )
        ]
    )
