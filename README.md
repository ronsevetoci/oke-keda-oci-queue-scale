# Example of OCI Queue queue size based HPA using Keda

In this example i will demonstrate how to use Keda and Prometheus to scale a Kubernetes deployment based on the size of an OCI queue,
This enables event drivven apps to scale horizontally based on the amount of load in the queue on OCI queue.

## Prerequeisties
1. OKE cluster up and running
2. Prometheus - https://github.com/prometheus-community/helm-charts/tree/main/charts/prometheus
3. Keda - https://keda.sh/docs/2.9/deploy/#install
4. OCI Queue - https://docs.oracle.com/en-us/iaas/Content/queue/queue-create.htm
5. IAM Policies - See the example policy - IAM-Policy.txt

### IAM Policies
We must have IAM policies in-place to allow our servicemonitor code to access the queue, in our example if are using workload identity bound to a Kubernetes service account to ensure granular access which is the safest approach.

### Architecture 

![Architecture Diagram](./images/oke-oci-queue-keda.drawio.png)
