from __future__ import absolute_import, division, print_function, unicode_literals

import json, gzip, base64

from chalice.app import Chalice

class DomovoiException(Exception):
    pass

class ARN:
    fields = "arn partition service region account_id resource".split()
    def __init__(self, arn="arn:aws::::", **kwargs):
        self.__dict__.update(dict(zip(self.fields, arn.split(":", 5)), **kwargs))

class Domovoi(Chalice):
    cloudwatch_events_rules = {}
    sns_subscribers = {}
    s3_subscribers = {}
    sfn_tasks = {}
    cwl_sub_filters = {}
    def __init__(self, app_name="Domovoi", configure_logs=True):
        Chalice.__init__(self, app_name=app_name, configure_logs=configure_logs)

    def scheduled_function(self, schedule):
        return self.cloudwatch_rule(schedule_expression=schedule, event_pattern=None)

    def sns_topic_subscriber(self, topic_name):
        def register_sns_subscriber(func):
            self.sns_subscribers[topic_name] = func
            return func
        return register_sns_subscriber

    def dynamodb_event_handler(self):
        raise NotImplementedError()

    def email_receipt_handler(self):
        # http://boto3.readthedocs.io/en/latest/reference/services/ses.html#SES.Client.create_receipt_rule
        raise NotImplementedError()

    def cloudwatch_logs_sub_filter_handler(self, log_group_name, filter_pattern):
        def register_cwl_subscription_filter(func):
            self.cwl_sub_filters[log_group_name] = dict(log_group_name=log_group_name, filter_pattern=filter_pattern,
                                                        func=func)
            return func
        return register_cwl_subscription_filter

    def cloudwatch_event_handler(self, **kwargs):
        return self.cloudwatch_rule(schedule_expression=None, event_pattern=kwargs)

    def s3_event_handler(self, bucket, events, prefix=None, suffix=None, use_sns=True):
        def register_s3_subscriber(func):
            self.s3_subscribers[bucket] = dict(events=events, prefix=prefix, suffix=suffix, func=func, use_sns=use_sns)
            return func
        return register_s3_subscriber

    def cloudwatch_rule(self, schedule_expression, event_pattern):
        def register_rule(func):
            if func.__name__ in self.cloudwatch_events_rules:
                raise KeyError(func.__name__)
            rule = dict(schedule_expression=schedule_expression, event_pattern=event_pattern, func=func)
            self.cloudwatch_events_rules[func.__name__] = rule
            return func
        return register_rule

    def step_function_task(self, state_name, state_machine_definition):
        def register_sfn_task(func):
            if state_name in self.sfn_tasks:
                raise KeyError(state_name)
            self.sfn_tasks[state_name] = dict(state_name=state_name,
                                              state_machine_definition=state_machine_definition,
                                              func=func)
            return func
        return register_sfn_task

    def _find_sns_s3_event_sub(self, sns_s3_event):
        assert sns_s3_event['Records'][0]["Sns"]['Subject'] == 'Amazon S3 Notification'
        s3_event = json.loads(sns_s3_event['Records'][0]["Sns"]["Message"])
        s3_bucket_name = s3_event.get("Bucket") or s3_event['Records'][0]["s3"]["bucket"]["name"]
        handler = self.s3_subscribers[s3_bucket_name]["func"] if s3_bucket_name in self.s3_subscribers else None
        return s3_event, handler

    def __call__(self, event, context):
        context.log("Domovoi dispatch of event {}".format(event))
        invoked_function_arn = ARN(context.invoked_function_arn)
        if "task_name" in event:
            if event["task_name"] not in self.cloudwatch_events_rules:
                raise DomovoiException("Received CloudWatch event for a task with no known handler")
            handler = self.cloudwatch_events_rules[event["task_name"]]["func"]
            event = event["event"]
        elif "Records" in event and "s3" in event["Records"][0]:
            s3_bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
            if s3_bucket_name not in self.s3_subscribers:
                raise DomovoiException("Received S3 event for a bucket with no known handler")
            handler = self.s3_subscribers[s3_bucket_name]["func"]
        elif "Records" in event and "Sns" in event["Records"][0]:
            try:
                event, handler = self._find_sns_s3_event_sub(event)
            except Exception:
                sns_topic = ARN(event["Records"][0]["Sns"]["TopicArn"]).resource
                if sns_topic not in self.sns_subscribers:
                    raise DomovoiException("Received SNS or S3-SNS event with no known handler")
                handler = self.sns_subscribers[sns_topic]
        elif "domovoi-stepfunctions-task" in invoked_function_arn.resource:
            _, lambda_name, lambda_alias = invoked_function_arn.resource.split(":")
            assert lambda_alias.startswith("domovoi-stepfunctions-task-")
            task_name = lambda_alias[len("domovoi-stepfunctions-task-"):]
            handler = self.sfn_tasks[task_name]["func"]
        elif "awslogs" in event:
            event = json.loads(gzip.decompress(base64.b64decode(event["awslogs"]["data"])))
            handler = self.cwl_sub_filters[event["logGroup"]]["func"]
        else:
            raise DomovoiException("No handler found for event {}".format(event))
        result = handler(event, context)
        context.log(result)
        return result
