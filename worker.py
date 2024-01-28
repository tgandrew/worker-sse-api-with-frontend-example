import time

from rq import get_current_connection, get_current_job

r = get_current_connection()

def query(question: str):
    job = get_current_job()
    r.xadd(job.id, {"msg": f"Starting to process question: {question}"})
    for i in range(10):
        time.sleep(1)
        r.xadd(job.id, {"msg": f"Sleep {i}"})
        print(f"Sleep {i}")
    r.xadd(job.id, {"msg": "STOP"})
    print("Finished")
    return {'task': 'complete'}