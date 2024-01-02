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

import { useEffect, useState } from 'react';
import { ChevronDown, ChevronUp, X } from 'lucide-react';
import { useDebounceCallback } from '@mantine/hooks';
import { Content, DropdownMenu, Item, Trigger } from '@radix-ui/react-dropdown-menu';

import { Icon } from '@/components/common/icons/Icon';
import Checkbox from '@/components/common/Checkbox';
import { useChatStore } from '@/store/editables/chat/useChatStore';
import { useEditablesStore } from '@/store/editables/useEditablesStore';
import { Agent, Material } from '@/types/editables/assetTypes';
import { cn } from '@/utils/common/cn';
import { getEditableObjectIcon } from '@/utils/editables/getEditableObjectIcon';

import { AgentAvatar } from '../chat/AgentAvatar';
import Autocomplete from './Autocomplete';

const ChatOptions = () => {
  const chat = useChatStore((state) => state.chat);
  const agents = useEditablesStore((state) => state.agents);
  const materials = useEditablesStore((state) => state.materials);

  const [materialsOptions, setMaterialsOptions] = useState<Material[]>([]);
  const [selectedAgentId, setSelectedAgentId] = useState<string>('aiChoice');
  const [chosenMaterials, setChosenMaterials] = useState<Material[]>([]);
  const [allowExtraMaterials, setAllowExtraMaterials] = useState<boolean>(false);

  useEffect(() => {
    // TODO: set options from chat
    console.log(chat);
  }, [chat]);

  const debounceChatUpdate = useDebounceCallback(() => {
    // TODO: send data to backend
    console.log(`Chat ${chat?.id} options updated`);
    console.log('chosenMaterials', chosenMaterials);
    console.log('selectedAgentId', selectedAgentId);
    console.log('allowExtraMaterials', allowExtraMaterials);
  }, 500);

  useEffect(() => {
    debounceChatUpdate();
  }, [chosenMaterials, selectedAgentId, allowExtraMaterials, debounceChatUpdate]);

  const handleMaterialSelect = (material: Material) => {
    setChosenMaterials((prev) => [...prev, materials?.find(({ id }) => id === material.id) as Material]);
    const filteredOptions = materialsOptions.filter(({ id }) => id !== material.id);
    setMaterialsOptions(filteredOptions);
  };

  const removeSelectedMaterial = (id: string) => {
    const material = chosenMaterials.find((material) => material.id === id) as Material;
    setChosenMaterials((prev) => prev.filter(({ id }) => id !== material.id));
    setMaterialsOptions((prev) => [...prev, material].sort((a, b) => a.name.localeCompare(b.name)));
  };

  useEffect(() => {
    setMaterialsOptions(materials as Material[]);
  }, [materials]);

  return (
    <div className="pt-5 border-t border-gray-600 text-gray-300 flex flex-col gap-5 flex-1">
      <h3 className="text-sm">Chat options</h3>

      <div className="flex flex-col gap-2.5">
        <label htmlFor="agents" className="text-xs">
          Chosen agent
        </label>
        <AgentsDropdown
          agents={agents}
          selectedAgent={agents.find((agent) => agent.id === selectedAgentId)}
          onSelect={setSelectedAgentId}
        />
      </div>

      <div className="flex flex-col gap-2.5">
        <label className="text-xs">Chosen materials</label>
        <Autocomplete options={materialsOptions} onOptionSelect={handleMaterialSelect} />
        <div className="flex flex-col gap-2.5 h-[100px] lg:h-[190px] overflow-y-auto w-full">
          {chosenMaterials.map((option) => {
            const OptionIcon = getEditableObjectIcon(option);
            return (
              <div
                key={option.id}
                className="flex justify-between items-center max-w-full w-max gap-2.5 bg-gray-700 px-2.5 py-2 rounded-[20px]"
              >
                <Icon icon={OptionIcon} className="w-6 h-6 min-h-6 min-w-6 text-material" />
                <p className="flex-1 truncate font-normal text-sm">{option.name}</p>
                <button onClick={() => removeSelectedMaterial(option.id)}>
                  <Icon icon={X} />
                </button>
              </div>
            );
          })}
        </div>
      </div>

      <div className="flex items-center gap-2.5 mt-auto">
        <Checkbox id="extraMaterials" checked={allowExtraMaterials} onChange={setAllowExtraMaterials} />
        <label htmlFor="extraMaterials" className="text-sm">
          Let AI add extra materials
        </label>
      </div>
    </div>
  );
};

type AgentsDropdownProps = {
  agents: Agent[];
  selectedAgent?: Agent;
  onSelect: (agentId: string) => void;
};

const AgentsDropdown = ({ agents, selectedAgent, onSelect }: AgentsDropdownProps) => {
  const [opened, setOpened] = useState<boolean>(false);

  return (
    <DropdownMenu open={opened} onOpenChange={setOpened}>
      <Trigger asChild>
        <button
          className={cn(
            'group flex justify-center align-center gap-[12px] rounded-[8px] border border-gray-500 px-[16px] py-[10px] text-gray-300 text-[16px] font-semibold w-full leading-[23px] hover:border-gray-300 transition duration-200 hover:text-gray-300',
            {
              'rounded-b-none bg-gray-700 border-gray-800 text-gray-500': opened,
            },
          )}
        >
          {selectedAgent ? (
            <div className="flex gap-2.5">
              <AgentAvatar agentId={selectedAgent.id} type="extraSmall" />
              <p>{selectedAgent.name}</p>
            </div>
          ) : (
            <p>AI Choice</p>
          )}
          <Icon
            icon={opened ? ChevronUp : ChevronDown}
            width={24}
            height={24}
            className="text-gray-500 ml-auto group-hover:text-gray-300 transition duration-200 w-[24px] h-[24px]"
          />
        </button>
      </Trigger>

      <Content
        className={cn('bg-gray-700 border-t-0 border-gray-800 p-0 w-[295px] h-40 overflow-auto z-50', {
          'rounded-t-none ': opened,
        })}
      >
        <Item
          className="group flex p-0 rounded-none hover:bg-gray-600 hover:outline-none w-full cursor-pointer"
          onClick={() => onSelect('aiChoice')}
        >
          <div className="flex items-center h-11 gap-[12px] px-[16px] py-[10px] text-[14px] text-gray-300 group-hover:text-white w-full">
            <p>AI Choice</p>
          </div>
        </Item>
        {agents
          .sort((a, b) => a.name.localeCompare(b.name))
          .map(({ id, name }) => (
            <Item
              key={id}
              onClick={() => onSelect(id)}
              className="group flex p-0 rounded-none hover:bg-gray-600 hover:outline-none w-full cursor-pointer"
            >
              <div className="flex items-center gap-[12px] px-[16px] py-[10px] text-[14px] text-gray-300 group-hover:text-white w-full">
                <AgentAvatar agentId={id} type="extraSmall" />
                <p>{name}</p>
              </div>
            </Item>
          ))}
      </Content>
    </DropdownMenu>
  );
};

export default ChatOptions;
