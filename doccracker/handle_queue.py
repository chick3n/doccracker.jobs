import argparse
import time
from dotenv import load_dotenv, find_dotenv
import logging
from . import _process_job
from .models.job import JobRequest
import logging
from .shared.queue import Queue
import json

parser = argparse.ArgumentParser(description = 'Handle queue requests for DocCracker')
parser.add_argument('queue', help='name of queue to retrieve from.')
args = parser.parse_args()
SLEEP_SECONDS = int(60)

def process_queue(queue:str) -> int:
    queue_client = Queue(encode_base64=True, decode_base64=True)
    queue_messages = queue_client.retrieve(queue)
    failed_count = 0

    for message in queue_messages:
        try:  
            if message.content is not None:
                job = JobRequest.from_queue_message(json.loads(message.content))
                if not _process_job.process_job(job):
                    raise Exception(f'{job.index}/{job.id} failed to process request. Queue Id {message.id}')
            queue_client.delete(queue, message)
        except Exception as e:
            logging.critical(str(e), exc_info=e)
            failed_count+=1

    return failed_count

load_dotenv(find_dotenv())
while(True):
    check_queue_start = time.perf_counter() 

    failures = process_queue(args.queue)

    sleep_for = SLEEP_SECONDS - (time.perf_counter() - check_queue_start)
    if sleep_for < 0:
        sleep_for = 1

    time.sleep(sleep_for)