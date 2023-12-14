# peggo_prometheus_exporter
Custom Prometheus Exporter for Injective's Peggo bridge.

## Prerequisites
- Docker
- Docker Compose

## Setup
1. Clone this repository:
```sh
git clone https://github.com/yourusername/peggo_prometheus_exporter.git
```

2. Navigate to the project directory:
```sh
cd peggo_prometheus_exporter
```

3. Copy the a .env.sample file and fill in the variables.
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
curl localhost:9910
```