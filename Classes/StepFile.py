from googleapiclient.http import MediaFileUpload
from Classes.Google import Create_Service
from flask import request
from functools import partial
import csv
import re
import os
import math
import random
import csv
import operator

from Classes.DBConnection import DBConnection
from Utility.Credentials import *
from Classes.StepData import StepData
from Utility.Constants import *
from operator import itemgetter 
from urllib.request import urlopen
from Classes.EucDis import EucDis
from Classes.GetData import GetData
from Classes.GetResponse import GetResponse
from Classes.GetNeighbors import GetNeighbors
from Classes.GetAccuracy import GetAccuracy
# from Classes.CompareResult import CompareResult

dbConnection = DBConnection(
    Neo4J_URI, Neo4J_Username, Neo4J_Password
)

class StepFile:

    def uploadStepFile(self, filename, isCompare):
        file = request.files['stepfile']
        StepData.set_filename(self, filename)
        fileSupported = StepFile.stepFileHeaders(self)

        if not fileSupported:
            os.chdir(FILE_DIRECTORY)
            os.remove(filename)
            return None
        else:
            StepFile.partCategory(self)
            StepFile.findRadius(self)
            StepFile.googleDriveFileUpload(self, file)
            StepFile.updateCSVFile(self)
            return StepFile.aiTrainer(self, isCompare)
    
    def googleDriveFileUpload(self, file):
        filename = StepData.get_filename(self)
        mimetype = file.mimetype
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

            fileId = file.get('id')
            StepData.set_gdriveFileId(self, fileId)

    def findRadius(self):
        filename = StepData.get_filename(self)
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
        
        StepData.set_radius(self, radius)

    def updateCSVFile(self):
        fileDescription = StepData.get_fileDescription(self)
        filename = StepData.get_filename(self)
        manifoldSolidBrepCount = StepData.get_manifoldSolidBrepCount(self)
        totalPlaneSurfaces = StepData.get_totalPlaneSurfaces(self)
        radius = StepData.get_radius(self)
        category = StepData.get_category(self)
        gdriveFileId = StepData.get_gdriveFileId(self)

        serialNumber = 1
        StepData.set_serialNumber(self, serialNumber)
        try:
            with open('PartDetails.csv', 'r') as readFile:
                reader = csv.reader(readFile)
                serialNumber= len(list(reader))
                
                StepData.set_serialNumber(self, serialNumber)

                with open('PartDetails.csv', 'a', newline='') as csvFile:
                    fieldnames = ["SERIAL_NUMBER","FILE_DESCRIPTION", "FILENAME","MANIFOLD_SOLID_BREP","PLANE","RADIUS","CATEGORY","GDRIVE_FILE_ID"]
                    writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

                    writer.writerow({'SERIAL_NUMBER': serialNumber,"FILE_DESCRIPTION": fileDescription, "FILENAME": filename, 
                    "MANIFOLD_SOLID_BREP": manifoldSolidBrepCount, "PLANE": totalPlaneSurfaces, "RADIUS":radius,"CATEGORY":category,
                    "GDRIVE_FILE_ID": gdriveFileId})

        except FileNotFoundError:
            with open('PartDetails.csv', 'w', newline='') as csvFile:
                fieldnames = ["SERIAL_NUMBER","FILE_DESCRIPTION", "FILENAME","MANIFOLD_SOLID_BREP","PLANE","RADIUS","CATEGORY","GDRIVE_FILE_ID"]
                writer = csv.DictWriter(csvFile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'SERIAL_NUMBER': serialNumber,"FILE_DESCRIPTION": fileDescription, "FILENAME": filename, 
                "MANIFOLD_SOLID_BREP": manifoldSolidBrepCount, "PLANE": totalPlaneSurfaces, "RADIUS":radius,"CATEGORY":category,
                "GDRIVE_FILE_ID": gdriveFileId})
    
    def partCategory(self):
        totalPlaneSurfaces = StepData.get_totalPlaneSurfaces(self)
        if totalPlaneSurfaces == 4:
            StepData.set_category(self, SQ_NUT)
        elif totalPlaneSurfaces == 6:
            StepData.set_category(self, HEX_NUT)

    def stepFileHeaders(self):
        filename = filename = StepData.get_filename(self)
        manifoldSolidBrepCount = 0
        totalPlaneSurfaces = -2
        with open('./instance/uploads/'+filename) as openfileobject:
            for line in openfileobject:
                if "FILE_DESCRIPTION" in line:
                    fileDescription = re.search(r'\(\((.*?)\)(.*?)\)',line).group(1).split(",")[0]
                    StepData.set_fileDescription(self, fileDescription)
                elif "MANIFOLD_SOLID_BREP" in line:
                    manifoldSolidBrepCount = manifoldSolidBrepCount + 1
                    StepData.set_manifoldSolidBrepCount(self, manifoldSolidBrepCount)
                elif "=PLANE(" in line:
                    totalPlaneSurfaces = totalPlaneSurfaces + 1
                    StepData.set_totalPlaneSurfaces(self, totalPlaneSurfaces)

        if manifoldSolidBrepCount > 1:
            return False
        else:
            return True
        

    def aiTrainer(self, isCompare):
        fileDescription = StepData.get_fileDescription(self)
        filename = StepData.get_filename(self)
        manifoldSolidBrepCount = StepData.get_manifoldSolidBrepCount(self)
        totalPlaneSurfaces = StepData.get_totalPlaneSurfaces(self)
        radius = StepData.get_radius(self)
        category = StepData.get_category(self)
        gdriveFileId = StepData.get_gdriveFileId(self)
        serialNumber = StepData.get_serialNumber(self)

        #NEO4J DATA, data of the form  [radius,id,class]
        partClass = 1
        resultTrainSet = dbConnection.getradius(serialNumber, partClass, radius)
        # TODO : Megha
        
        testInstance = []
        if isCompare:
            # Compare
            arrayOutside = []
            for i in range(len(resultTrainSet)):
                arrayInside = []
                list1 = itemgetter(i)(resultTrainSet)
                listprep1 = (list1['n.radius'])
                arrayInside.append(listprep1)
                listprep11 = (list1['n.id'])
                arrayInside.append(listprep11)
                listprep12 = (list1['n.partClass'])
                arrayInside.append(listprep12)
                arrayOutside.append(arrayInside)
            trainSet = arrayOutside
        else:
            # Import
            trainSet = [[4,11,'1'], [1,12,'1'],[2,13,'1'],[3,14,'1'],[5,16,'2'],[7,10,'2'],[10,19,'3']]
            
        #getting radius from step file algorithm
        testInstance.append(radius)

        #    checking if id already exists , generate non repeating random number
        for i in range(len(trainSet)):
            list1 = itemgetter(i)(trainSet)
            list1_element1 = itemgetter(1)(list1)
            step_data_id = random.randint(20,200)
        if not step_data_id == list1_element1:
            testInstance.append(step_data_id)
            
        a = testInstance[0:1]
        #extracting first element of list to find class
        a = itemgetter(0)(testInstance)

        # 1-4 is class 1, 5-8 is class 2 , 9-12 is class 3
        if a > 1 and a <= 4 :
            partClass = '1'
        elif a > 4 and a <= 8:
            partClass = '2'
        elif a > 8 and a <= 12:
            partClass = '3'
        else : 
            partClass = '4'

        importResult = dbConnection.savePartDetails(serialNumber, fileDescription, filename, manifoldSolidBrepCount, totalPlaneSurfaces, radius, category, partClass, gdriveFileId)
        importData = []
        for item in importResult:
            importData.append(item['n'])

        # if compare:
        if isCompare:
            # TODO : change the value of kNearestNeighbours for more accuracy
            kNearestNeighbours = 3
            neighbors = GetNeighbors.getNeighors(self, trainSet , testInstance , kNearestNeighbours)
            #getting predicted class of data 
            response = GetResponse.getResponse(self, neighbors)   
            predictions= []
            predictions.append(response)

            #getting accuracy based on true class and predicted class
            # TODO : return to UI
            accuracy = GetAccuracy.getAccuracy(self, predictions,partClass)

            getClassResult = dbConnection.getclass(partClass)
            testInstance.append(partClass)

            trainSet.append(testInstance)
    
            

            # to Neo4j
            compareResult = dbConnection.getclass(partClass)
            compareData = []
            for item in compareResult:
                compareData.append(item['n'])

            originalPart = []
            similarParts = []
            for item in compareData:
                if item['reference'] == StepData.get_filename(self):
                    originalPart.append(item)
                else:
                    similarParts.append(item)

            return originalPart, similarParts, accuracy
        
        return importData