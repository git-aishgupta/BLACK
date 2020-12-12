import json
from neo4j import GraphDatabase

class DBConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def deletePart(self, reference):
        with self.driver.session() as session:
            return session.write_transaction(self.deletePartFromDB, reference)

    def getPagination(self, offset, limit):
        with self.driver.session() as session:
            return session.write_transaction(self.getPaginationFromDB, offset, limit)

    def savePartDetails(self, filename, gdriveFileId):
        with self.driver.session() as session:
            return session.write_transaction(self.savePartDetailsToDB, filename, gdriveFileId)

    @staticmethod
    def deletePartFromDB(session, reference):
        session.run(
            "match (n:PartDetails {reference: $reference}) detach delete n",
            reference = reference,
        )
        return session.run("match (n) where not (n)--() delete (n)").data()
    
    @staticmethod
    def getPaginationFromDB(session, offset, limit):
        return session.run(
            "match (n:PartDetails) return n order by n.reference skip $offset limit $limit",
            offset = offset, limit = limit,
        ).data()

    @staticmethod
    def savePartDetailsToDB(session, filename, gdriveFileId):
        return session.run(
            "create (n:PartDetails {reference: $filename , gdrive_id: $gdriveFileId}) merge (gd:GoogleDrive {gdrive_id: $gdriveFileId}) merge (n)-[n_gd:HAS_FILE_ID]-(gd)",
            filename = filename, gdriveFileId = gdriveFileId,
        ).data()