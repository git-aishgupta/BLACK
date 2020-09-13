import json
from flask import Flask
from urllib.request import urlopen
from flask_cors import CORS

from Classes.GetNodeData import GetNodeData
from Classes.DeletePart import DeletePart
from Utility.JsonResponse import JsonResponse
from Utility.Constants import *

app = Flask(__name__)
CORS(app)

@app.route("/")
@app.route("/home")
def home():
    return HELLO_TEAM


@app.route("/getNodeData")
def getNodeData():
    return GetNodeData.getNodeData()

@app.route(URI_BASE + "/deletePart", methods=["POST"])
def getDeletePartRequest():
    data = DeletePart().partDeletion()
    return JsonResponse.getResponse(data, SUCCESS_MESSAGE, SUCCESS_CODE)

if __name__ == "__main__":
    app.run(debug=True)
