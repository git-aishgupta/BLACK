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

    def savePartDetails(self, serialNumber, fileDescription, filename, manifoldSolidBrepCount, totalPlaneSurfaces, radius, category, partClass, gdriveFileId):
        with self.driver.session() as session:
            return session.write_transaction(self.savePartDetailsToDB, serialNumber, fileDescription, filename, manifoldSolidBrepCount, totalPlaneSurfaces, radius, category, partClass, gdriveFileId)

    def getradius(self, serialNumber, partClass, radius):
            with self.driver.session() as session:
                return session.write_transaction(self.getradiusfromDB, serialNumber, radius, partClass)

    def getclass(self, partClass):
        with self.driver.session() as session:
            return session.write_transaction(self.getclassfromDB, partClass)

    def displaySearchData(self, query):
        with self.driver.session() as session:
            return session.write_transaction(self.getSearchDataFromDB, query)

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
    def savePartDetailsToDB(session, serialNumber, fileDescription, filename, manifoldSolidBrepCount, totalPlaneSurfaces, radius, category, partClass, gdriveFileId):
        session.run(
            "create (n:PartDetails {id: $serialNumber, reference: $filename , description: $fileDescription, manifold: $manifoldSolidBrepCount, plane: $totalPlaneSurfaces, radius: $radius, category: $category, partClass: $partClass, gdrive_id: $gdriveFileId}) merge (a:radi {rad: $radius}) merge (n)-[n_a:HAS_RADIUS]-(a) merge (b:cate {cat: $category}) merge (n)-[n_b:HAS_CATEGORY]-(b) merge (c:clas{cla: $partClass}) MERGE (a)-[n_c:HAS_CLASS]->(c)",
            serialNumber = serialNumber, filename = filename, fileDescription = fileDescription, manifoldSolidBrepCount = manifoldSolidBrepCount, totalPlaneSurfaces = totalPlaneSurfaces, radius = radius, category = category, gdriveFileId = gdriveFileId, partClass = partClass,
        )
        return session.run("match (n:PartDetails) where n.partClass = $partClass return n", partClass = partClass).data()

    @staticmethod
    def getradiusfromDB(session, serialNumber, radius, partClass):
        return session.run("match(n:PartDetails) return n.radius, n.id, n.partClass").data()

    @staticmethod
    def getclassfromDB(session, partClass):
        return session.run("match(n:PartDetails) where n.partClass = $partClass return n", partClass = partClass).data()

    @staticmethod
    def getSearchDataFromDB(session, query):
        return session.run(query).data()