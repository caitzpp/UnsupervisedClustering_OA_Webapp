import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
load_dotenv()

def get_blob_container_client(container_name: str):
    try:
        print("Azure Blob Storage Python quickstart sample")
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

        # Create the BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a container client
        container_client = blob_service_client.get_container_client(container_name)
        return container_client

    except Exception as ex:
        print('Exception:')
        print(ex)


def blob_exists(container_client, blob_name):
    """Check if a blob exists in the container."""
    try:
        container_client.get_blob_client(blob_name).get_blob_properties()
        return True
    except Exception:
        return False