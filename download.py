from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

# Get the list of all files in the Google Drive account
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()

# Download each file in the file list
for file1 in file_list:
    file1.GetContentFile(file1['title'])
