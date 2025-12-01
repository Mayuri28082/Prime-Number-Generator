## FastAPI Prime Number Generator 

This project demonstrates a production-style architecture using:
1. FastAPI - API service
2. Celery - Background task processing
3. RabbitMQ - Message broker
4. Redis - Celery result backend
5. Prometheus - Metrics collection
6. Grafana - Monitoring dashboards
7. Flower - Celery task monitoring UI
8. Locust - Load testing
9. Docker Compose - Multi-container orchestration

It includes both Sync and Async prime number generation.

## Project Structure
test_app/
|-- main.py
|-- tasks.py
|-- utils.py
|-- celery_worker.py
|-- locustfile.py
|-- Dockerfile
|-- docker-compose.yml
|-- prometheus.yml
|-- requirements.txt


## 1. Prerequisites
Install:
Docker Desktop
Python 3.10+
VS Code / Pycharm

## 2. How to Build & Run the Project (Using Docker)
Build & Start All Services  -> docker compose up --build
This starts: Service	URL
FastAPI	-> http://localhost:8000
RabbitMQ UI -> http://localhost:15672
Grafana -> http://localhost:3000
Prometheus -> http://localhost:9090
Flower (Celery UI) ->	http://localhost:5555

## 3. API Endpoints
1. Generate Prime Numbers (Sync) - Works immediately inside FastAPI.
GET /primes?n=10

2. Generate Prime Numbers (Async — Celery Background Task)
POST /primes/async?n=10

** Response example:
{
  "request_id": "bec93335-0223-4976-ad02-f13fa2c1251d",
  "task_id": "2a237247-29c2-4a72-8342-b82182d75bb4",
  "status": "PENDING"
}

3.  Get Task Result
GET /tasks/{task_id}

4.  Prometheus Metrics
GET /metrics

5. FastAPI Swagger UI
http://localhost:8000/docs

## 4. Start Celery Worker Manually (Optional)
run Celery manually (outside Docker):
celery -A tasks.celery_app worker --loglevel=info

## 5. Monitoring Tools
1️. RabbitMQ Management UI -> http://localhost:15672
username: guest
password: guest

2. Flower — Celery Task Dashboard -> http://localhost:5555
Shows:
Running tasks
Completed tasks
Queues
Worker status

3️. Prometheus — Raw Metrics Collector -> http://localhost:9090
Metrics include:
http_requests_total
http_request_latency_seconds

4️. Grafana Dashboard -> http://localhost:3000
username: admin  
password: admin  
After login → Import dashboard → Add Prometheus datasource.

## 6. Load Testing using Locust
Start Locust inside Docker (Not included in Compose. Run locally) -> locust -f locustfile.py
Open browser: -> http://localhost:8089
Enter: 
Host: http://localhost:8000
Users: e.g., 20
Spawn rate: e.g., 5
* Locust tests:
/primes?n=10
/primes?n=100
/primes/async

## 7. Stopping Containers
docker compose down
For a clean reset -> docker compose down -v

## 8. Verify Celery Worker Status
docker exec -it celery-worker sh
celery -A tasks inspect stats

## 9. Features Implemented
1. Sync + Async task execution
2. Celery distributed task queue
3. Reliable background processing
4. Real-time monitoring: Prometheus, Grafana, Flower
5. Automatic metrics exposure
6. Load testing with Locust
7. Fully containerized with Docker Compose
