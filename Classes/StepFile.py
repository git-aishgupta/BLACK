from googleapiclient.http import MediaFileUpload
from Classes.Google import Create_Service
from flask import request

class StepFile:
    def uploadStepFile(self):
        file = request.files['stepfile']
        file_filename = file.filename
        file_mimetype = file.mimetype
        
        CLIENT_SECRET_FILE='client_secrets.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        # id of the google drive folder in which you want to save the file. Fetch it from the folder URL.
        folder_id = '12E7toFhd_pKKZVVsPbbxIZkePTk8SVoh'

        file_names = [file_filename]
        mime_types = [file_mimetype]

        for file_name,mime_type in zip(file_names, mime_types):
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }

            # Upload file to GDrive from local storage at /instance/uploads/filename
            media = MediaFileUpload('./instance/uploads/{0}'.format(file_name), mimetype=mime_type)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            # print("file id : " + file.get('id'))
            # save filename, file id in neo4j database
            print("Google Drive link: https://drive.google.com/file/d/"+ file.get('id') +"/view")