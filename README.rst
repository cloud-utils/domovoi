Domovoi: AWS Lambda event handler manager
=========================================

*Domovoi* is an extension to `AWS Labs Chalice <https://github.com/awslabs/chalice>`_ to handle `AWS Lambda
<https://aws.amazon.com/lambda/>`_ `event sources
<http://docs.aws.amazon.com/lambda/latest/dg/invoking-lambda-function.html#intro-core-components-event-sources>`_ other
than HTTP requests through API Gateway. Domovoi lets you easily configure and deploy a Lambda function to run on a
schedule or in response to an `SNS <https://aws.amazon.com/sns/>`_ push notification:

.. code-block:: python

    import json, boto3, domovoi

    app = domovoi.Domovoi()

    @app.scheduled_function("cron(0 18 ? * MON-FRI *)")
    def foo(event, context):
        context.log("foo invoked at 06:00pm (UTC) every Mon-Fri")
        return dict(result=True)

    @app.scheduled_function("rate(1 minute)")
    def bar(event, context):
        context.log("bar invoked once a minute")
        boto3.resource("sns").create_topic(Name="bartender").publish(Message=json.dumps({"beer": 1}))
        return dict(result="Work work work")

    @app.sns_topic_subscriber("bartender")
    def tend(event, context):
        message = json.loads(event["Records"][0]["Sns"]["Message"])
        context.log(dict(beer="Quadrupel", quantity=message["beer"]))

    @app.cloudwatch_event_handler(source=["aws.ecs"])
    def monitor_ecs_events(event, context):
        message = json.loads(event["Records"][0]["Sns"]["Message"])
        context.log("Got an event from ECS: {}".format(message))

    @app.s3_event_handler(bucket="myS3bucket", events=["s3:ObjectCreated:*"], prefix="foo", suffix=".bar")
    def monitor_s3(event, context):
        message = json.loads(event["Records"][0]["Sns"]["Message"])
        context.log("Got an event from S3: {}".format(message))

Installation
------------
::

    pip install domovoi

Usage
-----
First-time setup::

    chalice new-project

Replace the Chalice app entry point (in ``app.py``) with the Domovoi app entry point as above, then deploy the event handlers::

    domovoi deploy

To stage files into the deployment package, use a ``domovoilib`` directory in your project where you would use
``chalicelib`` in Chalice. For example, ``my_project/domovoilib/rds_cert.pem`` becomes ``/var/task/domovoilib/rds_cert.pem``
with your function executing in ``/var/task/app.py`` with ``/var/task`` as the working directory. See the
`Chalice docs <http://chalice.readthedocs.io/>`_ for more information on how to set up Chalice configuration.

Supported event types
---------------------
See http://docs.aws.amazon.com/lambda/latest/dg/invoking-lambda-function.html for an overview of event sources that
can be used to trigger Lambda functions. Domovoi supports the following event sources:

* SNS subscriptions
* CloudWatch Events rule targets, including CloudWatch Scheduled Events (see http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html for a list of event types supported by CloudWatch Events)
* S3 events

TODO:

* CloudWatch Logs filter subscriptions
* DynamoDB events
* SES (email) events

Links
-----
* `Project home page (GitHub) <https://github.com/kislyuk/domovoi>`_
* `Documentation (Read the Docs) <https://domovoi.readthedocs.org/en/latest/>`_
* `Package distribution (PyPI) <https://pypi.python.org/pypi/domovoi>`_
* `Change log <https://github.com/kislyuk/domovoi/blob/master/Changes.rst>`_

Bugs
~~~~
Please report bugs, issues, feature requests, etc. on `GitHub <https://github.com/kislyuk/domovoi/issues>`_.

License
-------
Licensed under the terms of the `Apache License, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_.

.. image:: https://travis-ci.org/kislyuk/domovoi.png
        :target: https://travis-ci.org/kislyuk/domovoi
.. image:: https://codecov.io/github/kislyuk/domovoi/coverage.svg?branch=master
        :target: https://codecov.io/github/kislyuk/domovoi?branch=master
.. image:: https://img.shields.io/pypi/v/domovoi.svg
        :target: https://pypi.python.org/pypi/domovoi
.. image:: https://img.shields.io/pypi/l/domovoi.svg
        :target: https://pypi.python.org/pypi/domovoi
.. image:: https://readthedocs.org/projects/domovoi/badge/?version=latest
        :target: https://domovoi.readthedocs.org/
