#!/usr/bin/env python3
#
# Copyright 2020 TriggerMesh Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from datetime import datetime, timezone

from cloudevents.sdk import converters
from cloudevents.sdk import marshaller
from cloudevents.sdk.converters import structured, binary
from cloudevents.sdk.event import v1

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def target():
    mb = marshaller.NewHTTPMarshaller([binary.NewBinaryHTTPCloudEventConverter()])

    # Deserialize the HTTP request into a CloudEvent
    ce = mb.FromRequest(v1.Event(), request.headers, request.stream.read(), lambda x: x)
    
    # Do your Transformation or Target work based on the eventype
    if ce.EventType() == "com.triggermesh.create":
        print("Create EventType")
    elif ce.EventType() == "com.triggermesh.delete":
        print("Delete EventType")
    else:
        print("Unknown EventType")

    # Create a CloudEvent to send as response
    data = 'this is some data'
    event = (
        v1.Event()
        .SetContentType("application/json")
        .SetData(data)
        .SetEventID("my-id")
        .SetSource("from-galaxy-far-far-away")
        .SetSubject("foobar")
        .SetEventTime(datetime.now(timezone.utc).astimezone().isoformat())
        .SetEventType("com.triggermesh.transform")
    )

    m = marshaller.NewHTTPMarshaller([structured.NewJSONHTTPCloudEventConverter()])
    headers, body = m.ToRequest(event, converters.TypeStructured, lambda x: x)

    return app.response_class(
            response=body,
            headers=headers,
            status=200
    )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
