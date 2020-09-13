from Classes.DBConnection import DBConnection
from Utility.Credentials import *

dbConnection = DBConnection(
    Neo4J_URI, Neo4J_Username, Neo4J_Password
)


class GetNodeData:
    def getNodeData():
        jsonData = dbConnection.getNodeData()
        dbConnection.close()
        return jsonData
