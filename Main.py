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

@app.route(URI_BASE + "/stepfileupload", methods=["POST"])
def getStepFileUploadRequest():
    file = request.files['stepfile']
    try:
        with open('./instance/uploads/' + file.filename) as f:
            # file exists
            print(f)     
    except IOError:
        # file not exists
        file.save(os.path.join(uploads_dir, secure_filename(file.filename)))
        data = StepFile().uploadStepFile()

    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)
