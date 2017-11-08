#!/usr/bin/env python3.6

import os, sys, json, time, random, signal, base64, pickle, zlib
import boto3, domovoi

app = domovoi.Domovoi()

sfn = {
    "Comment": """
    This is a Domovoi integrated AWS Step Functions state machine using a threadpool pattern.
    See https://github.com/kislyuk/domovoi/blob/master/domovoi/examples/state_machine_app.py for more information on
    this state machine.
    """,
    "StartAt": "Scatter",
    "States": {
        "Scatter": {
            "Type": "Task",
            "Resource": None,  # This will be set by Domovoi to the Lambda ARN
            "Next": "Threadpool"
        },
        "Threadpool": {
            "Type": "Parallel",
            "Branches": [],
            "Next": "Finalizer"
        },
        "Finalizer": {
            "Type": "Task",
            "Resource": None,  # This will be set by Domovoi to the Lambda ARN
            "End": True
        }
    }
}

sfn_thread = {
    "StartAt": "Worker{t}",
    "States": {
        "Worker{t}": {
            "Type": "Task",
            "Resource": None,  # This will be set by Domovoi to the Lambda ARN
            "Next": "Branch{t}"
        },
        "Branch{t}": {
            "Type": "Choice",
            "Choices": [{
                "Variable": "$.finished",
                "BooleanEquals": True,
                "Next": "EndThread{t}"
            }],
            "Default": "Worker{t}"
        },
        "EndThread{t}": {
            "Type": "Pass",
            "End": True
        }
    }
}

num_threads = 64

class DomovoiTimeout(Exception):
    pass

@app.step_function_task(state_name="Scatter", state_machine_definition=sfn)
def scatter(event, context):
    # The scatter function should initialize and partition work between workers.
    # Each worker will receive the same event payload. You can change this using the state machine I/O processing
    # directives described in
    # http://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-input-output-processing.html,
    # or distribute work out-of-band through an SQS queue or similar.
    # Workers can introspect their state name (which contains the "thread ID") via context.invoked_function_arn.
    return event

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
        return dict(x=self.x)

def do_work(event, context):
    def alarm_handler(signum, frame):
        raise DomovoiTimeout("Time to save state")

    signal.signal(signal.SIGALRM, alarm_handler)
    timeout_seconds = int(context.get_remaining_time_in_millis() / 1000) - 8
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


for t in range(num_threads):
    thread = json.loads(json.dumps(sfn_thread).replace("{t}", str(t)))
    sfn["States"]["Threadpool"]["Branches"].append(thread)
    app.step_function_task(state_name="Worker{}".format(t), state_machine_definition=sfn)(do_work)

@app.step_function_task(state_name="Finalizer", state_machine_definition=sfn)
def finish_work(event, context):
    # The finalizer - the state after the "Parallel" (Threadpool) state - receives the parallel execution results as an
    # array. The finalizer can do things like aggregate results from the array and do any post-processing actions.
    return {"result": event}
