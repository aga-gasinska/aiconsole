from collections import defaultdict
from typing import Dict
import asyncio
from aiconsole.api.websockets.connection_manager import AICConnection
from aiconsole.api.websockets.server_messages import (
    LockAcquiredServerMessage,
    LockReleasedServerMessage,
    NotifyAboutChatMutationServerMessage,
)
from aiconsole.core.chat.apply_mutation import apply_mutation
from aiconsole.core.chat.chat_mutations import ChatMutation
from aiconsole.core.chat.chat_mutator import ChatMutator
from aiconsole.core.chat.load_chat_history import load_chat_history
from aiconsole.core.chat.save_chat_history import save_chat_history
from aiconsole.core.chat.types import Chat
from fastapi import HTTPException

chats: Dict[str, Chat] = {}
locks: Dict[str, str] = {}
lock_events: Dict[str, asyncio.Event] = defaultdict(asyncio.Event)

lock_timeout = 30  # Time in seconds to wait for the lock


async def wait_for_lock(chat_id: str) -> None:
    try:
        await asyncio.wait_for(lock_events[chat_id].wait(), timeout=lock_timeout)
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Lock acquisition timed out")


async def acquire_lock(chat_id: str, request_id: str):
    if chat_id in locks:
        await wait_for_lock(chat_id)

    chat_history = await load_chat_history(chat_id)
    locks[chat_id] = request_id
    chats[chat_id] = chat_history
    lock_events[chat_id].clear()

    await LockAcquiredServerMessage(request_id=request_id, chat_id=chat_id).send_to_chat(chat_id)

    return chat_history


async def release_lock(chat_id: str, request_id: str) -> None:
    if chat_id in locks and locks[chat_id] == request_id:
        save_chat_history(chats[chat_id])
        del locks[chat_id]
        del chats[chat_id]
        lock_events[chat_id].set()

        await LockReleasedServerMessage(request_id=request_id, chat_id=chat_id, aborted=False).send_to_chat(chat_id)


class DefaultChatMutator(ChatMutator):
    def __init__(self, chat_id: str, request_id: str, connection: AICConnection | None):
        self.chat_id = chat_id
        self.request_id = request_id
        self.connection = connection

    @property
    def chat(self) -> Chat:
        return chats[self.chat_id]

    async def mutate(self, mutation: ChatMutation) -> None:
        if self.chat_id not in locks or locks[self.chat_id] != self.request_id:
            raise HTTPException(status_code=403, detail="Access denied or chat is not locked")

        apply_mutation(self.chat, mutation)

        # when a server receives a mutation it should send it out to every connection except the one it came from
        await NotifyAboutChatMutationServerMessage(
            request_id=self.request_id,
            chat_id=self.chat_id,
            mutation=mutation,
        ).send_to_chat(self.chat_id, self.connection)
