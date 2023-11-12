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

import { useNavigate } from 'react-router-dom';
import { v4 as uuidv4 } from 'uuid';
import { useContextMenu } from '@/hooks/useContextMenu';
import { Asset } from '@/types/types';
import { getAssetColor } from '@/utils/getAssetColor';
import { CHAT_COLOR, CHAT_ICON, getAssetIcon } from '@/utils/getAssetIcon';

export function useAddMenu() {
  const { showContextMenu, hideContextMenu, isContextMenuVisible } = useContextMenu();

  const navigate = useNavigate();
  const MaterialNoteIcon = getAssetIcon({ content_type: 'static_text' } as unknown as Asset); //Hack: Figure out a better interface
  const MaterialDynamicNoteIcon = getAssetIcon({ content_type: 'dynamic_text' } as unknown as Asset); //Hack: Figure out a better interface
  const MaterialPythonAPIIcon = getAssetIcon({ content_type: 'api' } as unknown as Asset); //Hack: Figure out a better interface
  const AgentIcon = getAssetIcon('agent');

  function showContextMenuReplacement() {
    return showContextMenu([
      {
        key: 'chat',
        icon: <CHAT_ICON className="w-4 h-4" style={{ color: CHAT_COLOR }} />,
        title: 'New Chat ...',
        onClick: () => {
          navigate(`/chats/${uuidv4()}`);
        },
      },
      {
        key: 'note',
        icon: <MaterialNoteIcon className="w-4 h-4" style={{ color: getAssetColor('material') }} />,
        title: 'New Note ...',
        onClick: () => {
          navigate(`/materials/new?type=static_text`);
        },
      },
      {
        key: 'dynamic_note',
        icon: <MaterialDynamicNoteIcon className="w-4 h-4" style={{ color: getAssetColor('material') }} />,
        title: 'New Dynamic Note ...',
        onClick: () => {
          navigate(`/materials/new?type=dynamic_text`);
        },
      },
      {
        key: 'python_api',
        icon: <MaterialPythonAPIIcon className="w-4 h-4" style={{ color: getAssetColor('material') }} />,
        title: 'New Python API ...',
        onClick: () => {
          navigate(`/materials/new?type=api`);
        },
      },
      {
        key: 'agent',
        icon: <AgentIcon className="w-4 h-4" style={{ color: getAssetColor('agent') }} />,
        title: 'New Agent ...',
        onClick: () => {
          navigate(`/agents/new`);
        },
      },
      /*static_text: 'Markdown formated text will be injected into AI context.',
      dynamic_text: 'A python function will generate markdown text to be injected into AI context.',
      api: 'Documentation will be extracted from code and injected into AI context as markdown text, code will be available to execute by AI without import statements.',
    */
    ]);
  }

  return { showContextMenu: showContextMenuReplacement, hideContextMenu, isContextMenuVisible };
}