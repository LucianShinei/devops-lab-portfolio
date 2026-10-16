# Exercise 05: Docker Compose - Flask, Redis and MySQL

## Objective

Run a Flask API, Redis and MySQL together using Docker Compose, with service health checks and persistent storage.

## Architecture

- **Flask:** exposes the HTTP API on host port 5002.
- **Redis:** stores an incrementing page visit counter.
- **MySQL:** stores individual visit records in a database table.
- **Docker Compose:** manages services, networking, dependencies and volumes.

Compose provides service-name DNS, so Flask connects to Redis using `redis` and MySQL using `mysql`.

## Files

| File | Purpose |
|---|---|
| `app.py` | Flask endpoints and database operations |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Builds the Flask application image |
| `compose.yaml` | Defines services, health checks, networking and volumes |

## Prerequisites

- Docker Desktop
- Docker Compose

## Run the application

```powershell
docker compose config
docker compose up -d --build
docker compose ps
```

Open `http://localhost:5002/` or test it from PowerShell:

```powershell
Invoke-RestMethod http://localhost:5002/health
Invoke-RestMethod http://localhost:5002/
```

## API endpoints

| Endpoint | Purpose |
|---|---|
| `GET /health` | Returns the application health status |
| `GET /` | Increments the Redis counter and records a visit in MySQL |

A successful request to `/` returns a message, `redis_visit_count` and `mysql_total_visits`.

## Persistence

The Compose configuration declares two named volumes:

- `redis_data` stores Redis data, with Redis append-only persistence enabled.
- `mysql_data` stores MySQL database files.

To verify persistence, make requests to `/`, then recreate the containers:

```powershell
docker compose down
docker compose up -d
docker compose ps
Invoke-RestMethod http://localhost:5002/
```

Do not use `docker compose down -v` for this test, because it removes the Compose-managed volumes.

## Verified results

- The Flask health endpoint returned `healthy`.
- Redis and MySQL both recorded the first and second visits.
- After container recreation, both counters continued from 2 to 3.
- Redis and MySQL passed their configured health checks.

## Useful commands

```powershell
docker compose logs --tail 40
docker compose logs -f
docker compose ps
docker compose down
```

## Security note

The database credentials in this exercise are for local learning only. Use secrets or an appropriate secure configuration for real deployments.
