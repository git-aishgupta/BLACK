from googleapiclient.http import MediaFileUpload
from Classes.Google import Create_Service
from flask import request
from functools import partial
import csv
import re

from Classes.DBConnection import DBConnection
from Utility.Credentials import *

dbConnection = DBConnection(
    Neo4J_URI, Neo4J_Username, Neo4J_Password
)

class StepFile:
    def uploadStepFile(self):
        file = request.files['stepfile']
        filename = file.filename
        mimetype = file.mimetype
        

        uploadedFile = StepFile.googleDriveFileUpload(self,filename,mimetype)
        gdriveFileId = uploadedFile.get('id')

        # fetch important data out of STEP file
        manifoldSolidBrepCount = 0
        totalPlaneSurfaces = -2
        with open('./instance/uploads/'+filename) as openfileobject:
            for line in openfileobject:
                if "FILE_DESCRIPTION" in line:
                    fileDescription = re.search(r'\(\((.*?)\)(.*?)\)',line).group(1).split(",")[0]
                elif "MANIFOLD_SOLID_BREP" in line:
                    manifoldSolidBrepCount = manifoldSolidBrepCount + 1
                elif "=PLANE(" in line:
                    totalPlaneSurfaces = totalPlaneSurfaces + 1

        if manifoldSolidBrepCount > 1:
            print(manifoldSolidBrepCount)
            return None
        else:
            print("success brep")
        
        if totalPlaneSurfaces == 4:
            category = "SQUARE NUT"
        elif totalPlaneSurfaces == 6:
            category = "HEXAGONAL NUT"
    
        radius = StepFile.findRadius(self, filename)

        StepFile.updateCSVFile(self, fileDescription, filename, 
                    manifoldSolidBrepCount, totalPlaneSurfaces, radius,category,
                    gdriveFileId)
        

        # save filename, file id in neo4j database
        result = dbConnection.savePartDetails(filename, gdriveFileId)
        if not result:
            return None
        else:
            return result
    
    def googleDriveFileUpload(self, filename, mimetype):
        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        for filename,mimetype in zip([filename], [mimetype]):
            file_metadata = {
                'name': filename,
                'parents': [GOOGLE_DRIVE_FOLDER_ID]
            }

            # Upload file to GDrive from local storage at /instance/uploads/filename
            media = MediaFileUpload('./instance/uploads/{0}'.format(filename), mimetype=mimetype)

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            return file

    def findRadius(self, filename):
        with open('./instance/uploads/'+filename) as openfileobject:
            for l, line in enumerate(openfileobject,1):
                if "=ADVANCED_FACE(" in line:
                    adfs = re.search(r'\((.*?)\((.*?)\)(.*?)\)',line).group(2).split(",")
                    if len(adfs) == 2:
                        advancedFace = adfs[1]
                        for m, linet in enumerate(openfileobject,l+1):
                            if advancedFace in linet:
                                facebound = re.search(r'\((.*?)\)',linet).group(1).split(",")[1]
                                break
                        for n, linett in enumerate(openfileobject, m+1):
                            if facebound in linett:
                                edgeloop = re.search(r'\((.*?)\((.*?)\)(.*?)\)',linett).group(2).split(",")[0]
                                break
                        for o, linettt in enumerate(openfileobject, n+1):
                            if edgeloop in linettt:
                                orientededge =  re.search(r'\((.*?)\)',linettt).group(1).split(",")[3]
                                break
                        for p, linetttt in enumerate(openfileobject,o+1):
                            if orientededge in linetttt:
                                edgecurve =  re.search(r'\((.*?)\)',linetttt).group(1).split(",")[3]
                                break  
                        for q, linettttt in enumerate(openfileobject, p+1):
                            if edgecurve in linettttt:
                                circle =  re.search(r'\((.*?)\)',linettttt).group(1).split(",")
                                radius = round(float(circle[2]),2)
                                break
        
        return radius

    def updateCSVFile(self, fileDescription, filename, 
                    manifoldSolidBrepCount, totalPlaneSurfaces, radius,category,
                    gdriveFileId):
        try:
            serialNumber = 1
            with open('PartDetails.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                lines= len(list(reader))
                serialNumber = lines

                with open('PartDetails.csv', 'a', newline='') as csvFile:
                    fieldnames = ["SERIAL_NUMBER","FILE_DESCRIPTION", "FILENAME","MANIFOLD_SOLID_BREP","PLANE","RADIUS","CATEGORY","GDRIVE_FILE_ID"]
                    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

                    writer.writerow({'SERIAL_NUMBER': serialNumber,"FILE_DESCRIPTION": fileDescription, "FILENAME": filename, 
                    "MANIFOLD_SOLID_BREP": manifoldSolidBrepCount, "PLANE": totalPlaneSurfaces, "RADIUS":radius,"CATEGORY":category,
                    "GDRIVE_FILE_ID": "https://drive.google.com/file/d/" + gdriveFileId + "/view"})

        except FileNotFoundError:
            with open('PartDetails.csv', 'w', newline='') as csvFile:
                fieldnames = ["SERIAL_NUMBER","FILE_DESCRIPTION", "FILENAME","MANIFOLD_SOLID_BREP","PLANE","RADIUS","CATEGORY","GDRIVE_FILE_ID"]
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'SERIAL_NUMBER': 1,"FILE_DESCRIPTION": fileDescription, "FILENAME": filename, 
                "MANIFOLD_SOLID_BREP": manifoldSolidBrepCount, "PLANE": totalPlaneSurfaces, "RADIUS":radius,"CATEGORY":category,
                "GDRIVE_FILE_ID": "https://drive.google.com/file/d/" + gdriveFileId + "/view"})