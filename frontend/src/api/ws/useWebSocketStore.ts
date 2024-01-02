// The AIConsole Project
//
// Copyright 2023 10Clouds
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import ReconnectingWebSocket from 'reconnecting-websocket';
import { create } from 'zustand';
import { ErrorEvent } from 'reconnecting-websocket/events';
import { useChatStore } from '../../store/editables/chat/useChatStore';
import { useAPIStore } from '../../store/useAPIStore';
import { ClientMessage } from './clientMessages';
import { ServerMessage } from './serverMessages';
import { handleServerMessage } from './handleServerMessage';

export type WebSockeStore = {
  ws: ReconnectingWebSocket | null;
  initWebSocket: () => void;
  disconnect: () => void;
  sendMessage: (message: ClientMessage) => void;
  initStarted: boolean;
};

// Create Zustand store
export const useWebSocketStore = create<WebSockeStore>((set, get) => ({
  ws: null,
  initStarted: false,

  // updated function to init the WebSocket connection
  initWebSocket: () => {
    if (get().initStarted) return;
    set({ initStarted: true });

    const getBaseHostWithPort = useAPIStore.getState().getBaseHostWithPort;
    const ws = new ReconnectingWebSocket(`ws://${getBaseHostWithPort()}/ws`);

    ws.onopen = () => {
      set({ ws });

      const chatId = useChatStore.getState().chat?.id || '';

      get().sendMessage({
        type: 'OpenChatClientMessage',
        chat_id: chatId,
      });
    };

    ws.onmessage = async (e: MessageEvent) => {
      const data: ServerMessage = JSON.parse(e.data);
      handleServerMessage(data);
    };

    ws.onerror = (e: ErrorEvent) => {
      console.log('WebSocket error: ', e);
    };

    ws.onclose = () => {
      console.log('WebSocket connection closed');
      set({ ws: null });
    };
  },

  disconnect: () => {
    get().ws?.close();
    set({ ws: null });
  },

  sendMessage: (message: ClientMessage) => {
    get().ws?.send(JSON.stringify(message));
  },
}));
