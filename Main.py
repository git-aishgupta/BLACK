import json
from Classes.GetNodeData import GetNodeData
from Constants import *
from flask import Flask
from urllib.request import urlopen
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
@app.route("/home")
def home():
    return HELLO_TEAM


@app.route("/getNodeData")
def getNodeData():
    return GetNodeData.getNodeData()


if __name__ == "__main__":
    app.run(debug=True)
