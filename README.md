# 📈 OCI Queue-Based HPA with KEDA on OKE

This project demonstrates how to build an **event-driven auto-scaling solution** using:

- 📬 **OCI Queue** for workload queuing  
- 📊 **Prometheus** for custom metrics collection  
- ⚖️ **KEDA (Kubernetes Event-Driven Autoscaler)** for horizontal pod autoscaling (HPA)  
- 🚀 **OKE (Oracle Kubernetes Engine)** as the Kubernetes platform

The deployment will automatically scale based on the **number of messages in an OCI Queue**, enabling dynamic handling of load.

---

## ✅ Prerequisites

Make sure you have the following ready before deploying:

1. ✅ An [OKE Cluster](https://docs.oracle.com/en-us/iaas/Content/ContEng/Concepts/contengoverview.htm) up and running  
2. ✅ [Prometheus Helm Chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus) installed  
3. ✅ [KEDA installed](https://keda.sh/docs/2.9/deploy/#install) in the cluster  
4. ✅ An [OCI Queue](https://docs.oracle.com/en-us/iaas/Content/queue/queue-create.htm) configured  
5. ✅ Proper OCI IAM Policies in place (see [`IAM-Policy.txt`](./IAM-Policy.txt))

---

## 🔐 IAM Policies

To allow your app (and the Prometheus exporter) to access the OCI Queue securely, this example uses:

- **OCI Workload Identity**  
- **Kubernetes service account bindings**  
- **Granular IAM permissions**

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
| `App.py`             | Python Prometheus exporter that pulls message stats from OCI Queue          |
| `ServiceMonitor`     | Scrapes the exporter metrics for Prometheus                                 |
| `Prometheus`         | In-cluster monitoring, collects metrics and exposes them to KEDA            |
| `KEDA`               | Reads queue length metrics and adjusts replicas accordingly (via HPA)       |
| `HPA + Deployment`   | Your actual workload, scaled by KEDA based on queue depth                   |

---

## 🚀 Usage

## 🚀 Deployment Steps

This section outlines how to deploy the event-driven autoscaling solution using OCI Queue, Prometheus, and KEDA on OKE.

### ✅ Prerequisites

Make sure the following are ready:

- An operational **OKE (Oracle Kubernetes Engine)** cluster.
- An **OCI Queue** created and ready to receive messages.
- **IAM Policies** allowing access to OCI Queue and related resources.
- **Prometheus** installed on your OKE cluster (for metrics collection).
- **KEDA** installed on your OKE cluster (for event-driven scaling).

> ℹ️ [Install KEDA guide](https://keda.sh/docs/2.14/concepts/scaling-deployments/)

---

### 📦 Deployment Steps

1. **Clone this repository**:

    ```bash
    git clone https://github.com/ronsevetoci/oke-keda-oci-queue-scale.git
    cd oke-keda-oci-queue-scale
    ```

2. **Update environment configurations**:

    - Edit `deploy.yaml`:
      - Replace the placeholders with your OCI Queue **OCID** and **Region**.
      - Adjust any other environment variables as needed.

3. **Deploy the application**:

    ```bash
    kubectl apply -f deploy.yaml
    ```

4. **Deploy the KEDA ScaledObject**:

    ```bash
    kubectl apply -f scaledObject.yaml
    ```

    > Ensure the `scaledObject.yaml` references the correct queue metrics and scaling parameters.

5. **Deploy the Prometheus ServiceMonitor**:

    ```bash
    kubectl apply -f servicemonitor.yaml
    ```

    > This will allow Prometheus to scrape metrics from the application.

---

### 🧪 Testing the Setup

1. **Send test messages to the queue**:

    You can add messages to the queue directly from the UI, CLI or via SDK.
   
3. **Monitor autoscaling behavior**:

    Watch the pod scaling:

    ```bash
    kubectl get pods -w
    ```

    As messages increase in the queue, KEDA should trigger new pod creation. When the queue is drained, the pods should scale back down.

---

### 🧹 Cleanup

To remove all deployed resources:

```bash
kubectl delete -f servicemonitor.yaml
kubectl delete -f scaledObject.yaml
kubectl delete -f deploy.yaml

---

## 📜 License

MIT — see [`LICENSE`](./LICENSE)
