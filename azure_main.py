import os
from pathlib import Path

# Get the directory of this script
current_dir = Path(__file__).resolve().parent

# Construct full paths to the scripts
blob_script = current_dir / 'data_storage' / 'Azure' / 'blob' / 'push_to_blob.py'
db_script = current_dir / 'data_storage' / 'Azure' / 'synapse' / 'push_to_database.py'

# Run the scripts with full paths
os.system(f'python "{blob_script}"')
os.system(f'python "{db_script}"')