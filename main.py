from fastapi import FastAPI , Query, Request, Response, HTTPException
from pydantic import BaseModel
from utils import get_primes
from prometheus_client import Counter, Summary, generate_latest, CONTENT_TYPE_LATEST
from celery.result import AsyncResult
import uuid
import logging
from tasks import generate_primes_task, celery_app
from utils import get_primes


app = FastAPI(title = "Generate Prime number")

REQUEST_COUNTER = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Summary("http_request_latency_seconds", "Request latency in seconds", ["endpoint"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrimeNumResponse(BaseModel):
    count : int 
    primes: list[int] 


class TaskResponse(BaseModel):
    request_id: str
    task_id: str
    status: str



@app.get("/primes", response_model=PrimeNumResponse)
def primes_gen(n: int = Query(..., gt=0, description="Number of Primes to generate")):
    out = get_primes(n) 

    return PrimeNumResponse(count=n, primes=out)




@app.middleware("http")
async def add_request_id_and_metrics(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    logger.info(f"[REQUEST START] {request.url.path} req_id={request_id}")

    with REQUEST_LATENCY.labels(endpoint=request.url.path).time():
        response: Response = await call_next(request)

    response.headers["X-Request-ID"] = request_id
    REQUEST_COUNTER.labels(method=request.method, endpoint=request.url.path,
                        status=str(response.status_code)).inc()

    logger.info(f"[REQUEST END] req_id={request_id} status={response.status_code}")
    return response



@app.get("/primes", response_model=PrimeNumResponse)
def primes_gen(n: int = Query(..., gt=0)):
    primes = get_primes(n)
    return PrimeNumResponse(count=n, primes=primes)



@app.post("/primes/async", response_model=TaskResponse)
def primes_gen_async(n: int = Query(..., gt=0)):
    task = celery_app.send_task("tasks.generate_primes", args=[n])
    request_id = str(uuid.uuid4())

    return TaskResponse(request_id=request_id, task_id=task.id, status=task.status)



@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = celery_app.AsyncResult(task_id)
    if result.state == "SUCCESS":
        return {"task_id": task_id, "status": result.state, "result": result.result}
    return {"task_id": task_id, "status": result.state}



@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)









