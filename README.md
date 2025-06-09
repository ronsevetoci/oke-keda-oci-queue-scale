# 📈 OCI Queue-Based HPA with KEDA on OKE

This project demonstrates how to build an **event-driven auto-scaling solution** using:

- 📬 **OCI Queue** for workload queuing  
- ⚖️ **KEDA (Kubernetes Event-Driven Autoscaler)** for horizontal pod autoscaling (HPA)  
- 🚀 **OKE (Oracle Kubernetes Engine)** as the Kubernetes platform

Optional - 
- 📊 **Prometheus** for custom metrics collection

The deployment will automatically scale based on the **number of messages in an OCI Queue**, enabling dynamic handling of load.

You can choose wheter or not to use Prometheus to gather the metric and use a Prometheus Keda scaledObject(manifests/scaledObject.yaml) which will digest the metric from Prometheus or digest the metric directly from a Keda scaledObject(manifests/scaledObject_noProm.yaml) directly from the exporter service without relying on Prometheus - i have set up two different scaledObjects manifests for this end - if your not using Prometheus you do not need to deploy the servicemonitor.yaml. 

---

## ✅ Prerequisites

Make sure you have the following ready before deploying:

1. ✅ An [OKE Cluster](https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengoverview.htm) up and running  
2. ✅ [KEDA installed](https://keda.sh/docs/2.9/deploy/#install) in the cluster  
3. ✅ An [OCI Queue](https://docs.oracle.com/en-us/iaas/Content/queue/queue-create.htm) configured  
4. ✅ Proper OCI IAM Policies in place (see [`IAM-Policy.txt`](./IAM-Policy.txt))

Optional - If using Prometheus - 

5. ✅ [Prometheus Helm Chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus) installed

---

## 🔐 IAM Policies

To allow your app (and the Prometheus exporter) to access the OCI Queue securely, this example uses:

- **Granular IAM permissions**
- **OCI Workload Identity**  
- **Kubernetes service account bindings**  

This approach avoids using broad access keys and provides safer, fine-grained access.

You can find a sample policy in [`IAM-Policy.txt`](./IAM-Policy.txt).

---

## 🧭 Architecture

The architecture below illustrates how metrics are collected from the OCI Queue and drive auto-scaling in the cluster:
![Architecture Diagram](./images/oke-oci-queue-keda.drawio.png)

---

## 📦 Components Overview

| Component            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `exporter.py`        | Python Prometheus exporter that pulls message stats from OCI Queue          |
| `ServiceMonitor`     | Scrapes the exporter metrics for Prometheus  (optional)                     |
| `Prometheus`         | In-cluster monitoring, collects metrics and exposes them to KEDA (optional) |
| `KEDA`               | Reads queue length metrics and adjusts replicas accordingly (via HPA)       |
| `scaledObject`       | Provides KEDA controller with link to metric source and sets scale params   |
| `HPA + Deployment`   | Your actual workload, scaled by KEDA based on queue depth                   |

---

## 🚀 Usage

## 🚀 Deployment Steps

This section outlines how to deploy the event-driven autoscaling solution using OCI Queue, Prometheus(optional), and KEDA on OKE.

### 📦 Deployment Steps

1. **Clone this repository**:

    ```bash
    git clone https://github.com/ronsevetoci/oke-keda-oci-queue-scale.git
    cd oke-keda-oci-queue-scale
    ```

2. **Update environment configurations of exporter deployment yaml**:

    - Edit `manifests/deploy.yaml`:
      - Set environment variables - 
        1. OCI_QUEUE_ID - you OCI queue OCID (the queue on which your scaling login will be based)
        2. OCI_QUEUE_ENDPOINT - you OCI queue endpoint address - "https://cell-1.queue.messaging..." # The endpoint of the queue
        3. OCI_REGION - your OCI queue region - default - eu-frankfurt-1
      
3. **Deploy the exporter deployment**:

    ```bash
    kubectl apply -f manifests/deploy.yaml
    ```

5. **Optional(when using Prometheus to digest the metric) Deploy the Prometheus ServiceMonitor**:

    ```bash
    kubectl apply -f servicemonitor.yaml
    ```

    > This will allow Prometheus to scrape metrics from the application and expose them to KEDA.


4. **Deploy the KEDA ScaledObject**:

    ***When using Prometheus -***
    ```bash
    kubectl apply -f manifests/scaledObject.yaml
    ```
    ***When digesting directly from KEDA without Prometheus -*** 
    ```bash
    kubectl apply -f manifests/scaledObject_noProm.yaml
    ```

---

### 🧪 Testing the Setup

1. **Deploy dummy application-**

    Our scaledObjects are set to scale a Kubernetes deployment called "dummy" (examples/dummy-deploy.yaml), it a simple echo server which will be used for the purpose of testing that our scaling actually works and that more replicas of the Deployment are actually created as we exceed our scaledObject message threshold of 2 messages.

     ```bash
    kubectl apply -f examples/dummy-deploy.yaml
    ```

2. **Send test messages to the queue**:

    You can add messages to the queue directly from the UI, CLI or via SDK, i've added a message example (examples/message.json) for testing purposes, you can use it via OCI CLI like so: (your CLI session must be authenticated to your OCI tenancy)
        oci queue message put \
    --queue-id <your-queue-ocid> \
    --messages file://message.json \
    --endpoint <your-queue-endpoint>

    You can also simply put messages in the queue via console.
   
3. **Monitor autoscaling behavior**:
    
    The current config in the scaledObject is (manifests/scaledObject*.yaml) - 
    If the queue length (the amount of messages in the OCI queue we reffered the exporter to check) is 0, the deployment will scale down to 0.
    If the queue length is 1, the deployment will stay at 0.
    Once it reaches 1, the app activates (min 1 replica).
    When it exceeds 2, scaling up begins toward max 10.

    Watch the pod scaling:

    ```bash
    kubectl get pods -w
    ```

    As messages increase in the queue, KEDA should trigger new pod creation. When the queue is drained, the pods should scale back down.

---

## 📜 License

MIT — see [`LICENSE`](./LICENSE)
