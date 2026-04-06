from pathlib import Path
import sys

# Add scrape.py directory to path using absolute path
current_dir = Path(__file__).resolve().parent
scrape_path = current_dir.parent.parent.parent / 'data_sources' / 'website'
sys.path.insert(0, str(scrape_path))

from scrape import *
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# List the functions to process and push them to the database
functions = [league_table, top_scorers]

# Retrieve the database connection string from environment variables:
conn_string = os.getenv('AZURE_DATABASE_CONNECTION_STRING')

# Pass the connection string directly to pandas (no connection object needed)
for func in functions:
    function_name = func.__name__
    result_df = func()  # Call the function to get the DataFrame
    result_df.to_sql(function_name, con=conn_string, if_exists='replace', index=False)
    print(f'Pushed data for {function_name}')