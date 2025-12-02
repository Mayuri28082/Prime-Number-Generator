from prometheus_client import start_http_server, Gauge
from celery import Celery
import time

celery_app = Celery("prime_tasks",broker="amqp://guest:guest@rabbitmq:5672//")


celery_tasks = Gauge('celery_tasks_total', 'Total tasks in Celery queues')


def collect_metrics():
    while True:
        inspector = celery_app.control.inspect()
        stats = inspector.active() or {}
        total_tasks = sum(len(v) for v in stats.values()) if stats else 0
        celery_tasks.set(total_tasks)
        time.sleep(5)


if __name__ == "__main__":
    start_http_server(9808)
    collect_metrics()
