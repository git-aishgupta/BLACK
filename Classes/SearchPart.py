import json
from flask import request

from Classes.DBConnection import DBConnection
from Utility.Credentials import *

dbConnection = DBConnection(
    Neo4J_URI, Neo4J_Username, Neo4J_Password
)

class SearchPart:
    def partSearch(self):  
        req_data = request.get_json()
        #extracting data from json request
        data = req_data["data"]

        searchPart = data["searchPart"]
        limit = data["limit"]
        pageNumber = data["pageNumber"]
        offset = limit * (pageNumber - 1)

        inputValue = searchPart["input"]
        filterType = searchPart["filter"]
        category = searchPart["category"]
        sortBy = searchPart["sortBy"]

        matchClause = "match (n:PartDetails)"
        query = matchClause

        if filterType == None:
            print()
        elif filterType.upper() == 'TITLE':
            filterClause = ' where n.reference=~\"(?i)' + inputValue + '\"'
            query = query + filterClause
        elif filterType.upper() == 'RADIUS':
            filterClause = " where n.radius = " + inputValue
            query = query + filterClause

        if category == None:
            print()
        else:
            if filterType == None:
                categoryClause = ' where n.category=\"' + category + '\"'
            else:
                categoryClause = ' and n.category=\"' + category + '\"'

            query = query + categoryClause

        returnClause = " return n "
        query = query + returnClause

        orderbyClause = "order by "
        if sortBy == None:
            print()
        elif sortBy.upper() == "TITLE":
            orderbyClause = orderbyClause + "n.reference"
            query = query + orderbyClause
        elif sortBy.upper() == "RADIUS":
            orderbyClause = orderbyClause + "n.radius"
            query = query + orderbyClause

        paginationClause = " skip " + str(offset) + " limit " + str(limit)
        query = query + paginationClause
        result = dbConnection.displaySearchData(query)
        data = []
        for item in result:
            data.append(item['n'])
        
        return data
