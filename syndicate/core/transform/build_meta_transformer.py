#  Copyright 2021 EPAM Systems, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from abc import abstractmethod


class BuildMetaTransformer:

    def __init__(self, transformer_mapping):
        self.resources = list()
        self.transformer_mapping = transformer_mapping

    def transform_build_meta(self, build_meta):
        for name, resource in build_meta.items():
            resource_type = resource.get('resource_type')
            transformer = self.transformer_mapping.get(resource_type)
            if transformer is None:
                continue
            transformed_resource = transformer(name, resource)
            self.resources.append(transformed_resource)
        return self.__compose_template()

    @abstractmethod
    def output_file_name(self) -> str:
        pass

    @abstractmethod
    def __transform_iam_managed_policy(self, name, resource):
        pass

    @abstractmethod
    def __transform_iam_role(self, name, resource):
        pass

    @abstractmethod
    def __transform_lambda(self, name, resource):
        pass

    @abstractmethod
    def __compose_template(self):
        pass
