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
from aiconsole.core.assets.asset import EditableObject

from aiconsole.core.code_running.code_interpreters.language_map import LanguageStr
from aiconsole.core.gpt.types import GPTRole
from aiconsole.core.settings.project_settings import get_aiconsole_settings
from pydantic import BaseModel, Field, model_validator


class AICToolCall(BaseModel):
    id: str
    language: LanguageStr
    code: str
    headline: str
    output: str | None = None


class AICMessage(BaseModel):
    id: str
    timestamp: str
    content: str
    tool_calls: list[AICToolCall]


class AICMessageGroup(BaseModel):
    id: str
    agent_id: str
    username: str | None = None
    email: str | None = None
    role: GPTRole
    task: str
    materials_ids: list[str]
    messages: list[AICMessage]

    @model_validator(mode="after")
    def set_default_username(self):
        role = self.role
        if role == "user":
            self.username = self.username or get_aiconsole_settings().get_username()
        return self

    @model_validator(mode="after")
    def set_default_email(self):
        role = self.role
        if role == "user":
            self.email = self.email or get_aiconsole_settings().get_email()
        return self


class ChatHeadline(EditableObject):
    last_modified: datetime

    def model_dump(self, **kwargs):
        return {
            **super().model_dump(**kwargs),
            "last_modified": self.last_modified.isoformat(),
        }


class Chat(ChatHeadline):
    title_edited: bool = False
    message_groups: list[AICMessageGroup]


class Command(BaseModel):
    command: str


class ChatHeadlines(BaseModel):
    headlines: list[ChatHeadline]
