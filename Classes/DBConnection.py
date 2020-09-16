import json
from neo4j import GraphDatabase

class DBConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def deletePart(self, reference):
        with self.driver.session() as session:
            return session.write_transaction(self.deletePartFromDB, reference)

    @staticmethod
    def deletePartFromDB(session, reference):
        session.run(
            "match (n:PartDetails {reference: $reference}) detach delete n",
            reference=reference,
        )
        return session.run("match (n) where not (n)--() delete (n)").data()
