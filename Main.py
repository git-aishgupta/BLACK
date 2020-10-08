import json
from flask import Flask
from urllib.request import urlopen
from flask_cors import CORS

from Classes.Delete import Delete
from Classes.Pagination import Pagination
from Utility.JsonResponse import JsonResponse
from Utility.Constants import *

app = Flask(__name__)
CORS(app)

@app.route(URI_BASE + "/deletePart", methods=["POST"])
def getDeletePartRequest():
    data = Delete().deletePart()
    return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

@app.route(URI_BASE + "/pagination", methods=["GET"])
def getPaginationRequest():
    data = Pagination().getPagination()
    return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

if __name__ == "__main__":
    app.run(debug=True)
