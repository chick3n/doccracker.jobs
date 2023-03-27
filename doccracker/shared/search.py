import os
import logging
from typing import List, Optional, Tuple
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

class Search:
    def __init__(self, index):
        self.key = os.environ['Search_Key']
        self.endpoint = os.environ['Search_Endpoint']
        self.index = index

    def __get_search_client(self):
        return SearchClient(self.endpoint, self.index, AzureKeyCredential(self.key))

    def get_document_text(self, document_id:str, field:str='content') -> str | None:
        document = self.get_document(document_id)
        if document and field in document:
            return document[field]

    def get_document_texts(self, documents:List[str], field:str='content') -> List[Tuple[str, str]]:
        texts = []
        for document_id in documents:
            text = self.get_document_text(document_id, field)
            if text:
                texts.append(text)

        return texts

    def get_document(self, record_id:str) -> dict:
        client = self.__get_search_client()
        return client.get_document(key=record_id)
        
