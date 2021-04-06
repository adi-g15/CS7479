#!/usr/bin/python3

# Is file se ab automatically drive ka lecture handouts folder se download karke decrypt karlega ye files ko
# So you won't need to go to https://cs4401.netlify.app and check drive's folder, no need now :D
# Aur ye baar baar same file ko download/decrypt bhi nhi karega

# Steps to use (ONE TIME):
# 1. https://console.cloud.google.com/apis/credentials/ and create an OAuth key, download it as json, and rename as 'credentials.json
# 2. Run `python simple_decrypt.py`
# 3. Chose nit patna email id (ie. the email id that has access to the files)

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.cloud import storage
from PyPDF3 import PdfFileReader, PdfFileWriter
import re

# Ye run karna hai before running this script
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib PyPDF3

file_name_regex = re.compile(r"^Lecture \d+.*Unit.*\.pdf")
drive_folder_name = "Lecture Handouts"
your_folder_name  = "cs4401"    # jis folder me pdfs save hoga (decrypted)
password = "nitp_cs4401-Spr21"   # or any other password your notes has

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly']

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
    # Isme hum credentials (ie. token, etc. received when you logged in your google account)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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
        q=f"mimeType='application/vnd.google-apps.folder' and name = '{drive_folder_name}'",
        pageSize=1, fields="files(id, name)").execute().get('files', [])
    notes_folder_id = folders[0]['id'] or '1oGKKT1DVB__792WIMvARUSFJkUqy2jWu'

    # Now we fetch list of all files inside the folder
    results = service.files().list(
        q=f"mimeType='application/pdf' and '{notes_folder_id}' in parents and name contains 'Lecture'",
        pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

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
            print(f"Skipping {item['name']}")

if __name__ == '__main__':
    main()
