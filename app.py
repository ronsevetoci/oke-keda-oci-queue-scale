import os
import time
import oci
from prometheus_client import start_http_server, Gauge

# ====================
# 🔧 Configuration
# ====================
QUEUE_ID = os.environ.get("OCI_QUEUE_ID")
QUEUE_ENDPOINT = os.environ.get("OCI_QUEUE_ENDPOINT")
REGION = os.environ.get("OCI_REGION", "eu-frankfurt-1")
PORT = int(os.environ.get("EXPORTER_PORT", "8080"))

# ====================
# 📊 Prometheus Metrics
# ====================
QUEUE_LENGTH = Gauge(
    "oci_queue_length",
    "Total queue length (visible + in-flight)"
)

VISIBLE_MESSAGES = Gauge(
    "oci_queue_visible",
    "Visible messages in the queue"
)

IN_FLIGHT_MESSAGES = Gauge(
    "oci_queue_in_flight",
    "In-flight (processing) messages in the queue"
)

# ====================
# 🔐 OCI Auth & Client
# ====================
signer = oci.auth.signers.get_oke_workload_identity_resource_principal_signer()
config = {"region": REGION}
queue_client = oci.queue.QueueClient(config=config, signer=signer)
queue_client.base_client.endpoint = QUEUE_ENDPOINT

# ====================
# 📥 Metric Collection
# ====================
def collect_metrics():
    stats = queue_client.get_stats(queue_id=QUEUE_ID).data
    visible = stats.queue.visible_messages
    in_flight = stats.queue.in_flight_messages
    total = visible + in_flight

    QUEUE_LENGTH.set(total)
    VISIBLE_MESSAGES.set(visible)
    IN_FLIGHT_MESSAGES.set(in_flight)

# ====================
# 🚀 Main Entry Point
# ====================
if __name__ == "__main__":
    print(f"🚀 Starting OCI Queue Prometheus exporter on port {PORT}")
    start_http_server(PORT)

    while True:
        try:
            collect_metrics()
        except Exception as e:
            print(f"⚠️ Failed to collect metrics: {e}")
        time.sleep(15)  # Scrape interval