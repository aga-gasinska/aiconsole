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

import { useRef } from 'react';
import { useUserContextMenu } from '../../utils/common/useUserContextMenu';
import { ContextMenu, ContextMenuRef } from './ContextMenu';
import { useOpenSettings } from '@/utils/settings/useOpenSettings';
import { Icon } from './icons/Icon';
import { Settings } from 'lucide-react';
import { Button } from './Button';

interface TopBarProps {
  variant?: 'recentProjects' | 'chat';
}

export function TopBar({ children }: React.PropsWithChildren<TopBarProps>) {
  const menuItems = useUserContextMenu();
  const triggerRef = useRef<ContextMenuRef>(null);
  const openSettings = useOpenSettings();

  return (
    <div className="flex w-full px-[20px] py-[7px] border-b bg-transparent shadow-md border-gray-600 relative z-40 h-[80px] min-h-[80px]">
      <div className="flex gap-2 w-full items-center">
        {children}
        <ContextMenu options={menuItems} ref={triggerRef} triggerClassName="ml-auto">
          <Button variant="secondary" small iconOnly onClick={openSettings}>
            <Icon icon={Settings} width={24} height={24} />
          </Button>
        </ContextMenu>
      </div>
    </div>
  );
}
