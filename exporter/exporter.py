import os
import time
import threading
import oci
from prometheus_client import start_http_server, Gauge

# === 🔧 Config ===
QUEUE_ID = os.environ.get("OCI_QUEUE_ID")
QUEUE_ENDPOINT = os.environ.get("OCI_QUEUE_ENDPOINT")
REGION = os.environ.get("OCI_REGION", "eu-frankfurt-1")
PORT = int(os.environ.get("EXPORTER_PORT", "8080"))
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "15"))

# === 📊 Prometheus Metrics ===
QUEUE_LENGTH = Gauge("oci_queue_length", "Total queue length (visible + in-flight)")
VISIBLE_MESSAGES = Gauge("oci_queue_visible", "Visible messages in the queue")
IN_FLIGHT_MESSAGES = Gauge("oci_queue_in_flight", "In-flight (processing) messages in the queue")

# === 🔐 OCI Auth & Client ===
signer = oci.auth.signers.get_oke_workload_identity_resource_principal_signer()
config = {"region": REGION}
queue_client = oci.queue.QueueClient(config=config, signer=signer)
queue_client.base_client.endpoint = QUEUE_ENDPOINT

# === 🧠 State ===
last_visible = 0
last_in_flight = 0

# === 🔁 Background Metric Collector ===
def poll_metrics():
    global last_visible, last_in_flight
    while True:
        try:
            stats = queue_client.get_stats(queue_id=QUEUE_ID).data
            visible = stats.queue.visible_messages
            in_flight = stats.queue.in_flight_messages
            total = visible + in_flight

            # Update Prometheus metrics
            QUEUE_LENGTH.set(total)
            VISIBLE_MESSAGES.set(visible)
            IN_FLIGHT_MESSAGES.set(in_flight)

            # Store state in case it's needed
            last_visible = visible
            last_in_flight = in_flight

        except Exception as e:
            print(f"⚠️ Error polling metrics from OCI: {e}")

        time.sleep(POLL_INTERVAL)

# === 🚀 Entry Point ===
if __name__ == "__main__":
    print(f"🚀 Starting OCI Queue Exporter on port {PORT} (polling every {POLL_INTERVAL}s)")

    # Start HTTP server for Prometheus
    start_http_server(PORT)

    # Start background polling thread
    t = threading.Thread(target=poll_metrics, daemon=True)
    t.start()

    # Block forever
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("🛑 Shutting down.")