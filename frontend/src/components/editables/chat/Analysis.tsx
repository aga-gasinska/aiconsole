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

import { BlinkingCursor } from '@/components/editables/chat/BlinkingCursor';
import { cn } from '@/utils/common/cn';
import { UserInfo } from '@/components/editables/chat/UserInfo';
import { useChatStore } from '../../../store/editables/chat/useChatStore';

export function Analysis() {
  const currentAnalysisRequestId = useChatStore((store) => store.currentAnalysisRequestId);
  const agentId = useChatStore((store) => store.agent_id);
  const relevantMaterialIds = useChatStore((store) => store.relevant_material_ids);
  const thinkingProcess = useChatStore((store) => store.thinking_process);
  const nextStep = useChatStore((store) => store.next_step);

  if (currentAnalysisRequestId) {
    return (
      <div className={cn('flex flex-row py-10 text-stone-400/50')}>
        <div className="container flex mx-auto gap-5 ">
          <UserInfo
            agentId={agentId !== 'user' ? agentId || '' : ''}
            materialsIds={agentId !== 'user' ? relevantMaterialIds || [] : []}
          />
          <div className="flex-grow mr-20">
            Analysing ...
            {
              <>
                {` ${thinkingProcess || ''}`}{' '}
                {nextStep && (
                  <>
                    <br /> Next step: <span className="text-secondary/50 leading-[24px]">{nextStep}</span>
                  </>
                )}{' '}
              </>
            }
            <BlinkingCursor />
          </div>
        </div>
      </div>
    );
  } else {
    return <></>;
  }
}
