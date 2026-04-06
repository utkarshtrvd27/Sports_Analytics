from pathlib import Path
import sys

# Add scrape.py directory to path using absolute path
current_dir = Path(__file__).resolve().parent
scrape_path = current_dir.parent.parent.parent / 'data_sources' / 'website'
sys.path.insert(0, str(scrape_path))

from scrape import *
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os

load_dotenv()

# List of functions to process and upload
functions = [league_table, top_scorers]

def to_blob(func):

    '''
    Converts the output of a given function to Parquet format and uploads it to Azure Blob Storage.
    Args:
        func (function): The function that retrieves data to be processed and uploaded.
    Returns:
        None
    This function takes a provided function, calls it to obtain data, and then converts the data into
    an Arrow Table. The Arrow Table is serialized into Parquet format and uploaded to an Azure Blob
    Storage container specified in the function. The function's name is used as the blob name.
    '''

    file_name = func.__name__
    res = func()

    # Convert DataFrame to Arrow Table
    table = pa.Table.from_pandas(res)

    parquet_buffer = BytesIO()
    pq.write_table(table, parquet_buffer)

    # Retrieving Azure Blob Storage connection string
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING', 'fallback_connection_string')
    # Creating a Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Uploading the Parquet file to the given Azure Blob Container
    container_name = "utstg"
    blob_name = f"{file_name}.parquet"
    container_client = blob_service_client.get_container_client(container_name)

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(parquet_buffer.getvalue(), overwrite=True)
    print(f"{blob_name} successfully updated")


for items in functions:
    to_blob(items)