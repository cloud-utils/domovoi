Changes for v1.7.6 (2018-08-28)
===============================

-  Remove debug statement

Changes for v1.7.5 (2018-08-14)
===============================

-  Grant SQS permissions to invoke lambda

Changes for v1.7.4 (2018-07-10)
===============================

-  Allow queue attributes to be set in SQS

Changes for v1.7.3 (2018-07-06)
===============================

-  SQS S3 event envelope support

Changes for v1.7.2 (2018-07-05)
===============================

-  Support state machine introspection and SQS-SFN springboard

-  Update docs for SQS

Changes for v1.7.1 (2018-07-05)
===============================

-  Don’t assume eventSource exists

Changes for v1.7.0 (2018-07-05)
===============================

-  Add support for SQS event sources

Changes for v1.6.1 (2018-06-06)
===============================

-  Set function description from “description” config key

-  Fix version reporting and provide it in published Lambda tag

Changes for v1.6.0 (2018-06-05)
===============================

-  Domovoi is now compatible with Chalice 1.2+. This should be a
   backwards compatible change. However, Chalice underwent a complete
   deployment system rewrite in version 1.2, so deployment state or
   other aspects of your app’s deployment may be affected. You may need
   to clear the deployment state of your app.

Changes for v1.5.8 (2018-05-04)
===============================

-  Allow customizable rule name for @scheduled_function (fixes #9)

Changes for v1.5.7 (2018-05-03)
===============================

-  Ensure domovoi errors when there is no handler

Changes for v1.5.6 (2018-04-09)
===============================

-  Allow configurable concurrency reservation

Changes for v1.5.5 (2018-03-16)
===============================

-  Add support for new-project and update docs

Changes for v1.5.4 (2018-03-03)
===============================

-  Skip updating event source mapping when diff is null

Changes for v1.5.3 (2018-02-21)
===============================

-  Avoid triggering Lambda API rate limits when managing state aliases

Changes for v1.5.2 (2018-02-05)
===============================

-  Ensure SNS topic names can represent all DNS-compliant S3 bucket
   names. Fixes #5

Changes for v1.5.1 (2018-02-01)
===============================

-  Fix routing of domovoi dynamodb handlers

Changes for v1.5.0 (2018-02-01)
===============================

-  Add DynamoDB streams support

-  Bypass prompt when writing IAM policy for the first time

Changes for v1.4.5 (2017-12-12)
===============================

-  Only call step\_function\_task if the state has a Resource field
   that's callable

Changes for v1.4.4 (2017-12-11)
===============================

-  Allow state machine registration; pass state name in context

-  Deconflict concurrent S3 notification config operations

Changes for v1.4.3 (2017-11-29)
===============================

-  Improve SM updates: use update\_state\_machine

Changes for v1.4.2 (2017-11-14)
===============================

Accommodate eventual consistency in SM update loop

Changes for v1.4.1 (2017-11-14)
===============================

-  Add statement to debug SM deploy loop crash

Changes for v1.4.0 (2017-11-09)
===============================

-  Add support for CloudWatch Logs subscription filter events

-  Expand docs for step function / state machine examples

Changes for v1.3.2 (2017-11-07)
===============================

-  Support nested states

Changes for v1.3.1 (2017-10-30)
===============================

-  Key state machine tasks by state name, not function name

-  Parameterize sfn trust statement by region

Changes for v1.3.0 (2017-10-26)
===============================

-  Add step functions support

Changes for v1.2.6 (2017-08-26)
===============================

-  Monkey-patch chalice to avoid dependency wheel management bug

-  Use more intuitive errors when handler not found

Changes for v1.2.5 (2017-08-17)
===============================

Avoid running privileged op on update

Changes for v1.2.4 (2017-08-17)
===============================

-  Chalice 1.0 compat, part 3

Changes for v1.2.3 (2017-08-17)
===============================

-  Chalice 1.0 compat, part 2

Changes for v1.2.2 (2017-08-17)
===============================

Chalice 1.0 compatibility fixes

Changes for v1.2.1 (2017-07-14)
===============================

-  Simplify DLQ handling; add docs for DLQ

Changes for v1.2.0 (2017-07-14)
===============================

-  Support DLQ lambda config

Changes for v1.1.1 (2017-07-05)
===============================

-  Parameterize stage name, part 2

Changes for v1.1.0 (2017-07-05)
===============================

-  Parameterize stage name

Changes for v1.0.9 (2017-06-24)
===============================

-  Forward S3 notifications through SNS by default

Changes for v1.0.8 (2017-06-24)
===============================

-  Don't clobber existing S3 bucket notifications

Changes for v1.0.7 (2017-06-22)
===============================

-  Pass through configure\_logs

-  Test improvements

Changes for v1.0.6 (2017-06-15)
===============================

Fix error in release

Changes for v1.0.5 (2017-06-15)
===============================

Enable idempotent Lambda permission grants

Changes for v1.0.4 (2017-06-09)
===============================

-  Hardcode no autogen policy

Changes for v1.0.3 (2017-06-08)
===============================

-  Ensure S3 bucket notifications work without filters specified

Changes for v1.0.2 (2017-06-01)
===============================

-  Fix dispatching of S3 events

-  Fixes to deploy procedure

Changes for v1.0.1 (2017-06-01)
===============================

-  Fix event subscriptions

Changes for v1.0.0 (2017-05-28)
===============================

-  Update to be compatible with Chalice 0.8 and Python 3.6




Changes for v0.0.3 (2016-12-19)
===============================

-  Autogenerate IAM policy

-  Release automation

Version 0.0.1 (2016-12-14)
--------------------------
- Initial release.
