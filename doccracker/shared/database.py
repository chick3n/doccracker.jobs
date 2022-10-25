import os
import logging
from typing import Any, List, Optional
from ..models.job import Job, JobDocument, JobDocumentEntity, JobEntity, JobOptionEntity
from azure.data.tables import TableClient, UpdateMode

class Database:
    def __init__(self):
        self.conn = os.environ['Database_ConnectionString']
        self.table_job = 'jobs'
        self.table_job_documents = 'jobDocuments'
        self.table_job_options = 'jobOptions'

    def get_job(self, p_key, row_key) -> Optional[JobEntity]: 
        with TableClient.from_connection_string(self.conn, self.table_job) as table_client:
            parameters = {"pkey": p_key, "rkey": row_key}
            name_filter = "PartitionKey eq @pkey and RowKey eq @rkey"
            queried_entities = table_client.query_entities(
                query_filter=name_filter, select=["PartitionKey", "RowKey", "State", "Action", "CreatedOn"], parameters=parameters  # type: ignore
            )

            for entity in queried_entities:
                return JobEntity(entity,
                    self.get_job_documents(row_key),
                    self.get_job_options(row_key))

        return None

    def get_job_options(self, p_key) -> List[JobOptionEntity]:
        options:List[JobOptionEntity] = []
        with TableClient.from_connection_string(self.conn, self.table_job_options) as table_client:
            parameters = {"pkey": p_key}
            name_filter = "PartitionKey eq @pkey"
            queried_entities = table_client.query_entities(
                query_filter=name_filter, select=["PartitionKey", "RowKey", "Name", "Value"], parameters=parameters  # type: ignore
            )

            for entity in queried_entities:
                options.append(JobOptionEntity(entity))

            return options
        
    def get_job_documents(self, p_key) -> List[JobDocumentEntity]:
        documents:List[JobDocumentEntity] = []
        with TableClient.from_connection_string(self.conn, self.table_job_documents) as table_client:
            parameters = {"pkey": p_key}
            name_filter = "PartitionKey eq @pkey"
            queried_entities = table_client.query_entities(
                query_filter=name_filter, select=["PartitionKey", "RowKey", "Title"], parameters=parameters  # type: ignore
            )

            for entity in queried_entities:
                documents.append(JobDocumentEntity(entity))

            return documents

    def __update_job(self, job: dict[str, Any]) -> Optional[JobEntity]:
        with TableClient.from_connection_string(self.conn, self.table_job) as table_client:
            entity = table_client.get_entity(job['PartitionKey'], job['RowKey'])
            if entity is None:
                logging.info(f'Job Entity {job["PartitionKey"]}/{job["RowKey"]} does not exist')
                return None
            table_client.update_entity(mode=UpdateMode.MERGE, entity=job)
            return JobEntity(entity)
    
    def update_job_state(self, p_key, r_key, state) -> Optional[JobEntity]:
        entity = {'PartitionKey': p_key, 'RowKey': r_key, 'State': state}
        return self.__update_job(entity)

