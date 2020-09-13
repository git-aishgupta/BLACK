import json
from neo4j import GraphDatabase

import Utility.Queries


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
        nodes = session.run(Queries.RETURN_ALL_DATA)
        data_list = []
        for record in nodes.data():
            data_list.append(record)
        return json.dumps(data_list)
