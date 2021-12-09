import json
from syndicate.core.generators.deployment_resources.base_generator import \
    BaseDeploymentResourceGenerator
from syndicate.core.constants import IAM_ROLE, IAM_POLICY
from syndicate.core.generators import _read_content_from_file
from syndicate.commons.log_helper import get_logger, get_user_logger
import click

_LOG = get_logger(
    'syndicate.core.generators.deployment_resources.iam_role_generator')
USER_LOG = get_user_logger()


class IAMRoleGenerator(BaseDeploymentResourceGenerator):
    RESOURCE_TYPE = IAM_ROLE
    REQUIRED_RAPAMS = ['principal_service', ]
    NOT_REQUIRED_DEFAULTS = {
        "predefined_policies": list,
        "custom_policies": list,
        "allowed_accounts": list,
        "external_id": None,
        "instance_profile": bool
    }

    def _resolve_not_required_configuration(self) -> dict:
        try:
            self.validate_custom_policies_existence()
        except ValueError as e:
            raise click.BadParameter(str(e), param_hint='custom_policies')
        if self._dict['principal_service'] == 'ec2' and \
                not self._dict['instance_profile']:
            USER_LOG.info("Setting 'instance_profile' value to 'True' because "
                          "it wasn't specified and principal service is 'ec2'")
            self._dict['instance_profile'] = True
        return super()._resolve_not_required_configuration()


    def validate_custom_policies_existence(self):
        dep_res_files = self._get_deployment_resources_files()
        custom_policies = set(self._dict.get('custom_policies', []))
        _LOG.info(f"Validating existence of these policies: {custom_policies}")
        for file in dep_res_files:
            data = json.loads(_read_content_from_file(file))
            available_policies = set(filter(
                lambda name: data[name]['resource_type'] == IAM_POLICY, data))
            custom_policies = custom_policies - available_policies
        if custom_policies:
            message = f"Custom policies: {custom_policies} was not found " \
                      f"in deployment resources"
            _LOG.error(f"Validation error: {message}")
            raise ValueError(message)
        _LOG.info(f"Validation successfully finished, policies exist")
