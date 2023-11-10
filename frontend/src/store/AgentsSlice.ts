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

import { StateCreator } from 'zustand';

import { Agent } from '../types/types';
import { Api } from '@/api/Api';
import { AICStore } from './AICStore';

export type AgentsSlice = {
  agents: Agent[];
  initAgents: () => Promise<void>;
  getAgent: (id: string) => Agent | undefined;
};

export const createAgentsSlice: StateCreator<AICStore, [], [], AgentsSlice> = (
  set,
  get,
) => ({
  agents: [],
  initAgents: async () => {
    set({ agents: [] });
    if (!get().isProjectOpen()) return;
    const agents = await Api.getAgents();
    set(() => ({
      agents: agents,
    }));
  },
  getAgent: (id: string) => {
    return get().agents.find((agent) => agent.id === id);
  },
});
