# Sample Source in Python

This is a sample source written in Python, it needs to:

* Emit CloudEvents
* Send CloudEvents to the URL defined by the K_SINK environment variable

To achieve this we use the [Python CloudEvent SDK](https://github.com/cloudevents/sdk-python) and the python `requests` module.
To showcase this we do a source for Google Cloud Storage

## Configure Google Cloud Storage Notification

Create a bucket `bridgedemo`
Create a notification for bucket events
Create a subscription for the topic used to publish the notifications

```
gsutil notification create -t tmdemo -f json gs://bridgedemo
gsutil notification list gs://bridgedemo
gcloud pubsub subscriptions create bridgedemosub --topic tmdemo
```

# Build the Event Source Container

```
docker build -t gcr.io/triggermesh/googlecloudstorage .
```

# Deploy via a Deployment and a Sink Binding

The source as a deployment and a sink binding

```
kubectl apply -f d.yaml
kubectl apply -f sinkb.yaml
```
