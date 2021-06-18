import json
import schemathesis
import boto3
import requests
import os
import click

from syndicate.commons.log_helper import get_logger
from syndicate.core import ResourceProvider
from syndicate.core.conf.processor import ConfigHolder
from syndicate.core.build.bundle_processor import load_deploy_output
from syndicate.core.build.deployment_processor import _filter_the_dict
from syndicate.core.helper import exit_on_exception
from requests_aws_sign import AWSV4Sign


_LOG = get_logger('syndicate.core.build.warmup_processor')

ANY_METHOD = 'x-amazon-apigateway-any-method'
GET_METHOD = 'get'
POST_METHOD = 'post'
PUT_METHOD = 'put'
PATCH_METHOD = 'patch'
DELETE_METHOD = 'delete'
OPTIONS_METHOD = 'options'

methods_check = {
    POST_METHOD: requests.post,
    GET_METHOD: requests.get,
    PUT_METHOD: requests.put,
    PATCH_METHOD: requests.patch,
    DELETE_METHOD: requests.delete
}


def process_schemas(schemas_list):
    uri_method_dict = dict()
    for schema in schemas_list:
        url = schema.base_url.replace(schema.base_path[:-1], schema.base_path[1:-1])
        resources = schema.operations
        for resource, definition in resources.items():
            resource_url = url + resource
            for method in definition:
                if method != OPTIONS_METHOD:
                    if resource_url not in uri_method_dict:
                        uri_method_dict.update({resource_url: [method]})
                    elif resource_url in uri_method_dict:
                        uri_method_dict[resource_url].append(method)
    return uri_method_dict


def get_aws_sign():
    CONF_PATH = os.environ.get('SDCT_CONF')
    CONFIG = ConfigHolder(CONF_PATH)
    region = CONFIG.region
    boto3_session = boto3.session.Session()
    credentials = boto3_session.get_credentials()
    credentials.access_key = CONFIG.aws_access_key_id
    credentials.secret_key = CONFIG.aws_secret_access_key
    service = 'execute-api'
    auth = AWSV4Sign(credentials, region, service)
    return auth


def warm_upper(uri_method_dict):
    auth = get_aws_sign()
    headers = {"Content-Type": "application/json"}
    payload = {"warmUp": "true"}
    for uri, methods in uri_method_dict.items():
        for method in methods:
            if method in (POST_METHOD, PUT_METHOD, DELETE_METHOD):
                warmup_method = methods_check.get(method)
                response = warmup_method(uri, auth=auth, headers=headers, json=payload)
                click.echo(f'URL: {uri} '
                           f'Method: {method} {response.status_code} {response.reason}')
            elif method == GET_METHOD:
                warmup_method = methods_check.get(method)
                response = warmup_method(uri, auth=auth, data=payload)
                click.echo(f'URL: {uri} '
                           f'Method: {method} Status code: {response.status_code} Reason: {response.reason}')


def _get_api_gw_client():
    return ResourceProvider.instance.api_gw().connection.client


def _replace_method_any(schema_file):
    paths = schema_file.get('paths')
    for resource in paths:
        if ANY_METHOD in paths[resource].keys():
            paths[resource]['get'] = paths[resource].pop(ANY_METHOD)
    return schema_file


def transform_to_schema(exported_schema):
    file_schema = json.loads(exported_schema['body'].read())
    file_schema = _replace_method_any(file_schema)
    schema = schemathesis.from_file(str(file_schema),
                                    base_url=find_api_url(file_schema))
    return schema


def get_api_gw_export(rest_api_id, stage_name):
    api_gw_client = _get_api_gw_client()
    exported_schema = api_gw_client.get_export(
        restApiId=rest_api_id,
        stageName=stage_name,
        exportType='oas30',
        accepts='application/json')
    return exported_schema


def get_api_stages(rest_api_id, stages_info):
    allowed_api_id = {}
    stages = stages_info.get('item')
    for stage in stages:
        stage_name = stage.get('stageName')
        exported_schema = get_api_gw_export(rest_api_id, stage_name)
        if rest_api_id not in allowed_api_id:
            allowed_api_id.update({rest_api_id: [exported_schema]})
        else:
            allowed_api_id[rest_api_id].append(exported_schema)
    return allowed_api_id


def process_existed_api_gw_id():
    api_gw_client = _get_api_gw_client()
    all_apis = api_gw_client.get_rest_apis().get('items', {})
    schemas_list = []
    all_api_id = set()
    allowed_api_id = {}
    for api in all_apis:
        rest_api_id = api['id']
        stages_info = api_gw_client.get_stages(restApiId=rest_api_id)
        allowed_api_id = get_api_stages(rest_api_id, stages_info)
        all_api_id.add(rest_api_id)

    no_stage_api = set(all_api_id).difference(allowed_api_id)
    click.echo(f'API Gateway ID without Stages: {", ".join(no_stage_api)}')
    click.echo(f'Allowed API Gateway ID: {", ".join(allowed_api_id)}')
    user_input_id = input('Select API from existing (multiple IDs must be separated by commas): ')
    user_input_id = user_input_id.split(",")

    for user_input in user_input_id:
        user_input = user_input.strip()
        if user_input not in allowed_api_id:
            raise AssertionError(f'Specify only allowed IDs: {", ".join(allowed_api_id)}')
        for api_gw_meta in allowed_api_id[user_input]:
            schema = transform_to_schema(api_gw_meta)
            schemas_list.append(schema)
    return schemas_list


def process_inputted_api_gw_id(api_id):
    api_gw_client = _get_api_gw_client()
    schemas_list = []
    all_apis = api_gw_client.get_rest_apis().get('items', {})
    allowed_id = []
    for api in all_apis:
        allowed_id.append(api['id'])
    for rest_api_id in api_id:
        if rest_api_id not in allowed_id:
            click.echo(f'Provided {rest_api_id} API ID does not exists')
            continue
        stages_info = api_gw_client.get_stages(restApiId=rest_api_id)
        allowed_api_id = get_api_stages(rest_api_id, stages_info)
        no_stage_api = set(api_id).difference(set(allowed_api_id))
        click.echo(f'API Gateway ID without Stages: {", ".join(no_stage_api)}')

        for id, api_gw_meta in allowed_api_id.items():
            for meta in api_gw_meta:
                schema = transform_to_schema(meta)
                schemas_list.append(schema)
    return schemas_list


def load_schema(api_gw_resources_meta):
    schemes = []
    for resource_arn, meta in api_gw_resources_meta.items():
        rest_api_id = resource_arn.split('/')[-1]
        stage_name = meta.get('resource_meta', {}).get('deploy_stage')

        exported_schema = get_api_gw_export(rest_api_id, stage_name)

        schema = transform_to_schema(exported_schema)
        schemes.append(schema)
    return schemes


@exit_on_exception
def warmup_resources(bundle_name, deploy_name):
    output = load_deploy_output(bundle_name, deploy_name)

    filters = [
        lambda v: v['resource_meta'].get('resource_type') == 'api_gateway'
    ]

    for function in filters:
        output = _filter_the_dict(dictionary=output, callback=function)

    if not output:
        _LOG.warning('No resources to warmup, exiting')
        return

    schemes = load_schema(api_gw_resources_meta=output)
    return schemes


def find_api_url(schema_doc):
    server = schema_doc['servers'][0]
    api_base_path = server['variables']['basePath']['default']
    url = server['url'].format(basePath=api_base_path)
    return url
