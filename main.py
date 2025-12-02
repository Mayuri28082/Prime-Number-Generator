from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
import uuid
from tasks import generate_primes_task
from utils import get_primes
from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry import trace, metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "prime-service"})))
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="otel-collector:4317", insecure=True))
trace.get_tracer_provider().add_span_processor(span_processor)


metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint="otel-collector:4317", insecure=True))
metrics.set_meter_provider(MeterProvider(resource=Resource.create({"service.name": "prime-service"}), metric_readers=[metric_reader]))

meter = metrics.get_meter("prime-meter")
http_requests_counter = meter.create_counter("http_requests_total")


app = FastAPI(title="Prime Number Generator")

FastAPIInstrumentor.instrument_app(app)

Instrumentator().instrument(app).expose(app)  



class PrimeNumResponse(BaseModel):
    count: int
    primes: list[int]

class TaskResponse(BaseModel):
    request_id: str
    task_id: str
    status: str




@app.get("/primes", response_model=PrimeNumResponse)
def primes_gen(n: int = Query(..., gt=0)):
    primes = get_primes(n)
    return PrimeNumResponse(count=n, primes=primes)



@app.post("/primes/async", response_model=TaskResponse)
def primes_gen_async(n: int = Query(..., gt=0)):
    task = generate_primes_task.apply_async(args=[n])
    request_id = str(uuid.uuid4())
    return TaskResponse(request_id=request_id, task_id=task.id, status=task.status)




@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=generate_primes_task.app)
    return {"task_id": task_id, "status": result.state, "result": result.result if result.ready() else None}


