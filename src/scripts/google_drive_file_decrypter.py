#!/usr/bin/python3

# you may like to give this file a shorter name in your case

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from PyPDF3 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
import re
import subprocess
import sys

file_name_regex = re.compile(r"^Lecture \d+.*Unit.*\.pdf")
notes_folder_name = "Lecture Handouts"
password = "nitp_cs4401-Spr21"   # or any other password your notes has

# https://console.cloud.google.com/apis/credentials
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/drive.readonly']
BUCKET_URI = "gs://assignment-7d2c8.appspot.com"

# pre-condition: Current directory is same as the notes directory
def create_zips():
    SUB_CODE = 'CS4401_COA'

    with ZipFile("CS4401_COA_All.zip", "w") as all_notes:
        for filename in next(os.walk('.'))[2]:
            if filename[-4:] == '.zip':
                continue
            print(f"Adding {filename} in AllZip")
            all_notes.write(filename)

    files = next(os.walk('.'))[2]
    iter = filter(lambda file: file_name_regex.match(file) != None, files)
    files = list(iter)

    units = {'I': [], 'II': [], 'III': [], 'IV': []}

    for n in units:
        units[n] = [file for file in files if file.find(f"Unit {n} -") != -1]

        if len(units[n]) == 0:
            continue

        file_str = "\"" + "\" \"".join(units[n]) + "\""
        subprocess.run(f"zip -u {SUB_CODE}_Unit_{n}.zip {file_str}", shell=True)

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

def call_drive_api():
    # Shows basic usage of the Drive v3 API.
    # Prints the names and ids of the first 10 files the user has access to.

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
                print("credentials.json file not found... Go to https://console.cloud.google.com/apis/credentials/ and create an OAuth key, download it as json, and rename as 'credentials.json'")
            creds = flow.run_local_server(port=55000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Now everything after this runs inside the cs4401 directory (to make sure we don't change anything outside it)
    home_dir = os.getenv("HOME") or '/home'
    try:
        os.mkdir(home_dir + "/cs4401")
    except FileExistsError:
        print("cs4401 directory already exists... Continuing")

    os.chdir(home_dir + "/cs4401")

    # Getting folder id (of the name as in `notes_folder_name`variable)
    folders = service.files().list(
        q=f"mimeType='application/vnd.google-apps.folder' and name = '{notes_folder_name}'",
        pageSize=1, fields="files(id, name)").execute().get('files', [])
    notes_folder_id = folders[0]['id'] or '1oGKKT1DVB__792WIMvARUSFJkUqy2jWu'

    # Now we fetch list of all files inside the folder
    results = service.files().list(
        q=f"mimeType='application/pdf' and '{notes_folder_id}' in parents and name contains 'Lecture'",
        pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Iterate through all file names
    for item in items:
        print(u'{0} ({1})'.format(item['name'], item['id']))
        # the .get_media() provices us with a stream to download the files (We ONLY download files, whose names match the `file_name_regex` variable) 
        request = service.files().get_media(fileId=item['id'])
        if (file_name_regex.match(item['name']) != None) and not decrypted_file_exists(item['name']):
            result = request.execute()
            with open(item['name'], mode="wb") as fout:
                fout.write(result)

            decrypt_file(item['name'])
        else:
            # The file may have been something other the Lecture pdf
            print(f"Skipping {item['name']}")

    create_zips()

    if(os.getcwd() == os.getenv("HOME")):
        print("[WARNING] YOU MAY BE UPLOADING ALL FILES FROM HOME DIRECTORY ! WHICH CAN BE COSTLY")
        return

    subprocess.run(["gsutil", "-m", "cp", "*", f"{BUCKET_URI}/cs4401/"])

        # fh = io.BytesIo()
        # downloader = MediaIoBaseDownload(fh, request)
        # done = False
        # while done is False:
        #     status, done = downloader.next_chunk()
        #     print ("Download %d%%." , int(status.progress() * 100))

def NO_DRIVE_API():
    lecture_pdfs = []

    for file in next(os.walk('.'))[2]:
        if file_name_regex.match(file) != None:
            lecture_pdfs.append(file)

    try:
        os.mkdir("cs4401")
    except FileExistsError:
        print("cs4401 directory already exists... Continuing")

    print(" ".join(["gsutil", "-m", "cp", "-r", f"{BUCKET_URI}/cs4401", os.getcwd() + '/']))
    subprocess.run(["gsutil", "-m", "cp", "-r", f"{BUCKET_URI}/cs4401", os.getcwd() + '/'])

    # calling this for loop later, so that uploaded pdf take precedence over the one received from gsutil cp
    for pdf in lecture_pdfs:
        decrypt_file(pdf)
        os.rename(pdf, "cs4401/" + pdf)

    os.chdir("cs4401")
    create_zips()

    for pdf in lecture_pdfs:
        subprocess.run(["gsutil", "cp", pdf,f"{BUCKET_URI}/cs4401/"])

    subprocess.run(["gsutil", "-m", "mv", "*.zip", f"{BUCKET_URI}/cs4401/"])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        NO_DRIVE_API()
    else:
        call_drive_api()
