import json

PROVIDER_KEY = 'provider'
RESOURCE_KEY = 'resource'

LAMBDA_RESOURCE_NAME = 'aws_lambda_function'
IAM_POLICY_RESOURCE_NAME = 'aws_iam_policy'
IAM_ROLE_RESOURCE_NAME = 'aws_iam_role'
DYNAMO_DB_TABLE_RESOURCE_NAME = 'aws_dynamodb_table'
APP_AUTOSCALING_TARGET_RESOURCE_NAME = 'aws_appautoscaling_target'
APP_AUTOSCALING_POLICY_RESOURCE_NAME = 'aws_appautoscaling_policy'
API_GATEWAY_REST_API_RESOURCE_NAME = 'aws_api_gateway_rest_api'
API_GATEWAY_RESOURCE_RESOURCE_NAME = 'aws_api_gateway_resource'
API_GATEWAY_METHOD_RESPONSE_RESOURCE_NAME = 'aws_api_gateway_method_response'
API_GATEWAY_INTEGRATION_RESOURCE_NAME = 'aws_api_gateway_integration'
API_GATEWAY_STAGE_RESOURCE_NAME = 'aws_api_gateway_stage'
API_GATEWAY_DEPLOYMENT_RESOURCE_NAME = 'aws_api_gateway_deployment'
API_GATEWAY_INTEGRATION_RESPONSE_RESOURCE_NAME = 'aws_api_gateway_integration_response'
API_GATEWAY_METHOD_RESOURCE_NAME = 'aws_api_gateway_method'
S3_BUCKET_RESOURCE_NAME = 'aws_s3_bucket'

RESOURCE_TYPES = [LAMBDA_RESOURCE_NAME, IAM_POLICY_RESOURCE_NAME,
                  IAM_ROLE_RESOURCE_NAME, DYNAMO_DB_TABLE_RESOURCE_NAME,
                  APP_AUTOSCALING_TARGET_RESOURCE_NAME,
                  APP_AUTOSCALING_POLICY_RESOURCE_NAME,
                  API_GATEWAY_REST_API_RESOURCE_NAME,
                  API_GATEWAY_RESOURCE_RESOURCE_NAME,
                  API_GATEWAY_METHOD_RESPONSE_RESOURCE_NAME,
                  API_GATEWAY_INTEGRATION_RESOURCE_NAME,
                  API_GATEWAY_STAGE_RESOURCE_NAME,
                  API_GATEWAY_DEPLOYMENT_RESOURCE_NAME,
                  API_GATEWAY_INTEGRATION_RESPONSE_RESOURCE_NAME,
                  API_GATEWAY_METHOD_RESOURCE_NAME, S3_BUCKET_RESOURCE_NAME]


