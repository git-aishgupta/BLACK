import json
from flask import request

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
        if not result:
            return None
        else:
            return result
