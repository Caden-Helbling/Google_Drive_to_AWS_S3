import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import hashlib

# Authenticate with Google Drive API
creds = Credentials.from_authorized_user_file(os.path.join('/Users/chelblin/Projects/Google_Drive_to_AWS_S3/credentials.json'), ['https://www.googleapis.com/auth/drive'])
service = build('drive', 'v3', credentials=creds)

# List files
files = service.files().list().execute().get('files', [])

# Get MD5 checksum for each file
for file in files:
    file_id = file['id']
    md5_checksum = service.files().get(fileId=file_id, fields='md5Checksum').execute()['md5Checksum']
    print(f"{file['name']}: {md5_checksum}")

    # Copy file to local disk
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join('path', 'to', 'local', 'directory', file['name'])
    with open(file_path, 'wb') as f:
        f.write(request.execute())

    # Validate MD5 checksum
    with open(file_path, 'rb') as f:
        file_data = f.read()
        local_md5 = hashlib.md5(file_data).hexdigest()
    assert md5_checksum == local_md5
