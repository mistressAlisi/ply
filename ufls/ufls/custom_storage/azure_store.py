from storages.backends.azure_storage import AzureStorage


class PublicAzureStorage(AzureStorage):
    account_name = 'furrydelphiapublic'
    account_key = 'LlsjOxlOp8lcukF3Dy5jIeeAUftpiI7CV7pLD9/1aV/anBGohvqacVgXIqpMsT82zSybUQEunJ+XgT2hEcrSeA=='
    azure_container = 'ufls'
    expiration_secs = None