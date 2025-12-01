from celery import Celery
from utils import get_primes

BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
BACKEND_URL = "redis://redis:6379/0"

celery_app = Celery("prime_tasks", broker=BROKER_URL, backend=BACKEND_URL)


@celery_app.task(name="tasks.generate_primes")
def generate_primes_task(n: int):
    primes = get_primes(n)
    return {"count": n, "primes": primes}
