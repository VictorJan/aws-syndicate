import json

from syndicate.core.transform.terraform.tf_resource_reference_builder import \
    build_role_arn_ref
from syndicate.core.transform.terraform.converter.tf_resource_converter import \
    TerraformResourceConverter


class BatchJobDefConverter(TerraformResourceConverter):

    def convert(self, name, resource):
        job_definition_type = resource.get('job_definition_type')
        container_properties = resource.get('container_properties')
        parameters = resource.get('parameters')
        timeout = resource.get('timeout')
        tags = resource.get('tags')
        retry_strategy = resource.get('retry_strategy')
        if container_properties:
            job_role_arn = container_properties.get('job_role_arn')
            execution_role_arn = container_properties.get('execution_role_arn')

        batch_job_definition = batch_job_def(job_def_name=name,
                                             job_def_type=job_definition_type,
                                             container_properties=container_properties,
                                             parameters=parameters,
                                             timeout=timeout, tags=tags,
                                             retry_strategy=retry_strategy)
        self.template.add_aws_batch_job_definition(meta=batch_job_definition)


def batch_job_def(job_def_name, job_def_type, container_properties,
                  parameters, tags, timeout, retry_strategy):
    params = {
        'name': job_def_name,
        'type': job_def_type
    }

    if parameters:
        params['parameters'] = parameters
    if tags:
        params['tags'] = tags
    if timeout:
        params['timeout'] = timeout
    if retry_strategy:
        params['retry_strategy'] = retry_strategy

    if container_properties:
        properties = {}

        image = container_properties.get('image')
        if image:
            properties['image'] = image
        vcpus = container_properties.get('vcpus')
        if vcpus:
            properties['vcpus'] = vcpus
        memory = container_properties.get('memory')
        if memory:
            properties['memory'] = memory
        command = container_properties.get('command', [])
        if command:
            properties['command'] = command
        job_role_arn = container_properties.get('job_role_arn')
        if job_role_arn:
            role_arn_ref = build_role_arn_ref(role_name=job_role_arn)
            properties['executionRoleArn'] = role_arn_ref

        if properties:
            params['container_properties'] = json.dumps(properties)

    resource = {
        job_def_name: params
    }
    return resource
