import datetime
import re
from azure.storage.blob import BlockBlobService

class BlobFiles:
    def __init__(self, account, account_key, container_name, number_of_days_old):
        self.account = account
        self.account_key = account_key
        self.container_name = container_name
        self.number_of_days_old = int(number_of_days_old)

    def azure_blob(self):
        name_list = []
        block_blob_service = BlockBlobService(account_name=self.account, account_key=self.account_key)
        generator = block_blob_service.list_blobs(self.container_name)
        today = datetime.datetime.now().date()
        for blob in generator:
            blob_date = blob.properties.last_modified.date()
            time_between_insertion = today - blob_date
            if  time_between_insertion.days > self.number_of_days_old:
                name_list.append(blob.name)
        return name_list