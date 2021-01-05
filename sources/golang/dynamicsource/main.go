/*
Copyright (c) 2019-2020 TriggerMesh Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"time"

	cloudevents "github.com/cloudevents/sdk-go/v2"
)

const EventType = "EVENT_TYPE"
const EventSource = "EVENT_SOURCE"
const EventSubject = "EVENT_SUBJECT"
const EventID = "EVENT_ID"
const Payload = "PAYLOAD"
const Timeout = "TIMEOUT"
const Sink = "SINK"

// adapter implements the source's adapter.
type adapter struct {
	EventType    string
	EventSubject string
	EventSource  string
	EventID      string
	Payload      string
	Timeout      string
	Sink         string
	ceClient     cloudevents.Client
}

func main() {

	c, err := cloudevents.NewDefaultClient()
	if err != nil {
		fmt.Printf("failed to create client, %v", err)
	}

	a := &adapter{
		EventType:    os.Getenv(EventType),
		EventSource:  os.Getenv(EventSource),
		EventSubject: os.Getenv(EventSubject),
		EventID:      os.Getenv(EventID),
		Payload:      os.Getenv(Payload),
		Timeout:      os.Getenv(Timeout),
		Sink:         os.Getenv(Sink),
		ceClient:     c,
	}
	dur, err := time.ParseDuration(a.Timeout)
	if err != nil {

	}

	fmt.Println("Begining to emit specified Cloudevent..")
	for ok := true; ok; ok = (err == nil) {
		err = a.sendCloudEvent()
		if err != nil {
			fmt.Println("got error: %w", err)
		}

		time.Sleep(dur)
	}

}

func (a *adapter) sendCloudEvent() error {
	fmt.Println("Sending Event... ")
	c, err := cloudevents.NewDefaultClient()
	if err != nil {
		fmt.Printf("failed to create client, %v", err)
	}

	// Create an Event.
	event := cloudevents.NewEvent()
	event.SetSubject(a.EventSubject)
	event.SetType(a.EventType)
	event.SetSource(a.EventSource)
	event.SetID(a.EventID)

	if a.Payload == "" {
		event.SetData(cloudevents.ApplicationJSON, map[string]string{"hello": "world"})
	}
	if a.Payload != "" {
		json, err := json.Marshal(a.Payload)
		if err != nil {
			fmt.Println("Got an error marshaling payload data.")
		}
		event.SetData(cloudevents.ApplicationJSON, json)
	}

	//cant get the normal way working right now :/
	ctx := cloudevents.ContextWithTarget(context.Background(), a.Sink)

	if result := c.Send(ctx, event); cloudevents.IsUndelivered(result) {
		fmt.Printf("failed to send, %v", result)
		return result
	}
	return nil
}
