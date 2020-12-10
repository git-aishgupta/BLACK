from googleapiclient.http import MediaFileUpload
from Classes.Google import Create_Service

class StepFile:
    def importStepFile(self):
        CLIENT_SECRET_FILE='client_secrets.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        folder_id = '12E7toFhd_pKKZVVsPbbxIZkePTk8SVoh'

        file_names = ['07260-10.stp']
        mime_types = ['application/octet-stream']

        for file_name,mime_type in zip(file_names, mime_types):
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }

            media = MediaFileUpload('./{0}'.format(file_name), mimetype=mime_type)

            service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()