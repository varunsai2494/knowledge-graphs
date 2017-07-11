import json
import constants
import app
import neo4jNodeList as neo

import generic_functions as genfunc
def determineTypeOfQuestion(question):
    questionWords=constants.questionWords.keys()
    typeOfQuestion=genfunc.doubleMatch(question,questionWords)
    if typeOfQuestion:
        return typeOfQuestion[0]
    else:
        return None

def determineidentifier(question,questionWord):
    questionWords=constants.questionWords
    conditionalChecks=questionWords[questionWord]
    identifier=None
    for key,value in conditionalChecks.iteritems():
        if genfunc.doubleMatch(question,value):
            identifier=key
            break
    return identifier

def determineRelationWithMovie(question):
    listOfRelations=app.doubleMatchTheRelationWithMovie(question)
    if listOfRelations:
        return app.doubleMatchTheRelationWithMovie(question)

def executeQuery(relation):
    return neo.queryGraphDb(relation)

def finalOutput(question):
    outputString=""
    relationsDict=constants.relationWithMovie
    questiontype=determineTypeOfQuestion(question)
    identifier=determineidentifier(question,questiontype)
    relationList=determineRelationWithMovie(question)
    if relationList:
        for item in list(set(relationList)):
            result=executeQuery(item)
            if len(result):
                if identifier and identifier=="plural":
                    partialOutput=str((",").join([i["name"] for i in result])+str(" "+relationsDict[item][0])+" this movie.\n")
                else:
                    partialOutput= str(result[0]["name"]+str(" "+relationsDict[item][0])+" this movie.\n")
            else:
                partialOutput=""
            outputString=outputString+partialOutput
    if outputString:
        return outputString
    else:
        return "Sorry I couldn't find what you are looking for"
print "asking one  name"
print finalOutput("who is the actor in Batman Begins")
print "asking multiple names"
print finalOutput("who are the actor in Batman Begins")
print "Asking without is/are/was/were"
print finalOutput("who directed Batman Begins")
print "asking multiple questions"
print finalOutput("who directed  batman begins and  list of all the actors")