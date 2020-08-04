from Classes.DBConnection import DBConnection
import Credentials

dbConnection = DBConnection(
    Credentials.Neo4J_URI, Credentials.Neo4J_Username, Credentials.Neo4J_Password
)


class GetNodeData:
    def getNodeData():
        jsonData = dbConnection.getNodeData()
        dbConnection.close()
        return jsonData
