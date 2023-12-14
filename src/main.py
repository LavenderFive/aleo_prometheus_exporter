import os
import requests
import time

from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge

load_dotenv()
NODE_URL = os.getenv("NODE_URL")
ORCHESTRATOR_ADDR = os.getenv("ORCHESTRATOR_ADDRESS")
POLL_SECONDS = int(os.getenv("POLL_SECONDS"))
HTTP_PORT = int(os.getenv("HTTP_PORT"))

# Define a Gauge metric to track peggo event lag
PEGGO_EVENT_LAG = Gauge("peggo_event_lag", "Peggo event lag", ["orchestrator_address"])
PEGGO_NETWORK_NONCE = Gauge("peggo_network_nonce", "Injective network current peggo nonce", ["orchestrator_address"])
PEGGO_ORCHESTRATOR_NONCE = Gauge("peggo_orchestrator_nonce", "Peggo orchestrator nonce", ["orchestrator_address"])


def process_request():
    r = requests.get(f"{NODE_URL}/peggy/v1/module_state")
    network_nonce = int(r.json()["state"]["last_observed_nonce"])

    r = requests.get(f"{NODE_URL}/peggy/v1/oracle/event/{ORCHESTRATOR_ADDR}")
    orchestrator_nonce = int(r.json()["last_claim_event"]["ethereum_event_nonce"])

    event_lag = network_nonce - orchestrator_nonce

    PEGGO_EVENT_LAG.labels(ORCHESTRATOR_ADDR).set(event_lag)
    PEGGO_NETWORK_NONCE.labels(ORCHESTRATOR_ADDR).set(network_nonce)
    PEGGO_ORCHESTRATOR_NONCE.labels(ORCHESTRATOR_ADDR).set(orchestrator_nonce)


def main():
    start_http_server(HTTP_PORT)

    while True:
        process_request()
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    print(f"Polling {NODE_URL} every {POLL_SECONDS} seconds")
    print(f"On port {HTTP_PORT}")
    print(f"Orchestator {ORCHESTRATOR_ADDR}")

    main()
