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

import { ChangeEvent, useRef, useState } from 'react';

import { Icon } from '@/components/common/icons/Icon';
import { useClickOutside } from '@/hooks/useClickOutside';
import { cn } from '@/utils/common/cn';
import { getEditableObjectIcon } from '@/utils/editables/getEditableObjectIcon';

type AutocompleteProps<T> = {
  options: T[];
  onOptionSelect: (option: T) => void;
  className?: string;
};

const Autocomplete = <T extends { id: string; name: string }>({
  options,
  onOptionSelect,
  className,
}: AutocompleteProps<T>) => {
  const [inputValue, setInputValue] = useState('');
  const [filteredOptions, setFilteredOptions] = useState<T[]>([]);
  const ref = useRef<HTMLDivElement>(null);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    setInputValue(inputValue);

    const regex = new RegExp(`^${inputValue}`, 'i');
    const filteredOptions = options.filter((item) => regex.test(item.name));
    setFilteredOptions(filteredOptions);
  };

  const handleOptionSelect = (selectedOption: T) => {
    onOptionSelect(selectedOption);
    setInputValue('');
    setFilteredOptions([]);
  };

  const handleClickOutside = () => {
    setInputValue('');
    setFilteredOptions([]);
  };

  useClickOutside(ref, handleClickOutside);

  return (
    <div className={cn('relative', className)} ref={ref}>
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Start writing to add..."
        className="bg-transparent py-2 focus:outline-none border-gray-400 text-white w-full placeholder:text-gray-400 placeholder:text-[15px]"
      />
      {inputValue && (
        <ul className="absolute max-h-[164px] overflow-auto w-full left-1/2 -translate-x-1/2 rounded border-1 border-gray-800">
          {filteredOptions.map((option) => {
            const OptionIcon = getEditableObjectIcon(option);
            return (
              <li
                key={option.id}
                onClick={() => handleOptionSelect(option)}
                className="w-full overflow-hidden truncate bg-gray-700 px-4 py-2 flex items-center gap-3 cursor-pointer hover:bg-gray-600"
              >
                <Icon icon={OptionIcon} className="w-6 h-6 min-h-6 min-w-6 text-material" />
                <span className="truncate flex-1">{option.name}</span>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default Autocomplete;
