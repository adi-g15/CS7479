from os import path, environ as env
from .config import MIMETYPES
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_authorization_cred(scopes):
    # Isme hum credentials rkhenge (ie. authorization token for your google account)
    credential = None

    # After first authorization attempt completes, we save it in token.json

    """
    TIP: Can pass content of token.json in environment variable: GDRIVETOKEN
         Although, if token.json is present, it will be used
    """

    if not path.exists('token.json') and env.get("GDRIVETOKEN") is not None:
        gdrivetoken = env.get("GDRIVETOKEN")
        with open("token.json", mode="w") as token_json:
            token_json.write(gdrivetoken)

    if path.exists('token.json'):
        credential = Credentials.from_authorized_user_file('token.json', scopes)
    elif path.exists('credentials.json'):
        # If there are no (valid) credentials available, let the user log in.
        credential = InstalledAppFlow.from_client_secrets_file(
                                    'credentials.json', scopes
                                ).run_local_server(port=55000)

    if credential and not credential.valid and credential.expired and credential.refresh_token:
        credential.refresh(Request())

    # If still credential not initialised/not found
    if not credential or not credential.valid:
        print("1. Go to https://console.cloud.google.com/apis/credentials")
        print("2. Create an OAuth key, download it as json")
        print("3. Move here and rename as 'credentials.json'")
        raise FileNotFoundError("credentials.json file not found...")

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(credential.to_json())

    return credential

# Create folder with name=folder_name, in root, no parent
# @return id: ID of the created folder
def create_folder(service, folder_name):
    # reference: https://stackoverflow.com/a/15362344/12339402
    body = {
        'name': folder_name,
        'mimeType': MIMETYPES['FOLDER']
    }
    result = service.files().create(body=body).execute()

    return result.get('id')

# Getting folder id (of the name as in `folder_name` variable)
def get_folder_id(service, folder_name):
    folder = service.files().list(
        q=f"mimeType='{MIMETYPES['FOLDER']}' and name = '{folder_name}' ",
        pageSize=1, fields="files(id, name)").execute().get('files', [])

    if len(folder) != 0:
        if folder[0]['name'] == folder_name:
            return folder[0]['id']

    return None

# Getting list of files (id,name) inside the folder referenced by folder id
def get_files(service, folder_id):
    request = service.files().list(
        q=f"mimeType='{MIMETYPES['PDF']}' and '{folder_id}' in parents",
        pageSize=50, fields="nextPageToken, files(id, name, md5Checksum)")

    return request.execute().get('files', [])

# Upload file with given filepath, inside given folder
def upload_file(service, parent_folder_id, file_name):
    request = service.files().create(
        body={
            'name': file_name,
            'mimeType': MIMETYPES['PDF'],
            'parents': [parent_folder_id],
            'description': f"Decrypted version of the lecture file {file_name}",
                #'isAppAuthorized': True,
                #'ownedByMe': True,
                #'capabilities': {
                #    "canShare": True,
                #},
            },
        #enforceSingleParent = True,
        #useContentAsIndexableText = True,
        media_body=file_name
    )

    return request.execute()

