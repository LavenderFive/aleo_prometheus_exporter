# aleo_prometheus_exporter
Custom Prometheus Exporter for Aleo. Inspired by [DSVR's Aleo Exporter](https://github.com/dsrvlabs/aleo_exporter).

## Prerequisites
- Docker
- Docker Compose

## Metrics

- aleo_latest_height - the latest block height
- aleo_peer_count - the number of peers connected to the node
- aleo_coinbase_target - the coinbase target for latest block
- aleo_cumulative_proof_target - the cumulative proof target for latest block
- aleo_cumulative_weight - the cumulative weight for latest block
- aleo_last_coinbase_target - the coinbase target for the last coinbase
- aleo_last_coinbase_timestamp - the unix timestamp(UTC) for the last coinbase
- aleo_latest_round - the round that produced latest block
- aleo_network_id - the network ID of the latest block
- aleo_proof_target - the proof target for latest block
- aleo_timestamp - the unix timestamp(UTC) for latest block

## Setup
1. Clone this repository:
```sh
git clone https://github.com/yourusername/aleo_prometheus_exporter.git
cd peggo_prometheus_exporter
```

2. Copy the a .env.sample file and fill in the variables.
```sh
mv .env.sample .env
```

Running the Exporter
1. Build and start the Docker services:
```sh
docker-compose up -d
```
2. The Prometheus Exporter should now be running on the specified HTTP_PORT.
```sh
curl localhost:9911
```