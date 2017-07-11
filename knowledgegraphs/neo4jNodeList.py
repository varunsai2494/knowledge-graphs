from neo4j.v1 import GraphDatabase, basic_auth
import json
#function to return the list of all the nodes
driver = GraphDatabase.driver("bolt://localhost")
session = driver.session()

def getAllNodes():
    read_query = "MATCH (n) RETURN n.name as name,n.title as title,labels(n) as label"
    result=session.run(read_query)
    nodeList=[[str(record["name"]),record["label"][0],record["title"]] for record in result]
    print "There are currently "+str(len(nodeList)) +" nodes"
    return nodeList


def queryGraphDb(relation):
    a = "MATCH (n)-[p:" + relation +" ]->(m) RETURN m.name as name"
    result = session.run(a)
    nodeList = [record for record in result]
    return nodeList