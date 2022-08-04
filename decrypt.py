#!/usr/bin/python3

"""
# Steps to use:

> ## Pehli baar ye steps bhi krna hoga:
> 1. pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib PyPDF3
> 2. Go to https://console.cloud.google.com/apis/credentials/
> 3. Create an OAuth key, download it as json, copy in this folder and rename as 'credentials.json

1. Run `python decrypt.py`
2. Chose nit patna email id (ie. the email id that has access to the files)

"""

from utils.pdf import decrypted_pdf_exists, decrypt_pdf
from utils.google import get_authorization_cred, create_folder, get_folder_id, get_files, upload_file
from utils.config import *
from googleapiclient.discovery import build as BuildService
import os
from os import environ as env

"""
To edit variables such as password, folder names, etc. edit utils/config.py
"""

def main():
    global password
    if password == "":
        if env.get("PASSWD") is not None:
            password = env.get("PASSWD")
        else:
            print("[WARN] Password not set:")
            print("Please set `password` in the code (or PASSWD environment variable)")

    try:
        cred = get_authorization_cred(SCOPES)
    except FileNotFoundError as e:
        print("FileNotFoundError:", e)
        return 1

    service = BuildService('drive', 'v3', credentials=cred)

    try:
        os.mkdir(your_folder_name)
    except FileExistsError:
        print(f"AlreadyExists: {your_folder_name} directory already exists... Continuing")

    # Now everything after this runs inside the `your_folder` directory
    # (to make sure we don't change anything outside it)
    os.chdir(your_folder_name)

    notes_folder_id = get_folder_id(service, drive_folder_name)
    printdebug("notes_folder_id: ", notes_folder_id)

    if notes_folder_id is None:
        print(f"NotFoundError: {drive_folder_name} not found, in your Google Drive")
        print("TIP: Can use the 'Add a shortcut to drive' option on the shared folder")
        return 1

    # Now we fetch list of all files inside the folder
    items = get_files(service, notes_folder_id)

    printdebug("items: ", items)

    # Iterate through all file names
    for item in items:
        # .get_media() provides us with a request to download the file
        request = service.files().get_media(fileId=item['id'])

        if (file_name_regex.match(item['name']) != None) and not decrypted_pdf_exists(item['name']):
            print(f"Info: Downloading {item['name']}")
            result = request.execute()

            with open(item['name'], mode="wb") as fout:
                fout.write(result)

            decrypt_pdf(item['name'])
        else:
            # The file may have been something other the Lecture pdf
            print(f"Info: Skipping {item['name']}. Already downloaded or not a lecture pdf")

    # Uploading decrypted files
    decrypted_notes_folder_id = get_folder_id(service, drive_folder_name_decrypted)

    if decrypted_notes_folder_id is None:
        print("Info: Creating remote google drive folder")
        decrypted_notes_folder_id = create_folder(service, drive_folder_name_decrypted)
    else:
        print("AlreadyExists: Remote google drive folder already exists. Continuing...")

    already_uploaded_files = get_files(service, decrypted_notes_folder_id)
    printdebug("already_uploaded_files: ", already_uploaded_files)

    # iterate over all files in current directory
    for file in os.listdir():
        found = False
        for uploaded_file in already_uploaded_files:
            if uploaded_file['name'] == file:
                found = True
                break

        if found == False:
            print(f"Uploading {file}")
            upload_file(service, decrypted_notes_folder_id, file)
        else:
            print(f"Skipping {file}. Already uploaded")

def printdebug(*argv):
    if env.get("APP_DEBUG") is not None:
        print("\n[DEBUG]: ", argv, "\n")

if __name__ == '__main__':
    main()
