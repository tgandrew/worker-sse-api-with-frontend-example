import time

from rq import get_current_connection, get_current_job

r = get_current_connection()

def query(question: str):
    job = get_current_job()
    r.publish(job.id, f"Starting to process question: {question}")
    for i in range(10):
        time.sleep(1)
        r.publish(job.id, f"Sleep {i}")
        print(f"Sleep {i}")
    r.publish(job.id, "STOP")
    print("Finished")
    return {'task': 'complete'}