class TerraformTemplate(object):

    def __init__(self, provider, profile, region):
        self.aws_lambda_function = []
        self.aws_iam_policy = []
        self.aws_iam_role = []
        self.aws_dynamodb_table = []
        self.aws_appautoscaling_target = []
        self.aws_appautoscaling_policy = []
        self.aws_api_gateway_rest_api = []
        self.aws_api_gateway_resource = []
        self.aws_api_gateway_method_response = []
        self.aws_api_gateway_integration = []
        self.aws_api_gateway_stage = []
        self.aws_api_gateway_deployment = []
        self.aws_api_gateway_integration_response = []
        self.aws_api_gateway_method = []
        self.aws_s3_bucket = []

        self.compose_resources_mapping = {
            LAMBDA_RESOURCE_NAME: self._aws_lambda,
            IAM_POLICY_RESOURCE_NAME: self._aws_iam_policy,
            IAM_ROLE_RESOURCE_NAME: self._aws_iam_role,
            DYNAMO_DB_TABLE_RESOURCE_NAME: self._aws_dynamodb_table,
            APP_AUTOSCALING_TARGET_RESOURCE_NAME: self._aws_appautoscaling_target,
            APP_AUTOSCALING_POLICY_RESOURCE_NAME: self._aws_appautoscaling_policy,
            API_GATEWAY_REST_API_RESOURCE_NAME: self._aws_api_gateway_rest_api,
            API_GATEWAY_RESOURCE_RESOURCE_NAME: self._aws_api_gateway_resource,
            API_GATEWAY_METHOD_RESPONSE_RESOURCE_NAME: self._aws_api_gateway_method_response,
            API_GATEWAY_INTEGRATION_RESOURCE_NAME: self._aws_api_gateway_integration,
            API_GATEWAY_STAGE_RESOURCE_NAME: self._aws_api_gateway_stage,
            API_GATEWAY_DEPLOYMENT_RESOURCE_NAME: self._aws_api_gateway_deployment,
            API_GATEWAY_INTEGRATION_RESPONSE_RESOURCE_NAME: self._aws_api_gateway_integration_response,
            API_GATEWAY_METHOD_RESOURCE_NAME: self._aws_api_gateway_method,
            S3_BUCKET_RESOURCE_NAME: self._aws_aws_s3_bucket
        }

        self.resources = list()
        self.provider = list()
        provider_config = {
            provider: [
                {
                    "profile": profile,
                    "region": region
                }
            ]
        }
        self.provider.append(provider_config)

    def add_aws_lambda(self, meta):
        self.aws_lambda_function.append(meta)

    def add_aws_iam_policy(self, meta):
        self.aws_iam_policy.append(meta)

    def add_aws_iam_role(self, meta):
        self.aws_iam_role.append(meta)

    def add_aws_dynamodb_table(self, meta):
        self.aws_dynamodb_table.append(meta)

    def add_aws_appautoscaling_target(self, meta):
        self.aws_appautoscaling_target.append(meta)

    def add_aws_appautoscaling_policy(self, meta):
        self.aws_appautoscaling_policy.append(meta)

    def add_aws_api_gateway_rest_api(self, meta):
        self.aws_api_gateway_rest_api.append(meta)

    def add_aws_api_gateway_resource(self, meta):
        self.aws_api_gateway_resource.append(meta)

    def add_aws_api_gateway_method_response(self, meta):
        self.aws_api_gateway_method_response.append(meta)

    def add_aws_api_gateway_integration(self, meta):
        self.aws_api_gateway_integration.append(meta)

    def add_aws_api_gateway_stage(self, meta):
        self.aws_api_gateway_stage.append(meta)

    def add_aws_api_gateway_deployment(self, meta):
        self.aws_api_gateway_deployment.append(meta)

    def add_aws_api_gateway_integration_response(self, meta):
        self.aws_api_gateway_integration_response.append(meta)

    def add_aws_api_gateway_method(self, meta):
        self.aws_api_gateway_method.append(meta)

    def add_aws_s3_bucket(self, meta):
        self.aws_s3_bucket.append(meta)

    def _aws_lambda(self):
        return self.aws_lambda_function

    def _aws_iam_policy(self):
        return self.aws_iam_policy

    def _aws_iam_role(self):
        return self.aws_iam_role

    def _aws_dynamodb_table(self):
        return self.aws_dynamodb_table

    def _aws_appautoscaling_target(self):
        return self.aws_appautoscaling_target

    def _aws_appautoscaling_policy(self):
        return self.aws_appautoscaling_policy

    def _aws_api_gateway_rest_api(self):
        return self.aws_api_gateway_rest_api

    def _aws_api_gateway_resource(self):
        return self.aws_api_gateway_resource

    def _aws_api_gateway_method_response(self):
        return self.aws_api_gateway_method_response

    def _aws_api_gateway_integration(self):
        return self.aws_api_gateway_integration

    def _aws_api_gateway_stage(self):
        return self.aws_api_gateway_stage

    def _aws_api_gateway_deployment(self):
        return self.aws_api_gateway_deployment

    def _aws_api_gateway_integration_response(self):
        return self.aws_api_gateway_integration_response

    def _aws_api_gateway_method(self):
        return self.aws_api_gateway_method

    def _aws_aws_s3_bucket(self):
        return self.aws_s3_bucket

    def add_dynamo_db_stream(self, table_name, view_type):
        for table in self.aws_dynamodb_table:
            for resource in table.values():
                if table_name == resource.get('name'):
                    resource.update({'stream_enabled': 'true'})
                    resource.update({'stream_view_type': view_type})

    def compose_resources(self):
        for res_type in RESOURCE_TYPES:
            resource_extractor = self.compose_resources_mapping.get(res_type)
            resources_meta = resource_extractor()
            if resources_meta:
                self.resources.append({res_type: resources_meta})
        return json.dumps({PROVIDER_KEY: self.provider,
                           RESOURCE_KEY: self.resources})
