# Sample event target - Go

This sample event target uses the [Go SDK for CloudEvents][ce-gosdk] to expose a HTTP endpoint that listens to incoming
CloudEvents.

It accepts events with any [`type`][ce-type] attribute, and responds to every incoming event with another CloudEvent
similar to the example below, where the extensions `processedtype`, `processedsource`, and `processedid` contain the
value of the `type`, `source` and `id` context attributes of the processed event, respectively:

```
Context Attributes,
  specversion: 1.0
  type: com.example.target.ack
  source: io.triggermesh.targets.go-sample
  id: 40527f73-e4f5-4259-aff5-5e0abb01ee9b
  time: 2020-10-05T17:20:45.6983239Z
  datacontenttype: application/json
Extensions,
  processedid: 79cb1721-05aa-44e5-ad27-95c4d4d62df8
  processedsource: /apis/v1/namespaces/my-namespace/pingsources/my-ping
  processedtype: dev.knative.sources.ping
Data,
  {
    "code": 0,
    "detail": {
      "message": "event processed successfully",
      "processing_time_ms": 62
    }
  }
```

## Try it

To run this event target locally, make sure you have the [Go][go] toolchain installed, then execute the command below in
the current directory. This will download the modules required by the program, compile a temporary binary, and run it in
the foreground:

```console
$ go run .
go: downloading github.com/sethvargo/go-signalcontext v0.1.0
go: downloading github.com/cloudevents/sdk-go/v2 v2.3.1
go: downloading go.opencensus.io v0.22.0
go: downloading go.uber.org/zap v1.10.0
go: downloading github.com/google/uuid v1.1.1
go: downloading github.com/lightstep/tracecontext.go v0.0.0-20181129014701-1757c391b1ac
go: downloading go.uber.org/atomic v1.4.0
go: downloading go.uber.org/multierr v1.1.0
go: downloading github.com/hashicorp/golang-lru v0.5.3
2020/10/05 17:20:08 Running CloudEvents handler
```

The CloudEvents HTTP receiver listens on TCP port 8080 and exposes a single HTTP route at `/`:

```console
$ ss -tlpn
State    Recv-Q   Send-Q   Local Address:Port   Peer Address:Port   Process
LISTEN   0        128                  *:8080              *:*       users:(("go",pid=3398,fd=6))
```

You can now send a CloudEvent to this HTTP endpoint using either [the binary or structured content
mode][ce-http-mapping], and confirm that it responds with the acknowledgement demonstrated in the introduction.

We use the [`curl`][curl] command in the example below, but you could replicate this example using any other tool such
as [Postman][postman]:

```
$ curl -D- http://localhost:8080/ \
    -H 'Content-Type: application/json' \
    -H 'Ce-Specversion: 1.0' \
    -H 'Ce-Type: greeting' \
    -H 'Ce-Source: my-workstation' \
    -H 'Ce-Id: 0000' \
    -d '{ "msg": "Hello, TriggerMesh!" }'
```
```http
HTTP/1.1 200 OK
Ce-Id: 92d87aa3-2ed5-4a3b-b389-81a726bc852a
Ce-Processedid: 0000
Ce-Processedsource: my-workstation
Ce-Processedtype: greeting
Ce-Source: io.triggermesh.targets.go-sample
Ce-Specversion: 1.0
Ce-Time: 2020-10-05T17:20:44.4758642Z
Ce-Type: com.example.target.ack
Content-Length: 86
Content-Type: application/json
Date: Tue, 05 Oct 2020 17:20:44 GMT

{"code":0,"detail":{"message":"event processed successfully","processing_time_ms":62}}
```


[ce-gosdk]: https://github.com/cloudevents/sdk-go
[ce-type]: https://github.com/cloudevents/spec/blob/v1.0/spec.md#type
[ce-http-mapping]: https://github.com/cloudevents/spec/blob/v1.0/http-protocol-binding.md#3-http-message-mapping

[go]: https://golang.org/
[curl]: https://curl.haxx.se/
[postman]: https://www.postman.com/downloads/
