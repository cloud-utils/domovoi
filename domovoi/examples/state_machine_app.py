#!/usr/bin/env python3.6

import os, sys, json, time, random, signal, base64, pickle, zlib
import boto3, domovoi

app = domovoi.Domovoi()

sfn = {
    "Comment": """
    This is a Domovoi integrated AWS Step Functions state machine. It uses AWS Lambda as the task executor.
    Domovoi will replace the Resource field of all Task states with the ARN of the appropriate lambda function managed
    by Domovoi.
    See AWS documentation of the state machine language here:
        http://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html
    See AWS documentation of *Choice* state conditionals here:
        http://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-choice-state.html
    The *Sleep* state can be used to wait on other events without busy-waiting.
    Use the following command to invoke the state machine:
        $ aws stepfunctions start-execution --state-machine-arn ARN --input '{"x": 1}',
    where ARN is displayed in the result of `domovoi deploy`.
    State machine input is passed directly in the `event` argument to the task handlers. There is a 32KB I/O size limit.
    """,
    "StartAt": "Worker",
    "States": {
        "Worker": {
            "Type": "Task",
            "Resource": None,  # This will be set by Domovoi to the Lambda ARN
            "Next": "Branch"
        },
        "Branch": {
            "Type": "Choice",
            "Choices": [{
                "Variable": "$.finished",
                "BooleanEquals": True,
                "Next": "Sleep"
            }],
            "Default": "Worker"
        },
        "Sleep": {
            "Type": "Wait",
            # This is a delay step that can be set by the worker lambda to avoid busy-waiting.
            "SecondsPath": "$.sleep_seconds",
            "Next": "Finalizer"
        },
        "Finalizer": {
            "Type": "Task",
            "Resource": None,  # This will be set by Domovoi to the Lambda ARN
            "End": True
        }
    }
}

class DomovoiTimeout(Exception):
    pass

class Worker:
    def run(self, x):
        # The run() function should save its work in progress in attributes attached to self.
        # If the Lambda function runs out of time, the worker instance is pickled and restored when the lambda is
        # restarted, but all other state is lost.
        self.x = getattr(self, "x", 0) + x
        if random.random() < 0.8:
            while True:
                # This represents some long-running task that may not be interruptible from within Python.
                time.sleep(9000)
        return dict(x=self.x, sleep_seconds=random.randrange(8))

@app.step_function_task(state_name="Worker", state_machine_definition=sfn)
def do_work(event, context):
    def alarm_handler(signum, frame):
        raise DomovoiTimeout("Time to save state")

    signal.signal(signal.SIGALRM, alarm_handler)
    timeout_seconds = (context.get_remaining_time_in_millis() / 1000) - 10
    context.log("Setting timeout to {}".format(timeout_seconds))
    signal.alarm(timeout_seconds)

    if "state" in event:
        worker = pickle.loads(zlib.decompress(base64.b64decode(event["state"])))
    else:
        worker = Worker()

    try:
        result = worker.run(event["x"])
    except DomovoiTimeout:
        event.update(state=base64.b64encode(zlib.compress(pickle.dumps(worker))).decode(), finished=False)
        return event

    event.update(result, finished=True)
    return event

@app.step_function_task(state_name="Finalizer", state_machine_definition=sfn)
def finish_work(event, context):
    return {"result": event["x"]}
