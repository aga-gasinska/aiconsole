from typing import Protocol

from aiconsole.core.chat.chat_mutations import ChatMutation
from aiconsole.core.chat.types import Chat


class ChatMutator(Protocol):
    chat: Chat

    async def mutate(self, mutation: ChatMutation) -> None:
        ...
