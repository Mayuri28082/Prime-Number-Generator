from celery import Celery
from utils import get_primes
from opentelemetry.instrumentation.celery import CeleryInstrumentor
from opentelemetry import metrics
import time


celery_app = Celery("prime_tasks", broker="amqp://guest:guest@rabbitmq:5672//", backend="redis://redis:6379/0")

CeleryInstrumentor().instrument()

celery_meter = metrics.get_meter("celery-meter")
task_counter = celery_meter.create_counter("celery_task_completed_total")
task_duration = celery_meter.create_histogram("celery_task_duration_seconds")


@celery_app.task(name="tasks.generate_primes_task")
def generate_primes_task(n: int):
    start = time.time()
    primes = get_primes(n)
    duration = time.time() - start
    task_counter.add(1)
    task_duration.record(duration)
    return {"count": n, "primes": primes}
