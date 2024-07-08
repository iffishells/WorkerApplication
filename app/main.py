from fastapi import FastAPI
from redis import Redis
from rq import Queue
from pydantic import BaseModel
from app.job import print_number


class JobData(BaseModel):
    lowest: int
    highest: int


app = FastAPI()
redis_conn = Redis(host='localhost', port=6379)
task_queue = Queue("task_queue", connection=redis_conn)


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.post("/tasks")
def post_job(job: JobData):
    lowest = job.lowest
    highest = job.highest

    job = task_queue.enqueue(print_number, lowest, highest)
    return {"job_id": job.get_id()}
