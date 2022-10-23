import json
from .shared import Database, Search, BlobStorage
from .models.job import JobRequest, JobAction, JobEntity, JobState
import logging
from .jobs.summary import ExtractiveSummary
import os


def process_job(job:JobRequest) -> bool:    
    db_client = Database()
    
    job_entity = db_client.get_job(job.index, job.id)
    
    if job_entity is None:
        logging.warn(f'No table entry found for {job.index}/{job.id}')
        return False

    if job_entity.Action == JobAction.ExtractiveSummary:
        process_extractive_summary(job_entity)
        db_client.update_job_state(job_entity.PartitionKey, job_entity.RowKey, JobState.Completed)
    else:
        logging.warn(f'{job_entity.PartitionKey}/{job_entity.RowKey} unknown action {job_entity.Action}')
        return False
    return True

def process_extractive_summary(job:JobEntity) -> None:
    search = Search(job.PartitionKey)    
    blob_client = BlobStorage()
    sum_client = ExtractiveSummary()
    upload_container = os.environ['Container_CompleteName']
    
    summaries = {}
    for document in job.Documents:
        text = search.get_document_text(document.RowKey)
        summary = sum_client.sbertsummary(text)
        if summary:
            summaries[document.RowKey] = summary

    blob_client.upload(upload_container, job.RowKey, json.dumps(summaries, indent=4, default=str))
    


    


