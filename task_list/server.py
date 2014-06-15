# No shebang line, this module is meant to be imported
#
# Copyright 2014 Oliver Palmer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import uuid
from datetime import datetime, timedelta
from functools import partial
from json import dumps as _dumps
from random import randint

from flask import Flask, render_template
from flask.views import MethodView

JOB = None
TASKS = {}  # {jobid {taskid: (start, end)}}
MIN_TASKS = 5
MAX_TASKS = 15
MIN_START_TIME = 1
MAX_START_TIME = 10
MIN_COMPLETION_TIME = 3
MAX_COMPLETION_TIME = 15


def default_json_dumper(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return str(obj)

dumps = partial(_dumps, default=default_json_dumper)
app = Flask("")


def create_tasks():
    global JOB
    JOB = uuid.uuid4()
    now = datetime.utcnow()
    tasks = TASKS[JOB] = {}
    for i in range(randint(MIN_TASKS, MAX_TASKS)):
        end_time = now + timedelta(
            seconds=randint(MIN_COMPLETION_TIME, MAX_COMPLETION_TIME))
        start_time = end_time - timedelta(
            seconds=randint(MIN_START_TIME, MAX_START_TIME))
        tasks[i] = (start_time, end_time)


class View(MethodView):
    def get(self):
        if not TASKS:
            create_tasks()

        tasks = {}
        now = datetime.utcnow()
        for task_id, (start_time, end_time) in TASKS[JOB].items():
            if now <= start_time:
                tasks[task_id] = "waiting"
            elif now > end_time:
                tasks[task_id] = "done"
            else:
                tasks[task_id] = "running"

        return dumps({"job": JOB, "tasks": tasks})

    def delete(self):
        create_tasks()
        return ""

# TODO: create /api/v1/tasks/<id>
app.add_url_rule("/api/v1/tasks/", view_func=View.as_view("tasks"))


@app.route("/")
def index():
    return render_template("index.html")


app.run(debug=True)