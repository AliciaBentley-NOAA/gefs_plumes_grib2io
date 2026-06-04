import os
import glob
from datetime import datetime, timedelta

# Change to the target directory
os.chdir('/home/people/emc/www/htdocs/users/meg/gefs_plumes')

# 1. Calculate the date from 18 days ago
target_date = datetime.now() - timedelta(days=18)

# 2. Format it as YYYYMMDD
date_str = target_date.strftime('%Y%m%d')

# 3. Find all files containing that date string
# This matches the behavior of *YYYYMMDD*
file_pattern = f'*{date_str}*'
files_to_delete = glob.glob(file_pattern)

# 4. Loop through and delete the files safely
if not files_to_delete:
    print(f"No files found matching pattern: {file_pattern}")
else:
    print(f"Found {len(files_to_delete)} files from 18 days ago ({date_str}). Cleaning up...")
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")
