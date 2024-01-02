from typing import Union

from aiconsole.core.code_running.code_interpreters.language import LanguageStr
from aiconsole.core.gpt.types import GPTRole
from pydantic import BaseModel


class LockAcquiredMutation(BaseModel):
    pass


class LockReleasedMutation(BaseModel):
    aborted: bool


class CreateMessageGroupMutation(BaseModel):
    message_group_id: str
    agent_id: str
    username: str
    email: str
    role: GPTRole
    task: str
    materials_ids: list[str]
    analysis: str


class DeleteMessageGroupMutation(BaseModel):
    message_group_id: str


class SetIsAnalysisInProgressMutation(BaseModel):
    is_analysis_in_progress: bool


class SetTaskMessageGroupMutation(BaseModel):
    message_group_id: str
    task: str


class AppendToTaskMessageGroupMutation(BaseModel):
    message_group_id: str
    task_delta: str


class SetRoleMessageGroupMutation(BaseModel):
    message_group_id: str
    role: GPTRole


class SetAgentIdMessageGroupMutation(BaseModel):
    message_group_id: str
    agent_id: str


class SetMaterialsIdsMessageGroupMutation(BaseModel):
    message_group_id: str
    materials_ids: list[str]


class AppendToMaterialsIdsMessageGroupMutation(BaseModel):
    message_group_id: str
    material_id: str


class SetAnalysisMessageGroupMutation(BaseModel):
    message_group_id: str
    analysis: str


class AppendToAnalysisMessageGroupMutation(BaseModel):
    message_group_id: str
    analysis_delta: str


# Continuation of Mutation Classes


class CreateMessageMutation(BaseModel):
    message_group_id: str
    message_id: str
    timestamp: str
    content: str


class DeleteMessageMutation(BaseModel):
    message_id: str


class AppendToContentMessageMutation(BaseModel):
    message_id: str
    content_delta: str


class SetContentMessageMutation(BaseModel):
    message_id: str
    content: str


class SetIsStreamingMessageMutation(BaseModel):
    message_id: str
    is_streaming: bool


class CreateToolCallMutation(BaseModel):
    message_id: str
    tool_call_id: str
    code: str
    language: LanguageStr | None
    headline: str
    output: str | None


class DeleteToolCallMutation(BaseModel):
    tool_call_id: str


class SetHeadlineToolCallMutation(BaseModel):
    tool_call_id: str
    headline: str


class AppendToHeadlineToolCallMutation(BaseModel):
    tool_call_id: str
    headline_delta: str


class SetCodeToolCallMutation(BaseModel):
    tool_call_id: str
    code: str


class AppendToCodeToolCallMutation(BaseModel):
    tool_call_id: str
    code_delta: str


class SetLanguageToolCallMutation(BaseModel):
    tool_call_id: str
    language: LanguageStr


class SetOutputToolCallMutation(BaseModel):
    tool_call_id: str
    output: str | None


class AppendToOutputToolCallMutation(BaseModel):
    tool_call_id: str
    output_delta: str


class SetIsStreamingToolCallMutation(BaseModel):
    tool_call_id: str
    is_streaming: bool


class SetIsExecutingToolCallMutation(BaseModel):
    tool_call_id: str
    is_executing: bool


ChatMutation = (
    LockAcquiredMutation
    | LockReleasedMutation
    | CreateMessageGroupMutation
    | DeleteMessageGroupMutation
    | SetIsAnalysisInProgressMutation
    | SetTaskMessageGroupMutation
    | AppendToTaskMessageGroupMutation
    | SetRoleMessageGroupMutation
    | SetAgentIdMessageGroupMutation
    | SetMaterialsIdsMessageGroupMutation
    | AppendToMaterialsIdsMessageGroupMutation
    | SetAnalysisMessageGroupMutation
    | AppendToAnalysisMessageGroupMutation
    | CreateMessageMutation
    | DeleteMessageMutation
    | AppendToContentMessageMutation
    | SetContentMessageMutation
    | SetIsStreamingMessageMutation
    | CreateToolCallMutation
    | DeleteToolCallMutation
    | SetHeadlineToolCallMutation
    | AppendToHeadlineToolCallMutation
    | SetCodeToolCallMutation
    | AppendToCodeToolCallMutation
    | SetLanguageToolCallMutation
    | SetOutputToolCallMutation
    | AppendToOutputToolCallMutation
    | SetIsStreamingToolCallMutation
    | SetIsExecutingToolCallMutation
)
