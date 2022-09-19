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

from utils.pdf import decrypted_pdf_exists, decrypt_pdf, merge_pdfs
from utils.google import get_authorization_cred, create_folder, get_folder_id, get_files, upload_file
from utils.config import *
from googleapiclient.discovery import build as BuildService
import os
from os import environ as env
from os import sys
import hashlib

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

    # Filter out the Lecture Files (ie. those with .pdf extension and following file_name_regex)
    items = [item for item in items if (file_name_regex.match(item['name']) is not None)]

    printdebug("items: ", items)

    # Iterate through all file names
    for item in items:
        # .get_media() provides us with a request to download the file
        request = service.files().get_media(fileId=item['id'])

        if not decrypted_pdf_exists(item['name']):
            print(f"Info: Downloading {item['name']}")
            result = request.execute()

            with open(item['name'], mode="wb") as fout:
                fout.write(result)

            decrypt_pdf(item['name'], password)
        else:
            # The file may have been something other the Lecture pdf
            print(f"Info: Skipping {item['name']}. Already downloaded or decrypted")

    # Uploading decrypted files
    decrypted_notes_folder_id = get_folder_id(service, drive_folder_name_decrypted)

    if decrypted_notes_folder_id is None:
        print("Info: Creating remote google drive folder")
        decrypted_notes_folder_id = create_folder(service, drive_folder_name_decrypted)
    else:
        print("AlreadyExists: Remote google drive folder already exists. Continuing...")

    # Get existing files in the google drive decrypted folder
    remote_files = get_files(service, decrypted_notes_folder_id)
    printdebug("remote_files: ", remote_files)

    # Merge and upload lecture files into a `merged_notes_fname`
    # Skip "Lecture 0 [*]" since it contains just syllabus, not required in CombinedNotes :)
    lecture_files = [item["name"] for item in items if not item["name"].startswith("Lecture 0 [")]

    # Required to make sure the order is correct
    lecture_files.sort()

    printdebug("lecture_files: ", lecture_files)
    merge_pdfs(lecture_files, merged_notes_fname)
    uploaded_combined_notes = findElement(remote_files, merged_notes_fname)

    should_upload = True
    existing_fileid = None
    if uploaded_combined_notes is not None:
        # Since the file already exists, we need to replace, in case it is uploaded
        existing_fileid = uploaded_combined_notes["id"]

        # Check if our local file is the same as the one already uploaded
        should_upload = (uploaded_combined_notes["md5Checksum"] != md5sum(merged_notes_fname))
        printdebug("md5sum: ", md5sum(merged_notes_fname))

    if should_upload:
        printdebug(f"Uploading {merged_notes_fname}: ", os.path.abspath(merged_notes_fname))
        upload_file(service, decrypted_notes_folder_id, merged_notes_fname, existing_fileid)
    else:
        print(f"AlreadyExists: Same {merged_notes_fname} already exists. Continuing...")

    # Uploading lecture files
    already_uploaded_files = [item['name'] for item in remote_files]
    printdebug("already_uploaded_files: ", already_uploaded_files)

    # NOTE: Ignores any other file in the current directory
    for file in lecture_files:
        uploaded_file = findElement(remote_files, file)
        should_upload = True
        existing_fileid = None
        if uploaded_file is not None:
            existing_fileid = uploaded_file["id"]
            should_upload = (uploaded_file["md5Checksum"] != md5sum(file))

        if should_upload:
            print(f"Info: Uploading {file}")
            upload_file(service, decrypted_notes_folder_id, file, existing_fileid)
        else:
            print(f"Info: Skipping {file}. Already uploaded")

    return 0

def printdebug(*argv):
    if env.get("APP_DEBUG") is not None:
        print("\n[DEBUG]: ", argv, "\n")

def findElement(items, name):
    for item in items:
        if item['name'] == name:
            return item
    return None

# ref: https://stackoverflow.com/a/16876405/12339402
def md5sum(filename):
    with open(filename, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

if __name__ == '__main__':
    # Return with error code as returned by main
    # (0 if no error, 1 if error)
    # This helps fail the github action if anything went wrong
    sys.exit( main() )

