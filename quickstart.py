from __future__ import print_function

import os.path

import os

if not os.path.exists('/Users/chelblin/Projects/Google_Drive_to_AWS_S3/Downloads'):
    os.makedirs('/Users/chelblin/Projects/Google_Drive_to_AWS_S3/Downloads')


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.readonly']

def download_file(service, file_id, file_name):
    request = service.files().get_media(fileId=file_id)
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    if not os.path.exists(file_name):
        file_extension = os.path.splitext(file_name)[1]
        if file_extension in docs_editors_mimetypes:
            request = service.files().export_media(fileId=file_id, mimeType=docs_editors_mimetypes[file_extension])
        with open(file_name, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'{file_name} downloaded {int(status.progress() * 100)}.')




def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
        else:
            for item in items:
                file_id = item['id']
                file_name = item['name']
                download_file(service, file_id, file_name)
                print(f"{file_name} downloaded successfully")
    except HttpError as error:
        print(f'An error occurred: {error}')
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['name'], item['id']))
    # except HttpError as error:
    #     # TODO(developer) - Handle errors from drive API.
    #     print(f'An error occurred: {error}')

    #     # Call the Drive v3 API to retrieve the ID of the file to be downloaded
    #     file_id = '1SP8uwA7wA1YOHduzlZgTT7gGcsKuPTwFSPOyHmwgwMs'
    #     file = service.files().export(fileId=file_id, mimeType='application/pdf').execute()

    #     # Download the file
    #     file_name = file['name']
    #     request = service.files().get_media(fileId=file_id)
    #     with open(file_name, 'wb') as f:
    #         f.write(request.execute())
        
    #     print(f'{file_name} has been downloaded successfully.')
    # except HttpError as error:
    #     # Handle errors from the Drive API
    #     print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()