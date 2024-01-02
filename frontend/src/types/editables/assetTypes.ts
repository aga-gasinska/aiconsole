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

import { z } from 'zod';

export type AssetDefinedIn = 'aiconsole' | 'project';
export const assetDefinedInOptions: AssetDefinedIn[] = ['aiconsole', 'project'];
export const AssetStatusSchema = z.enum(['disabled', 'enabled', 'forced']);
export type AssetStatus = z.infer<typeof AssetStatusSchema>;
export const assetStatusOptions: AssetStatus[] = ['disabled', 'enabled', 'forced'];
export type MaterialContentType = 'static_text' | 'dynamic_text' | 'api';
export const materialContenTypeOptions: MaterialContentType[] = ['static_text', 'dynamic_text', 'api'];
export type TabsValues = 'chats' | 'materials' | 'agents';

export type Material = Asset & {
  content_type: MaterialContentType;
  content: string;
};

export type RenderedMaterial = {
  id: string;
  content: string;
  error: string;
};

export const MaterialDefinitionSourceSchema = z.enum(['aiconsole', 'project']);
export type MaterialDefinitionSource = z.infer<typeof MaterialDefinitionSourceSchema>;

export const AssetTypeSchema = z.enum(['material', 'agent']);

export type AssetType = z.infer<typeof AssetTypeSchema>;

export const GPTModeSchema = z.enum(['quality', 'speed', 'cost']);

export type GPTMode = z.infer<typeof GPTModeSchema>;

export const GPTRoleSchema = z.enum(['user', 'system', 'assistant', 'tool']);

export type GPTRole = z.infer<typeof GPTRoleSchema>;

export const LanguageStrSchema = z.enum(['python', 'actionscript']);

export type LanguageStr = z.infer<typeof LanguageStrSchema>;

export type EditableObjectType = 'material' | 'agent' | 'chat';

export type EditableObjectTypePlural = 'materials' | 'agents' | 'chats';

export const EditableObjectSchema = z.object({
  id: z.string(),
  name: z.string(),
});

export type EditableObject = z.infer<typeof EditableObjectSchema>;

export const AssetSchema = EditableObjectSchema.extend({
  usage: z.string(),
  usage_examples: z.array(z.string()),
  defined_in: MaterialDefinitionSourceSchema,
  status: AssetStatusSchema,
  default_status: AssetStatusSchema,
  override: z.boolean(),
});

export type Asset = z.infer<typeof AssetSchema>;

export const AgentSchema = AssetSchema.extend({
  system: z.string(),
  gpt_mode: GPTModeSchema,
  execution_mode: z.string(),
});

export type Agent = z.infer<typeof AgentSchema>;
