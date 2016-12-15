class ARN:
    fields = "arn partition service region account_id resource".split()
    def __init__(self, arn="arn:aws::::", **kwargs):
        self.__dict__.update(dict(zip(self.fields, arn.split(":", 5)), **kwargs))

class Domovoi(object):
    scheduled_tasks = {}
    sns_subscribers = {}

    def scheduled_function(self, schedule):
        def register_scheduled_task(func):
            if func.__name__ in self.scheduled_tasks:
                raise KeyError(func.__name__)
            self.scheduled_tasks[func.__name__] = dict(schedule=schedule, func=func)
            return func
        return register_scheduled_task

    def sns_topic_subscriber(self, topic_name):
        def register_scheduled_task(func):
            self.sns_subscribers[topic_name] = func
            return func
        return register_scheduled_task

    def s3_event_handler(self, bucket, event_type):
        # http://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.put_bucket_notification_configuration
        raise NotImplementedError()

    def dynamodb_event_handler(self):
        raise NotImplementedError()

    def email_receipt_handler(self):
        # http://boto3.readthedocs.io/en/latest/reference/services/ses.html#SES.Client.create_receipt_rule
        raise NotImplementedError()

    def cloudwatch_log_handler(self, log_group_name, filter_pattern):
        # http://boto3.readthedocs.io/en/latest/reference/services/logs.html#CloudWatchLogs.Client.put_subscription_filter
        raise NotImplementedError()

    def __call__(self, event, context):
        context.log("Domovoi dispatch of event {}".format(event))
        if "scheduled_task" in event:
            handler = self.scheduled_tasks[event["scheduled_task"]]["func"]
        elif "Records" in event:
            sns_topic = ARN(event["Records"][0]["Sns"]["TopicArn"]).resource
            handler = self.sns_subscribers[sns_topic]
        else:
            raise Exception("No handler found for event {}".format(event))
        result = handler(event, context)
        context.log(result)
        return result
