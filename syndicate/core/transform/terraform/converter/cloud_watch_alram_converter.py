from syndicate.core.transform.terraform.tf_transform_helper import \
    build_sns_topic_arn_ref
from syndicate.core.transform.terraform.converter.tf_resource_converter import \
    TerraformResourceConverter


class CloudWatchAlarmConverter(TerraformResourceConverter):

    def convert(self, name, resource):
        metric_name = resource.get('metric_name')
        period = resource.get('period')
        evaluation_periods = resource.get('evaluation_periods')
        threshold = resource.get('threshold')
        comparison_operator = resource.get('comparison_operator')
        statistic = resource.get('statistic')
        namespace = resource.get('namespace')
        alarm_actions = resource.get('sns_topics')
        sns_topic_arns = []
        if alarm_actions:
            for topic in alarm_actions:
                arn = build_sns_topic_arn_ref(sns_topic=topic)
                sns_topic_arns.append(arn)

        alarm = build_cloud_watch_alarm_meta(alarm_name=name,
                                             metric_name=metric_name,
                                             period=period,
                                             evaluation_periods=evaluation_periods,
                                             threshold=threshold,
                                             comparison_operator=comparison_operator,
                                             statistic=statistic,
                                             alarm_actions=sns_topic_arns,
                                             namespace=namespace)
        self.template.add_aws_cloudwatch_metric_alarm(alarm)


def build_cloud_watch_alarm_meta(metric_name, namespace, period, threshold,
                                 evaluation_periods, comparison_operator,
                                 statistic, alarm_name, alarm_actions):
    alarm = {
        "alarm_name": alarm_name,
        "comparison_operator": comparison_operator,
        "evaluation_periods": evaluation_periods
    }

    if metric_name:
        alarm.update({'metric_name': metric_name})

    if namespace:
        alarm.update({'namespace': namespace})

    if metric_name:
        alarm.update({'period': period})

    if namespace:
        alarm.update({'statistic': statistic})

    if namespace:
        alarm.update({'threshold': threshold})

    if alarm_actions:
        alarm.update({'alarm_actions': alarm_actions})

    resource = {
        alarm_name: alarm
    }
    return resource
