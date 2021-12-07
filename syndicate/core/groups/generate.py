"""
    Copyright 2018 EPAM Systems, Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import os
import pathlib
import click

from syndicate.core.conf.generator import generate_configuration_files
from syndicate.core.generators.lambda_function import (
    generate_lambda_function)
from syndicate.core.generators.project import (generate_project_structure,
                                               PROJECT_PROCESSORS)
from syndicate.core.helper import (check_required_param, timeit, OrderedGroup,
                                   check_bundle_bucket_name,
                                   check_prefix_suffix_length,
                                   resolve_project_path)
from syndicate.core.generators.deployment_resources import (S3Generator,
                                                            DynamoDBGenerator)

GENERATE_GROUP_NAME = 'generate'
GENERATE_PROJECT_COMMAND_NAME = 'project'
GENERATE_CONFIG_COMMAND_NAME = 'config'
PROJECT_PATH_HELP = 'Path to project folder. ' \
                    'Default value: current working directory'


@click.group(name=GENERATE_GROUP_NAME, cls=OrderedGroup, chain=True)
def generate():
    """Generates project, lambda or configs"""


@generate.command(name=GENERATE_PROJECT_COMMAND_NAME)
@click.option('--name', nargs=1, callback=check_required_param,
              help='* The project name')
@click.option('--path', nargs=1,
              help=PROJECT_PATH_HELP)
@click.pass_context
@timeit()
def project(ctx, name, path):
    """
    Generates project with all the necessary components and in a right
    folders/files hierarchy to start developing in a min.
    """
    click.echo('Project name: {}'.format(name))

    proj_path = os.getcwd() if not path else path
    if not os.access(proj_path, os.X_OK | os.W_OK):
        click.echo(f"Incorrect permissions for the provided path '{proj_path}'")
        return
    click.echo('Project path: {}'.format(proj_path))
    generate_project_structure(project_name=name,
                               project_path=proj_path)


@generate.command(name='lambda')
@click.option('--name', nargs=1, multiple=True, type=str,
              callback=check_required_param,
              help='(multiple) * The lambda function name')
@click.option('--runtime', nargs=1, callback=check_required_param,
              help='* Lambda runtime',
              type=click.Choice(PROJECT_PROCESSORS))
@click.option('--project_path', nargs=1,
              help="Path to the project folder. Default value: the one "
                   "from the current config if it exists. "
                   "Otherwise - the current working directory",
              callback=resolve_project_path)
@click.pass_context
@timeit()
def lambda_function(ctx, name, runtime, project_path):
    """
    Generates required environment for lambda function
    """
    if not os.access(project_path, os.F_OK):
        click.echo(f"The provided path {project_path} doesn't exist")
        return
    elif not os.access(project_path, os.W_OK) or not os.access(project_path,
                                                               os.X_OK):
        click.echo(f"Incorrect permissions for the provided path "
                   f"'{project_path}'")
        return
    click.echo(f'Lambda names: {name}')
    click.echo(f'Runtime: {runtime}')
    click.echo(f'Project path: {project_path}')
    generate_lambda_function(project_path=project_path,
                             runtime=runtime,
                             lambda_names=name)


@generate.command(name=GENERATE_CONFIG_COMMAND_NAME)
@click.option('--name',
              required=True,
              help='* Name of the configuration to create. '
                   'Generated config will be created in folder '
                   '.syndicate-config-{name}. May contain name '
                   'of the environment.')
@click.option('--region',
              help='* The region that is used to deploy the application',
              required=True)
@click.option('--bundle_bucket_name',
              help='* Name of the bucket that is used for uploading artifacts.'
                   ' It will be created if specified.', required=True,
              callback=check_bundle_bucket_name)
@click.option('--access_key',
              help='AWS access key id that is used to deploy the application.')
@click.option('--secret_key',
              help='AWS secret key that is used to deploy the application.')
@click.option('--config_path',
              help='Path to store generated configuration file')
@click.option('--project_path',
              help=PROJECT_PATH_HELP)
@click.option('--prefix',
              help='Prefix that is added to project names while deployment '
                   'by pattern: {prefix}resource_name{suffix}. '
                   'Must be less than or equal to 5.',
              callback=check_prefix_suffix_length)
@click.option('--suffix',
              help='Suffix that is added to project names while deployment '
                   'by pattern: {prefix}resource_name{suffix}. '
                   'Must be less than or equal to 5.',
              callback=check_prefix_suffix_length)
@timeit()
def config(name, config_path, project_path, region, access_key,
           secret_key, bundle_bucket_name, prefix, suffix):
    """
    Creates Syndicate configuration files
    """
    generate_configuration_files(name=name,
                                 config_path=config_path,
                                 project_path=project_path,
                                 region=region,
                                 access_key=access_key,
                                 secret_key=secret_key,
                                 bundle_bucket_name=bundle_bucket_name,
                                 prefix=prefix,
                                 suffix=suffix)


@generate.command(name='dynamodb_table')
@click.option('--name', required=True, type=str, help="DynamoDB table name")
@click.option('--hash_key_name', required=True, type=str,
              help="DynamoDB table hash key")
@click.option('--hash_key_type', required=True,
              type=click.Choice(['S', 'N', 'B']),
              help="DynamoDB hash key type")
@click.option('--project_path', nargs=1,
              help="Path to the project folder. Default value: the one "
                   "from the current config if it exists. "
                   "Otherwise - the current working directory",
              callback=resolve_project_path)
@timeit()
def dynamodb_table(name, hash_key_name, hash_key_type, project_path):
    """Generates dynamoDB deployment resources template"""

    if not os.access(project_path, os.F_OK):
        click.echo(f"The provided path {project_path} doesn't exist")
        return
    elif not os.access(project_path, os.W_OK) or not os.access(project_path,
                                                               os.X_OK):
        click.echo(f"Incorrect permissions for the provided path "
                   f"'{project_path}'")
        return

    generator = DynamoDBGenerator(
        resource_name=name,
        hash_key_name=hash_key_name,
        hash_key_type=hash_key_type,
        project_path=project_path
    )
    generator.write_deployment_resource()
    click.echo(f"Table '{name}' with its meta was successfully added to "
               f"deployment resources")


@generate.command(name='s3_bucket')
@click.option('--name', required=True, type=str, help="S3 bucket name",
              callback=check_bundle_bucket_name)
@click.option('--project_path', nargs=1,
              help="Path to the project folder. Default value: the one "
                   "from the current config if it exists. "
                   "Otherwise - the current working directory",
              callback=resolve_project_path)
@timeit()
def s3_bucket(name, project_path):
    """Generates s3 bucket deployment resources template"""

    # this code is repeated, I know, that's temporal
    if not os.access(project_path, os.F_OK):
        click.echo(f"The provided path {project_path} doesn't exist")
        return
    elif not os.access(project_path, os.W_OK) or not os.access(project_path,
                                                               os.X_OK):
        click.echo(f"Incorrect permissions for the provided path "
                   f"'{project_path}'")
        return
    generator = S3Generator(
        resource_name=name,
        project_path=project_path
    )
    generator.write_deployment_resource()
