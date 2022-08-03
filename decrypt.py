#!/usr/bin/python3

"""
# Steps to use:

> ## Pehli baar ye steps bhi krna hoga:
> 1. pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib PyPDF3
> 2. Go to https://console.cloud.google.com/apis/credentials/ and create an OAuth key, download it as json, copy in this folder and rename as 'credentials.json

1. Run `python decrypt.py`
2. Chose nit patna email id (ie. the email id that has access to the files)

"""

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from PyPDF3 import PdfFileReader, PdfFileWriter
import re
from os import environ as env

file_name_regex = re.compile(r"^Lecture \d+.*\.pdf$")
drive_folder_name = "Lecture Handouts"  # jis folder me encrypted pdfs hai (in google drive)
drive_folder_name_decrypted = drive_folder_name + " Decrypted" # jis folder me pdfs save honge (in google drive)
your_folder_name  = "cs7479"            # jis folder me pdfs save hoga (decrypted, local)

# To make it simpler, directly add password here
password = ""

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.install']

def printdebug(*argv):
    i=0
    #print("\n[DEBUG]: ", argv, "\n");

def decrypted_file_exists(fname):
    if os.path.isfile(fname):
        with open(fname, "rb") as file:
            return PdfFileReader(file).getIsEncrypted() == False
    else:
        return False

def decrypt_file(filename):
    print(f"Decrypting {filename}...")
    file = open(filename, "rb")

    writer = PdfFileWriter()
    reader = PdfFileReader(file)

    if reader.getIsEncrypted == False:
        return

    reader.decrypt(password)

    for page in reader.pages:
        writer.addPage(page)

    new_filename = filename + '.temp'
    decrypted_file = open(new_filename, "wb")
    writer.write(decrypted_file)

    file.close()
    decrypted_file.close()
    os.remove(filename)
    os.rename(new_filename, filename)

def main():
    if password == "" and env.get("PASSWD") is None:
        print("[WARN] Password not set. Please set `password` in the code (or PASSWD environment variable)")

    # Isme hum credentials (ie. token, etc. received when you logged in your google account)
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # NOTE: Can also pass content of token.json in environment variable: GDRIVETOKEN. token.json has higher precedence, if present
    if os.path.exists('token.json') is False and env.get("GDRIVETOKEN") is not None:
        gdrivetoken = env.get("GDRIVETOKEN")
        with open("token.json", mode="w") as token_json:
            token_json.write(gdrivetoken)

    if os.path.exists('token.json'):
        try:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        except ValueError:
            print("ValueError happened")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            except FileNotFoundError:
                print("credentials.json file not found... \nGo to https://console.cloud.google.com/apis/credentials/ and create an OAuth key, download it as json, and rename as 'credentials.json'")
            creds = flow.run_local_server(port=55000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Now everything after this runs inside the `your_folder` directory (to make sure we don't change anything outside it)
    try:
        os.mkdir(your_folder_name)
    except FileExistsError:
        print(f"{your_folder_name} directory already exists... Continuing")

    os.chdir(your_folder_name)

    # Getting folder id (of the name as in `drive_folder_name`variable)
    folders = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name = '{drive_folder_name}' or name = '{drive_folder_name_decrypted}'",
        pageSize=10, fields="files(id, name)").execute().get('files', [])

    printdebug("folders: ", folders)

    notes_folder_id = None
    decrypted_notes_folder_id = None

    for folder in folders:
        if folder['name'] == drive_folder_name:
            if notes_folder_id is None:
                notes_folder_id = folder['id']
        elif folder['name'] == drive_folder_name_decrypted:
            if decrypted_notes_folder_id is None:
                decrypted_notes_folder_id = folder['id']

    if notes_folder_id == None:
        print(f"{drive_folder_name} not found, in your Google Drive (can use the 'Add a shortcut to drive' option on the shared folder)")
        print("Exiting...")
        return

    # Now we fetch list of all files inside the folder
    results = service.files().list(
        q=f"mimeType='application/pdf' and '{notes_folder_id}' in parents",
        pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    printdebug("items: ", items)

    # Iterate through all file names
    for item in items:
        # the .get_media() provices us with a stream to download the files (We ONLY download files, whose names match the `file_name_regex` variable) 
        request = service.files().get_media(fileId=item['id'])
        if (file_name_regex.match(item['name']) != None) and not decrypted_file_exists(item['name']):
            print(f"Downloading {item['name']}")
            result = request.execute()
            with open(item['name'], mode="wb") as fout:
                fout.write(result)

            decrypt_file(item['name'])
        else:
            # The file may have been something other the Lecture pdf
            print(f"Skipping {item['name']}. Already downloaded or not a lecture pdf")

    # Uploading decrypted files
    if decrypted_notes_folder_id is None:
        print("Creating remote google drive folder")
        # reference: https://stackoverflow.com/questions/13558653/how-can-i-create-a-new-folder-with-google-drive-api-in-python
        # creating at root, no parent
        body = {
            'name': drive_folder_name_decrypted,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        result = service.files().create(body=body).execute()
        print("Created remote google drive folder: ", result)
        decrypted_notes_folder_id = result.get('id')
    else:
        print("Remote google drive folder already exists. Continuing...")

    already_uploaded_files = service.files().list(
        q=f"mimeType='application/pdf' and '{decrypted_notes_folder_id}' in parents",
        pageSize=50, fields="nextPageToken, files(id, name)").execute().get('files', [])

    printdebug("already_uploaded_files: ", already_uploaded_files)

    # iterate over all files in current directory
    for file in os.listdir():
        request = service.files().create(
            body={
                'name': file,
                'mimeType': 'application/pdf',
                'parents': [decrypted_notes_folder_id],
                'description': f"Decrypted version of the lecture file {file}",
                #'isAppAuthorized': True,
                #'ownedByMe': True,
                #'capabilities': {
                #    "canShare": True,
                #},
            },
            #enforceSingleParent = True,
            #useContentAsIndexableText = True,
            media_body=file
        )

        found = False
        for uploaded_file in already_uploaded_files:
            if uploaded_file['name'] == file:
                found = True
                break

        if found == False:
            print(f"Uploading {file}")
            request.execute()
        else:
            print(f"Skipping {file}. Already uploaded")

if __name__ == '__main__':
    main()
