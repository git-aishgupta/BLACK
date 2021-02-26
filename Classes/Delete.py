import json
import os
from flask import request
from Utility.Constants import *

from Classes.DBConnection import DBConnection
from Utility.Credentials import *

dbConnection = DBConnection(
    Neo4J_URI, Neo4J_Username, Neo4J_Password
)

class Delete:
    def deletePart(self):
        req_data = request.get_json()
        pd = req_data["data"]["partDetail"]
        reference = pd["reference"]
        result = dbConnection.deletePart(reference)
        os.chdir(FILE_DIRECTORY)
        os.remove(reference)
        
        if result is None:
            return None
        else:
            return result
