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
from cloudevents.sdk.converters import structured
from cloudevents.sdk.event import v1

from google.cloud import pubsub_v1

import requests

subscriber = pubsub_v1.SubscriberClient()

subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    sub=os.getenv('MY_SUBSCRIPTION_NAME'),
)

K_SINK = os.getenv('K_SINK')

m = marshaller.NewHTTPMarshaller([structured.NewJSONHTTPCloudEventConverter()])

def run_structured(event, url):
    structured_headers, structured_data = m.ToRequest(
        event, converters.TypeStructured, json.dumps
    )
    print("structured CloudEvent")
    print(structured_data.getvalue())

    response = requests.post(url,
                             headers=structured_headers,
                             data=structured_data.getvalue())
    response.raise_for_status()

def callback(message):
    local_time = datetime.now(timezone.utc).astimezone()
    event = (
        v1.Event()
        .SetContentType("application/json")
        .SetData(json.loads(message.data.decode()))
        .SetEventID("my-id")
        .SetSource("from-galaxy-far-far-away")
        .SetEventTime(local_time.isoformat())
        .SetEventType("com.google.cloudstorage")
        .SetExtensions("")
    )

    res = run_structured(event, K_SINK)
    message.ack()

future = subscriber.subscribe(subscription_name, callback)

try:
    future.result()
except KeyboardInterrupt:
    future.cancel()




