\# CIE Question 6 – Retail Analytics Stack



A containerised retail analytics application built using Flask, MySQL, Redis and Docker Compose, with Prometheus and Grafana for monitoring and AppArmor for security testing.



\## 1. Project Overview



The project demonstrates a multi-container retail analytics system with isolated services, database integration, Redis caching, container monitoring, security enforcement and fault diagnosis.



\### Architecture



```text

&#x20;                   Flask REST API

&#x20;                    Port 5001

&#x20;                        |

&#x20;                Docker Bridge Network

&#x20;                    retail-net

&#x20;                  /      |      \\

&#x20;               MySQL    Redis   Flask

&#x20;               3306     6379    5000

&#x20;                        

&#x20;                 Monitoring Stack

&#x20;                        

&#x20;            cAdvisor → Prometheus → Grafana

&#x20;                         9090       3000

```



\## 2. Technology Stack



\- \*\*Python and Flask:\*\* REST API and application logic.

\- \*\*MySQL 8.4:\*\* Relational database for retail sales records.

\- \*\*Redis 7:\*\* In-memory caching for sales statistics.

\- \*\*Docker:\*\* Containerisation.

\- \*\*Docker Compose:\*\* Multi-container orchestration.

\- \*\*Prometheus:\*\* Metrics collection and storage.

\- \*\*cAdvisor:\*\* Container resource monitoring.

\- \*\*Grafana:\*\* Monitoring dashboards and visualisation.

\- \*\*AppArmor:\*\* Mandatory access control and security testing.



\## 3. Services and Ports



| Service | Host Port | Container Port |

|---|---:|---:|

| Flask | 5001 | 5000 |

| MySQL | Not published | 3306 |

| Redis | Not published | 6379 |

| Prometheus | 9091 | 9090 |

| Grafana | 3001 | 3000 |

| cAdvisor | Internal only | 8080 |



All application services communicate through the custom Docker bridge network `retail-net`.



MySQL and Redis ports are not published to the host. They are accessible internally by the other containers through the Docker network.



\## 4. Setup and Execution



Run the following commands from this directory using Docker Desktop:



```powershell

docker context use desktop-linux

docker compose up -d --build

docker compose ps

```



View application logs:



```powershell

docker compose logs -f app

```



Check the status of all services:



```powershell

docker compose ps

```



\## 5. Flask API Endpoints



Base URL: `http://localhost:5001`



| Method | Endpoint | Description |

|---|---|---|

| GET | `/` | Application home page |

| GET | `/health` | Checks MySQL and Redis connectivity |

| GET | `/sales/stats` | Returns retail sales statistics |



Example requests:



```powershell

Invoke-RestMethod http://localhost:5001/

Invoke-RestMethod http://localhost:5001/health

Invoke-RestMethod http://localhost:5001/sales/stats

```



\### Expected Sales Statistics



| Metric | Value |

|---|---:|

| Total Orders | 3 |

| Items Sold | 7 |

| Total Revenue | 108.49 |

| Average Order Value | 36.16 |



\### Redis Caching



The `/sales/stats` endpoint uses Redis caching.



\- \*\*MISS:\*\* Data is fetched from MySQL, calculated and stored in Redis.

\- \*\*HIT:\*\* Previously cached data is returned directly from Redis.



The cache has a 30-second expiry.



\## 6. Monitoring with Prometheus and Grafana



The monitoring stack consists of:



1\. cAdvisor collects container resource metrics.

2\. Prometheus scrapes and stores the collected metrics.

3\. Grafana queries Prometheus and visualises the metrics.



Monitoring interfaces:



\- Grafana: http://localhost:3001

\- Prometheus: http://localhost:9091



The Grafana dashboard includes CPU utilisation monitoring for the retail containers.



\## 7. AppArmor Security Testing



A custom AppArmor profile named `retail-python` was created and loaded in Ubuntu WSL.



A separate Docker daemon was used at `/run/docker-apparmor.sock` to apply the custom profile to a Python test container.



Select the dedicated Docker daemon:



```bash

export DOCKER\_HOST=unix:///run/docker-apparmor.sock

```



Verify the active profile:



```bash

docker run --rm \\

&#x20; --security-opt apparmor=retail-python \\

&#x20; python:3.12-slim \\

&#x20; python -c "print(open('/proc/self/attr/current').read().strip())"

```



Expected output:



```text

retail-python (enforce)

```



Test restricted file access:



```bash

docker run --rm \\

&#x20; --security-opt apparmor=retail-python \\

&#x20; python:3.12-slim \\

&#x20; python -c "open('/etc/shadow').read()"

```



Expected result: `PermissionError: Permission denied`.



\*\*Environment note:\*\* The custom AppArmor profile was successfully enforced on a separate Python Docker test container using the Ubuntu WSL Docker daemon. It was not attached to the main Docker Desktop retail Compose application container.



\## 8. Fault Diagnosis and Recovery



Redis failure was simulated by stopping the Redis container:



```powershell

docker compose stop redis

```



The application health endpoint was used to inspect service connectivity:



```powershell

Invoke-RestMethod http://localhost:5001/health

```



Redis was restored:



```powershell

docker compose start redis

Start-Sleep -Seconds 5

Invoke-RestMethod http://localhost:5001/health

```



Expected recovery:



```text

mysql     redis       status

connected connected   healthy

```



\## 9. Cleanup



Stop and remove the containers and Compose network:



```powershell

docker compose down

```



To additionally remove the persistent Docker volumes:



```powershell

docker compose down -v

```



\*\*Note:\*\* The second command deletes the MySQL, Redis and Grafana persistent data volumes.



\## 10. Conclusion



The project demonstrates a containerised retail analytics application using isolated Docker services, Flask API endpoints, MySQL database integration, Redis caching, AppArmor security testing, Prometheus metrics collection, Grafana monitoring and fault recovery.



\*\*Project:\*\* CIE – Question 6  

\*\*Title:\*\* Retail Analytics Stack

