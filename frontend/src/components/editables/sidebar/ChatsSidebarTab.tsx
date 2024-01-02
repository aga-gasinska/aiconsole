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

import { useEditablesStore } from '@/store/editables/useEditablesStore';
import useGroupByDate from '@/utils/editables/useGroupByDate';
import SideBarItem from './SideBarItem';
import ChatOptions from '../assets/ChatOptions';

export const ChatsSidebarTab = () => {
  const chatHeadlines = useEditablesStore((state) => state.chats);
  const { today, yesterday, previous7Days, older } = useGroupByDate(chatHeadlines);

  const sections = [
    { title: 'Today', headlines: today },
    { title: 'Yesterday', headlines: yesterday },
    { title: 'Previous 7 days', headlines: previous7Days },
    { title: 'Older than 7 days', headlines: older },
  ];

  return (
    <div className="flex flex-col justify-between content-between pr-[20px] overflow-y-auto h-full">
      <div className="overflow-y-auto mb-5 min-h-[100px]">
        {sections.map(
          (section) =>
            section.headlines.length > 0 && (
              <div key={section.title}>
                <h3 className="uppercase px-[9px] py-[5px] text-gray-400 text-[12px] leading-[18px]">
                  {section.title}
                </h3>
                {section.headlines.map((chat) => (
                  <SideBarItem key={chat.id} editableObject={chat} editableObjectType="chat" />
                ))}
              </div>
            ),
        )}
      </div>

      <div className="w-full h-[375px] lg:h-[465px]">
        <ChatOptions />
      </div>
    </div>
  );
};
