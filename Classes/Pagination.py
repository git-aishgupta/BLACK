import json
from flask import request

from Classes.DBConnection import DBConnection
from Utility.Credentials import *

dbConnection = DBConnection(
    Neo4J_URI, Neo4J_Username, Neo4J_Password
)

class Pagination:
    def getPagination(self):
        response = []
        offset = int(request.args.get('offset'))
        limit = int(request.args.get('limit'))
        offset = offset * 4
        result = dbConnection.getPagination(offset, limit)
        
        if not result:
            return None
        else:
            for i in result:
                for key in i:
                    response.append(i[key]) 
            return response