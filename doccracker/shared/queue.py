from typing import List
from azure.core.paging import ItemPaged
from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy,
        QueueMessage
)

import os, uuid, base64

class Queue:
    def __init__(self, encode_base64=False, decode_base64=False):
        self.conn = os.environ['Queue_ConnectionString']
        self.encode_base64 = encode_base64
        self.decode_base64 = decode_base64
    
    def __client(self, queue_name:str):
        return QueueClient.from_connection_string(self.conn, queue_name ,
                            message_encode_policy = BinaryBase64EncodePolicy() if self.encode_base64 else None,
                            message_decode_policy = BinaryBase64DecodePolicy() if self.decode_base64 else None
                            )

    def create(self, queue_name:str):
        try:
            self.__client(queue_name).create_queue()
        except:
            pass

    def send(self, queue:str, message:str) -> None:
        #encoded_message = base64.b64encode(message.encode('utf8'))
        self.__client(queue).send_message(message)

    def peek(self, queue:str) -> List[QueueMessage]:
        return self.__client(queue).peek_messages(1)

    def retrieve(self, queue:str, max:int=10, timeout:int=30) -> ItemPaged[QueueMessage]:
        messages = self.__client(queue).receive_messages(messages_per_page=max,
            visibility_timeout=timeout)

        return messages

    def delete(self, queue:str, msg:QueueMessage):
        self.__client(queue).delete_message(msg)