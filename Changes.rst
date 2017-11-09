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
