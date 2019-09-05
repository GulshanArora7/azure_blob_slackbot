from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.storage import StorageManagementClient

class STORAGE:
    def __init__(self, subscription_id, client_id, client_secret, tenant_id, resource_group_name, storage_account_name ):
        self.subscription_id = subscription_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name

    def azure_storage(self):
        credentials = ServicePrincipalCredentials(
            client_id = self.client_id,
            secret = self.client_secret,
            tenant = self.tenant_id
        )
        storage_client = StorageManagementClient(credentials, self.subscription_id)
        storage_keys = storage_client.storage_accounts.list_keys(self.resource_group_name, self.storage_account_name)
        storage_keys = {v.key_name: v.value for v in storage_keys.keys}
        key1 = storage_keys['key1']
        return key1
    