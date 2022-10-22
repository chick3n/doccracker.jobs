import argparse
import time
from shared.queue import Queue
from models.job import JobRequest
import json
from dotenv import load_dotenv, find_dotenv

parser = argparse.ArgumentParser(description = 'Handle queue requests for DocCracker')
parser.add_argument('queue', help='name of queue to retrieve from.')
args = parser.parse_args()
SLEEP_SECONDS = 60


def process_queue(queue:str):
    queue_client = Queue()
    queue_messages = queue_client.retrieve(queue)
    for message in queue_messages:        
        job = JobRequest.from_queue_message(json.loads(message.content))
        print(job)

load_dotenv(find_dotenv())
while(True):
    check_queue_start = time.perf_counter() 

    process_queue(args.queue)

    sleep_for = SLEEP_SECONDS - (time.perf_counter() - check_queue_start)
    if sleep_for < 0:
        sleep_for = 1

    time.sleep(sleep_for)