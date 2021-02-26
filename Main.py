import os
import json
from flask import Flask
from urllib.request import urlopen
from flask_cors import CORS
from flask import request

from Classes.Delete import Delete
from Classes.Pagination import Pagination
from Utility.JsonResponse import JsonResponse
from Classes.StepFile import StepFile
from Utility.Constants import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from Classes.SearchPart import SearchPart

app = Flask(__name__)
CORS(app)

# Create a directory in a known location to save files to.
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)


@app.route(URI_BASE + "/deletePart", methods=["POST"])
def getDeletePartRequest():
    data = Delete().deletePart()
    return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

@app.route(URI_BASE + "/pagination", methods=["GET"])
def getPaginationRequest():
    data = Pagination().getPagination()
    return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

@app.route(URI_BASE + "/searchPart", methods=["POST"])
def getSearchPartRequest():
    data = SearchPart().partSearch()
    return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

@app.route(URI_BASE + "/stepfileupload", methods=["POST"])
def getStepFileUploadRequest():
    file = request.files['stepfile']
    compareFlag = request.form.get('compareFlag')

    if compareFlag == "true":
        isCompare = True
    else:
        isCompare = False

    os.chdir(FILE_DIRECTORY)
    fileExists = False
    for f in os.listdir():
        if file.filename == f:
            fileExists = True

    os.chdir(LOCAL_DIRECTORY)

    if fileExists:
        return JsonResponse.getResponse(None, DUPLICATE_PART, ERROR_CODE)
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(uploads_dir, filename))
        result = StepFile().uploadStepFile(filename, isCompare)
        data = result
        if data is not None:
            if isCompare:
                test_tup1 = ('originalPart', 'similarParts', 'accuracy') 
                data = dict(zip(test_tup1, result))
        
        if result == None:
            return JsonResponse.getResponse(data, MULTIPART_STEP_FILE, ERROR_CODE)
        else:
            return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

if __name__ == "__main__":
    app.run(debug=True)
