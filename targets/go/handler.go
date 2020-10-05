/*
Copyright (c) 2020 TriggerMesh Inc.

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
	"log"
	"math/rand"
	"time"

	cloudevents "github.com/cloudevents/sdk-go/v2"
)

const (
	eventTypeAck = "com.example.target.ack"

	eventSrcName = "io.triggermesh.targets.go-sample"

	ceExtProcessedType   = "processedtype"
	ceExtProcessedID     = "processedid"
	ceExtProcessedSource = "processedsource"
)

// Handler runs a CloudEvents receiver.
type Handler struct {
	cli cloudevents.Client
}

// NewHandler returns a new Handler for the given CloudEvents client.
func NewHandler(c cloudevents.Client) *Handler {
	rand.Seed(time.Now().UnixNano())

	return &Handler{
		cli: c,
	}
}

// Run starts the handler and blocks until it returns.
func (h *Handler) Run(ctx context.Context) error {
	return h.cli.StartReceiver(ctx, h.receive)
}

// ACKResponse represents the data of a CloudEvent payload returned to
// acknowledge the processing of an event.
type ACKResponse struct {
	Code   ACKCode     `json:"code"`
	Detail interface{} `json:"detail"`
}

// ACKCode defines the outcome of the processing of an event.
type ACKCode int

// Enum of supported ACK codes.
const (
	CodeSuccess ACKCode = iota // 0
	CodeFailure                // 1
)

// receive implements the handler's receive logic.
func (h *Handler) receive(e cloudevents.Event) (*cloudevents.Event, cloudevents.Result) {
	code := CodeSuccess
	ceResult := cloudevents.ResultACK

	result, err := processEvent(e)
	// this error handling is for demo purposes only, since processEvent()
	// always succeeds
	if err != nil {
		code = CodeFailure
		ceResult = cloudevents.ResultNACK
	}

	return newAckEvent(e, code, result), ceResult
}

// processEvent processes the event and returns the result of the processing.
func processEvent(e cloudevents.Event) (interface{} /*result*/, error) {
	tBegin := time.Now()

	randomDelay()

	res := &dummyResult{
		Message:        "event processed successfully",
		ProcessingTime: time.Since(tBegin).Milliseconds(),
	}

	return res, nil
}

// dummyResult represents a fictional structured result of some event
// processing.
type dummyResult struct {
	Message        string `json:"message"`
	ProcessingTime int64  `json:"processing_time_ms"`
}

// newAckEvent returns a CloudEvent that acknowledges the processing of an
// event.
func newAckEvent(e cloudevents.Event, code ACKCode, detail interface{}) *cloudevents.Event {
	resp := cloudevents.NewEvent()
	resp.SetType(eventTypeAck)
	resp.SetSource(eventSrcName)
	resp.SetExtension(ceExtProcessedType, e.Type())
	resp.SetExtension(ceExtProcessedSource, e.Source())
	resp.SetExtension(ceExtProcessedID, e.ID())

	data := &ACKResponse{
		Code:   code,
		Detail: detail,
	}

	if err := resp.SetData(cloudevents.ApplicationJSON, data); err != nil {
		log.Panicf("Error serializing CloudEvent data: %s", err)
	}

	return &resp
}

// randomDelay sleeps for a random amount of time.
func randomDelay() {
	const maxDelay = 100 * time.Millisecond

	randomDelay := time.Duration(rand.Int63n(int64(maxDelay)))
	time.Sleep(randomDelay)
}
