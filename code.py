#!/usr/bin/python3

# NOTE- Agar bas apne computer pe use karna hai to use `src/scripts/simple_decrypt.py`
#       Ye wo actual script hai jo `https://cs4401.netlify.app` ko update karta hai naya pdf se, plus zip files bhi create karta hai, unit wise

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.cloud import storage
from PyPDF3 import PdfFileReader, PdfFileWriter
from zipfile import ZipFile
from glob import glob
import os.path
import re
import sys

# Ye install karlo before running this script
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib google-cloud-storage PyPDF3

file_name_regex = re.compile(r"^Lecture \d+.*Unit.*\.pdf")
drive_folder_name = "Lecture Handouts"
your_folder_name  = "cs4401"     # jis folder me pdfs save hoga (decrypted)
password = "nitp_cs4401-Spr21"   # or any other password your notes has

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/devstorage.read_write']
BUCKET_ID  = "assignment-7d2c8.appspot.com"
BUCKET_URI = f"gs://{BUCKET_ID}"

DONT_ASK_FOR_UPLOAD_CONFIRMATION = False    # When running this script somewhere when you don't have internet limitations, set this True (since you may need to upload about ~100 MB in total)

# pre-condition: Current directory is same as the notes directory
def create_zips():
    SUB_CODE = 'CS4401_COA'

    with ZipFile(f"{SUB_CODE}_All.zip", "w") as all_notes:
        for filename in next(os.walk('.'))[2]:
            if file_name_regex.match(filename) != None:
                print(f"Adding {filename} in {SUB_CODE}_All.zip")
                all_notes.write(filename)

    files = next(os.walk('.'))[2]
    iter = filter(lambda file: file_name_regex.match(file) != None, files)
    files = list(iter)

    units = {'I': [], 'II': [], 'III': [], 'IV': []}

    for n in units:
        units[n] = [file for file in files if file.find(f"Unit {n} -") != -1]

        if len(units[n]) == 0:
            continue

        print(f"Adding {len(units[n])} files in {SUB_CODE}_Unit_{n}.zip")
        with ZipFile(f"{SUB_CODE}_Unit_{n}.zip", "w") as unit_zip:
            for filename in units[n]:
                unit_zip.write(filename)

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

    if reader.getIsEncrypted() == False:
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

# Iska jarurat nahi hoga, agar sirf offline use ke liye chahiye, see the "simple_decrypt.py" for that :D
# ref: https://stackoverflow.com/questions/48514933/how-to-copy-a-directory-to-google-cloud-storage-using-google-cloud-python-api#52193880
def upload_files_to_gcs(file_list, bucket, gcs_path):
    for file in file_list:
        if os.path.isfile(file):
            if file_name_regex.match(file):
                remote_path = os.path.join(gcs_path, file)
                blob = bucket.blob(remote_path) # create blob (for yet non-existing file)
                if not blob.exists():
                    print(f"Uploading {file}... ", end='')
                    blob.upload_from_filename(file) # blob.upload_from_filename()  upload contents from local file
                    print("Done")
            elif file[-4:] == ".zip":
                remote_path = os.path.join(gcs_path, file)
                blob = bucket.blob(remote_path)

                if DONT_ASK_FOR_UPLOAD_CONFIRMATION or input(f"Upload {file}  (y/n) ? ") == 'y':
                    print(f"Uploading {file}... ", end='')
                    blob.upload_from_filename(file) # blob.upload_from_filename()  upload contents from local file
                    print("Done")

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
                return
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

    create_zips()

    client = storage.Client(project=None, credentials=creds)
    lecture_bucket = client.get_bucket(BUCKET_ID)
    upload_files_to_gcs(glob("*"), lecture_bucket, "cs4401/")

if __name__ == '__main__':
    if sys.argv.count('-y') != 0:
        DONT_ASK_FOR_UPLOAD_CONFIRMATION = True
    main()
