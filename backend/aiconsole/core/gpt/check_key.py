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


from openai import AuthenticationError, OpenAI

from aiconsole.core.gpt.consts import MODEL_DATA

cached_good_keys = set()


# Verify the OpenAI key has access to the required models
def check_key(key: str) -> bool:
    if key in cached_good_keys:
        return True

    client = OpenAI(api_key=key)
    try:
        models = client.models.list().data
    except AuthenticationError:
        return False
    available_models = [model.id for model in models]
    needed_models = MODEL_DATA.keys()

    good = set(needed_models).issubset(set(available_models))

    if good:
        cached_good_keys.add(key)

    return good
