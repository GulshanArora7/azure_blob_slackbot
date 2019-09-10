import datetime
import re
from azure.storage.blob import BlockBlobService
from application.convert_size import SIZE_CONVERSION

class BlobFilesPattern:
    def __init__(self, storage_account_name, storage_account_key, condition, number_of_days_old, container_name, file_pattern):
        self.storage_account_name = storage_account_name
        self.storage_account_key = storage_account_key
        self.condition =  condition
        self.number_of_days_old = int(number_of_days_old)
        self.container_name = container_name
        self.file_pattern =  file_pattern

    def azure_blob_file(self):
        regular_exp = re.compile(self.file_pattern)
        name_list = []
        block_blob_service = BlockBlobService(account_name=self.storage_account_name, account_key=self.storage_account_key)
        generator = block_blob_service.list_blobs(self.container_name)
        today = datetime.datetime.now().date()
        for blob in generator:
            if (regular_exp.match(str(blob.name))):
                blob_date = blob.properties.last_modified.date()
                time_between_insertion = today - blob_date
                if self.condition == "last":
                    if  time_between_insertion.days <= self.number_of_days_old:
                        c_size = SIZE_CONVERSION(blob.properties.content_length)
                        blob_size = c_size.convert_size()
                        name_list.append(' : '.join([blob.name, blob_size]))
                elif self.condition == "before":
                    if  time_between_insertion.days >= self.number_of_days_old:
                        c_size = SIZE_CONVERSION(blob.properties.content_length)
                        blob_size = c_size.convert_size()
                        name_list.append(' : '.join([blob.name, blob_size]))
                else:
                    print("Unexpected ERROR..!!")
        return name_list