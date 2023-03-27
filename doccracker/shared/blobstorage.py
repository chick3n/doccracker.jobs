import os
from azure.storage.blob import BlobServiceClient, BlobClient

class BlobStorage:
    def __init__(self):
        self.conn = os.environ['Storage_ConnectionString']
        self.service:BlobServiceClient = BlobServiceClient.from_connection_string(self.conn)

    def __client(self, container, blobname) -> BlobClient:
        return self.service.get_blob_client(container=container, blob=blobname)

    def upload(self, container_name:str, filename:str, text:str) -> None:
        client = self.__client(container=container_name, blobname=filename)
        client.upload_blob(text, overwrite=True)
