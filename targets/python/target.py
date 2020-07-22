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

import json
import logging
from datetime import datetime, timezone
import uuid

from cloudevents.sdk import converters
from cloudevents.sdk import marshaller
from cloudevents.sdk.converters import structured, binary
from cloudevents.sdk.event import v1

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def target():
	
    # Deserialize the HTTP request into a CloudEvent
    try:
    	logging.info('Deserializing CloudEvent in binary format')
    	# Instantiate the Binary Format marshaller
        mb = marshaller.NewHTTPMarshaller([binary.NewBinaryHTTPCloudEventConverter()])
        ce = mb.FromRequest(v1.Event(), request.headers, request.stream.read(), lambda x: x)
    except:
        logging.warning('Deserializing application/cloudevents+json CloudEvent')
        # Instantiate the JSON Structured CloudEvent marshaller
        m = marshaller.NewHTTPMarshaller([structured.NewJSONHTTPCloudEventConverter()])
        ce = m.FromRequest()
    except:
    	logging.warning('Could not deserialize CloudEvent')
    	    # Create a CloudEvent to send as response
        data = 'Data received was not understandable as a CloudEvent'
        event = (
            v1.Event()
            .SetContentType("application/json")
            .SetData(data)
            .SetEventID(str(uuid.uuid1()))
            .SetSource("from_your_own_target")
            .SetSubject("your_event_subject")
            .SetEventTime(datetime.now(timezone.utc).astimezone().isoformat())
            .SetEventType("io.triggermesh.target.byown")
        )
        return app.response_class(
                response=body,
                headers=headers,
                status=400
        )

    # Do your Transformation or Target work based on the eventype
    if ce.EventType() == "io.triggermesh.byown.create":
        logging.info("Create EventType")
    elif ce.EventType() == "io.triggermesh.byown.delete":
        logging.info("Delete EventType")
    else:
        logging.warning("Unknown EventType")

    # Create a CloudEvent to send as response
    data = 'this is some data'
    event = (
        v1.Event()
        .SetContentType("application/json")
        .SetData(data)
        .SetEventID(str(uuid.uuid1()))
        .SetSource("from_your_own_target")
        .SetSubject("your_event_subject")
        .SetEventTime(datetime.now(timezone.utc).astimezone().isoformat())
        .SetEventType("io.triggermesh.target.byown")
    )

    # Prepare the Header and Body to send a request back as a CloudEvent
    m = marshaller.NewHTTPMarshaller([structured.NewJSONHTTPCloudEventConverter()])
    headers, body = m.ToRequest(event, converters.TypeStructured, lambda x: x)

    return app.response_class(
            response=body,
            headers=headers,
            status=200
    )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
