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

_Coming soon: deployment steps, Helm templates, and `kubectl` instructions to deploy this stack easily._

---

## 📜 License

MIT — see [`LICENSE`](./LICENSE)
