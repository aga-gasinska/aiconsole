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

import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from aiconsole.api.websockets import connection_manager
from aiconsole.api.websockets.incoming_message_handler import incoming_message_handler
from aiconsole.api.websockets.server_messages import (
    DebugJSONServerMessage,
    ErrorServerMessage,
)
from aiconsole.core.chat.locking import chats
from aiconsole.core.project import project

router = APIRouter()

_log = logging.getLogger(__name__)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    connection = await connection_manager.connect(websocket)
    await project.send_project_init(connection)

    try:
        while True:
            _log.debug("Waiting for message")
            json_data = await websocket.receive_json()
            _log.debug(f"Received message: {json_data}")
            try:
                await incoming_message_handler.handle(connection, json_data)
            except Exception as e:
                await ErrorServerMessage(
                    error=f"Error handling message: {e} type={e.__class__.__name__}"
                ).send_to_connection(connection)
                _log.exception(e)
                _log.error(f"Error handling message: {e}")
    except WebSocketDisconnect:
        connection_manager.disconnect(connection)
