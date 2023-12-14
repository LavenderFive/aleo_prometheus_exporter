import json
import math
import os
from urllib.parse import urljoin
import requests
import time
from munch import munchify
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge

load_dotenv()
NODE_URL = os.getenv("NODE_URL")
NETWORK_ID = os.getenv("NETWORK_ID")
POLL_SECONDS = int(os.getenv("POLL_SECONDS"))
HTTP_PORT = int(os.getenv("HTTP_PORT"))

# Define a Gauge metric to track peggo event lag
ALEO_LATEST_HEIGHT = Gauge("aleo_latest_height", "the latest block height")
ALEO_PEER_COUNT = Gauge("aleo_peer_count", "the number of peers connected to the node")
ALEO_COINBASE_TARGET = Gauge("aleo_coinbase_target", "the coinbase target for latest block")
ALEO_CUMULATIVE_PROOF_TARGET = Gauge("aleo_cumulative_proof_target", "the cumulative proof target for latest block")
ALEO_CUMULATIVE_WEIGHT = Gauge("aleo_cumulative_weight", "the cumulative weight for latest block")
ALEO_LAST_COINBASE_TARGET = Gauge("aleo_last_coinbase_target", "the coinbase target for the last coinbase")
ALEO_LAST_COINBASE_TIMESTAMP = Gauge("aleo_last_coinbase_timestamp", "the unix timestamp(UTC) for the last coinbase")
ALEO_LATEST_ROUND = Gauge("aleo_latest_round", "the round that produced latest block")
ALEO_NETWORK_ID = Gauge("aleo_network_id", "the network ID of the latest block")
ALEO_PROOF_TARGET = Gauge("aleo_proof_target", "the proof target for latest block")
ALEO_TIMESTAMP = Gauge("aleo_timestamp", "the unix timestamp(UTC) for latest block")


def request(url: str, endpoint: str):
    r = requests.get(f"{url}/{endpoint}")
    if r.status_code != 200:
        return math.nan
    return r.content


def process_request(node_url: str):

    latest_height = int(request(node_url, "latest/height"))
    ALEO_LATEST_HEIGHT.set(latest_height)
    
    peer_count = int(request(node_url, "peers/count"))
    ALEO_PEER_COUNT.set(peer_count)
    
    latest_block_response = json.loads(request(node_url, "latest/block"))
    if latest_block_response is math.nan:
        ALEO_COINBASE_TARGET.set(latest_block_response)
        ALEO_CUMULATIVE_PROOF_TARGET.set(latest_block_response)
        ALEO_CUMULATIVE_WEIGHT.set(latest_block_response)
        ALEO_LAST_COINBASE_TARGET.set(latest_block_response)
        ALEO_LAST_COINBASE_TIMESTAMP.set(latest_block_response)
        ALEO_LATEST_ROUND.set(latest_block_response)
        ALEO_NETWORK_ID.set(latest_block_response)
        ALEO_PROOF_TARGET.set(latest_block_response)
        ALEO_TIMESTAMP.set(latest_block_response)
    else: 
        munched = munchify(latest_block_response)
        metadata = munched.header.metadata

        ALEO_COINBASE_TARGET.set(int(metadata.coinbase_target))
        ALEO_CUMULATIVE_PROOF_TARGET.set(int(metadata.cumulative_proof_target))
        ALEO_CUMULATIVE_WEIGHT.set(int(metadata.cumulative_weight))
        ALEO_LAST_COINBASE_TARGET.set(int(metadata.last_coinbase_target))
        ALEO_LAST_COINBASE_TIMESTAMP.set(int(metadata.last_coinbase_timestamp))
        ALEO_LATEST_ROUND.set(int(metadata.round))
        ALEO_NETWORK_ID.set(int(metadata.network))
        ALEO_PROOF_TARGET.set(int(metadata.proof_target))
        ALEO_TIMESTAMP.set(int(metadata.timestamp))


def main():
    start_http_server(HTTP_PORT)

    node_url = urljoin(NODE_URL, NETWORK_ID)
    while True:
        process_request(node_url)
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    print(f"Polling {NODE_URL} every {POLL_SECONDS} seconds")
    print(f"On port {HTTP_PORT}")

    main()
