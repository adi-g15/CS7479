import re

# Regex to filter Lecture pdfs
file_name_regex = re.compile(r"^Lecture \d+.*\.pdf$")

# jis folder me encrypted pdfs hai (in google drive)
drive_folder_name = "Lecture Handouts"

# jis folder me pdfs save honge (in google drive)
drive_folder_name_decrypted = drive_folder_name + " Decrypted"

# jis folder me pdfs save hoga (decrypted, local)
your_folder_name = "cs7479"

# To make it simpler, directly add password here
password = ""

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/drive.metadata.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.install']

MIMETYPES = {
    'FOLDER': 'application/vnd.google-apps.folder',
    'PDF': 'application/pdf'
}

