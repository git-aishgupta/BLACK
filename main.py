import credentials, queries, json
from flask import Flask
from urllib.request import urlopen
from flask_cors import CORS
from neo4j import GraphDatabase, basic_auth

app = Flask(__name__)
CORS(app)

HELLO_TEAM = "Hello Team!"


@app.route("/")
@app.route("/home")
def home():
    return HELLO_TEAM


@app.route("/getNodeData")
def about():
    jsonData = dbConnection.getNodeData()
    dbConnection.close()
    return jsonData


class DBConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def getNodeData(self):
        with self.driver.session() as session:
            return session.write_transaction(self.getData)

    @staticmethod
    def getData(session):
        nodes = session.run(queries.RETURN_ALL_DATA)
        data_list = []
        for record in nodes.data():
            data_list.append(record)
        return json.dumps(data_list)


dbConnection = DBConnection(
    credentials.Neo4J_URI, credentials.Neo4J_Username, credentials.Neo4J_Password
)

if __name__ == "__main__":
    app.run(debug=True)
