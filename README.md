## FastAPI Prime Number Generator 

This project demonstrates a production-style architecture using:
1. FastAPI - API service
2. Celery - Background task processing
3. RabbitMQ - Message broker
4. Redis - Celery result backend
5. OpenTelemetry - Traces + Metrics
6. VictoriaMetrics - High-performance metric storage
7. Grafana - Monitoring dashboards
8. Flower - Celery task monitoring UI
9. Locust - Load testing
10. Docker Compose - Multi-container orchestration
11. Node Exporter → System metrics
12. RabbitMQ Exporter → Queue metrics
13. Custom Celery Exporter → Worker metrics

It includes both Sync and Async prime number generation.


## Project Structure
test_app/
|-- main.py
|-- tasks.py
|-- utils.py
|-- celery_worker.py
|-- celery_exporter.py
|-- locustfile.py
|-- Dockerfile
|-- docker-compose.yml
|-- prometheus.yml
|-- promscrape.yaml
│-- otel-config.yaml
│-- grafana
      │--dashboard.json
|-- requirements.txt


## 1. Prerequisites
Install:
1. Docker Desktop 
2. Python 3.10+
3. VS Code / Pycharm 


## 2. How to Build & Run the Project (Using Docker)
Build & Start All Services  -> docker compose up --build
This starts: Service	URL
1. FastAPI	-> http://localhost:8000
2. Swagger UI -> http://localhost:8000/docs
3. RabbitMQ UI -> http://localhost:15672
4. Grafana -> http://localhost:3000
5. Flower (Celery UI) -> http://localhost:5555
6. VictoriaMetrics UI -> http://localhost:8428


## 3. API Endpoints
1. Generate Prime Numbers (Sync) - Works immediately inside FastAPI -> 
GET /primes?n=10

2. Generate Prime Numbers (Async — Celery Background Task) ->
POST /primes/async?n=10

** Response example:
{
  "request_id": "bec93335-0223-4976-ad02-f13fa2c1251d",
  "task_id": "2a237247-29c2-4a72-8342-b82182d75bb4",
  "status": "PENDING"
}

3.  Get Task Result -> 
GET /tasks/{task_id}


## 4. Start Celery Worker Manually (Optional)
run Celery manually (outside Docker)-> 
celery -A tasks.celery_app worker --loglevel=info


## 5. Monitoring Tools
1. RabbitMQ Management UI -> http://localhost:15672
username: guest
password: guest

2. Flower (Celery Task Dashboard) -> http://localhost:5555
Shows:
Running tasks
Completed tasks
Queues
Worker status

3. Grafana Dashboard -> http://localhost:3000
username: admin  
password: admin  
After login -> Import dashboard -> Add Prometheus data source (url->  http://victoriametrics:8428)


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
1. docker compose down
2. For a clean reset -> docker compose down -v


## 8. Features Implemented
1. FastAPI -> Sync + Async task execution
2. Celery -> Background task worker
3. Monitoring Stack -> 
      a. VictoriaMetrics as TSDB
      b. Grafana dashboards
      c. RabbitMQ Exporter
      d. Custom Celery Exporter
4. Load Testing -> Locust simulating real users
5. Dockerized -> All services containerized


