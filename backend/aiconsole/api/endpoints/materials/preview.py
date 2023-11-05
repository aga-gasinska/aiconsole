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
    
from datetime import datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from aiconsole.agents.types import Agent
from aiconsole.chat.types import Chat
from aiconsole.execution_modes.normal import execution_mode_normal
from aiconsole.gpt.consts import GPTMode
from aiconsole.materials.content_evaluation_context import ContentEvaluationContext
from aiconsole.materials.material import Material

router = APIRouter()

@router.post("/preview")
async def materials_preview(material: Material):
    content_context = ContentEvaluationContext(
        chat=Chat(id="chat", title="", last_modified=datetime.now(), title_edited=False, message_groups=[]),
        agent=Agent(
            id="user",
            name="User",
            usage="",
            system="",
            execution_mode=execution_mode_normal,
            gpt_mode=GPTMode.QUALITY,
        ),
        gpt_mode=GPTMode.FAST,
        relevant_materials=[],
    )

    rendered_material = await material.render(content_context)

    return JSONResponse(rendered_material.model_dump())