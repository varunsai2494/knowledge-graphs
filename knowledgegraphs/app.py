import recipe
import constants
import json
import keywords
import neo4jNodeList
import generic_functions as genFunc

conjunctionList=["and", "or", "but", "nor", "so", "for", "yet", "after", "although", "as", "as if", "as long as", "because", "before", "even if", "even though", "once", "since", "so that", "though", "till", "unless", "until", "what", "when", "whenever", "wherever", "whether", "while","."]

#function to split reviewtext at conjuctions into list of smaller sentences
# def sentenceBrokenAtConjunctions(rawtextAFterSpellCheck):
#     rawtextConjReplacedwithStar=rawtextAFterSpellCheck
#     for item in conjunctionList:
#         rawtextConjReplacedwithStar=(" "+rawtextConjReplacedwithStar+" ").lower().replace(str(" "+item+" ")," * ")
#     textSplitatStarList=rawtextConjReplacedwithStar.split(" * ")
#     return textSplitatStarList

def sentenceBrokenAtConjunctions(rawtextAFterSpellCheck):
    allNGrams = neo4jNodeList.getAllNodes()
    personNames = [str(item[0]) for item in allNGrams if item[1] == "Person"]
    movieNames = [str(item[2]) for item in allNGrams if item[1] == "Movie"]

    print movieNames

    doublematchperson = list(set(genFunc.doubleMatch(rawtextAFterSpellCheck,personNames)))
    doublematchmovie = list(set(genFunc.doubleMatchWithNoDuplicates(rawtextAFterSpellCheck,movieNames )))

    flag=True
    print doublematchmovie
    if doublematchmovie and len(doublematchmovie)==1:
        flag=False

    if flag:
        rawtextConjReplacedwithStar=rawtextAFterSpellCheck
        for item in conjunctionList:
            rawtextConjReplacedwithStar=(" "+rawtextConjReplacedwithStar+" ").lower().replace(str(" "+item+" ")," * ")
        textSplitatStarList=rawtextConjReplacedwithStar.split(" * ")
        return textSplitatStarList
    else:
        return[rawtextAFterSpellCheck]
#spellcheck on the list generated above
def spellcheck(rawtext):
    spellCheckResponse=recipe.callrecipe("spellcheck","azure",rawtext)
    return str(spellCheckResponse["corrected"])

#negation
def negation_sentence(text):
    filter= constants.filter
    for item in filter:
        text=text.replace(str(item),str(filter[item]))
    if " not " in text:
        d=constants.good_bad
        # with open('good_bad synonyms.json') as json_data:
        #     d = json.load(json_data)

        for k in ["good","bad"]:
            for i in d[k]:
                if " not " in text:
                    if str("not"+" "+ str(i)) in text:
                        complement={"good":"bad","bad":"good"}
                        text=text.replace(str("not"+" "+ str(i)),complement[str(k)])
                else:
                    break
    return text

def searchForperformance(string):
    good_bad_dictionary=constants.good_bad
    good=bad=neutral=[]
    good=genFunc.doubleMatch(string,good_bad_dictionary["good"])
    if good:
        return "good"
    else:
        bad=genFunc.doubleMatch(string,good_bad_dictionary["bad"])
        if bad:
            return "bad"
        else:
            neutral = genFunc.doubleMatch(string, good_bad_dictionary["neutral"])
            if neutral:
                return "neutral"
            else:
                return None

# def getLargestTokens(listOfCustomNers):
#     listOfNGramTokens = [] # Where N>1
#     for ner in listOfCustomNers:
#         if(len(ner.split(' ')) > 1):
#             listOfNGramTokens.append((ner))
#
#     for token in listOfNGramTokens:
#         subTokens = token.split(' ')
#         for subToken in subTokens:
#             if(subToken in listOfCustomNers):
#                 listOfCustomNers.remove(subToken)
#
#     return listOfCustomNers

def checkIfNgramInGraphDb(listOFNounGrams):
    outputList=[]
    SortedListOFNounGramsDesc = sorted(listOFNounGrams, key=lambda t: t.count(" "), reverse=True)
    graphDbNodes=neo4jNodeList.getAllNodes()
    nodeNames=[str(i[2]) if i[2] else str(i[0]) for i in graphDbNodes]
    for item in SortedListOFNounGramsDesc:
        if str(item).lower().strip() in nodeNames:
            check=any([True for i in outputList if str(item).lower() in str(i).lower()])
            if not check:
                outputList.append(str(item))
        # else:
        #     partialNodeSearch=[j for j in nodeNames if genFunc.doubleMatch(str(j), [x for x in item.split(" ") if x])]
        #     check = any([True for i in outputList if str(item).lower() in str(i).lower()])
        #     if not check:
        #         outputList.append(str(item))
    return outputList



def doubleMatchTheRelationWithMovie(sentence):
    relationsDict=constants.relationWithMovie
    doubleMatch=[]
    for item in relationsDict:
        doubleMatch=doubleMatch+[item for i in relationsDict[item] if str(" "+i+" ") in str(" "+sentence+" ")]
    return doubleMatch

def getUpdateNodesinfo(rawtext):
    rawtext=rawtext=rawtext.replace("."," . ").replace(","," , ").replace("'s","")
    # spellcheck on rawtext
    spellCheckText=spellcheck(rawtext)
    print spellCheckText

    # conjunction divide
    listOFSmallerSentences=sentenceBrokenAtConjunctions(spellCheckText)
    print listOFSmallerSentences

    # negation
    negatedListOFSmallerSentences=[negation_sentence(str(item)) for item in listOFSmallerSentences]
    print negatedListOFSmallerSentences

    # create ngrams
    # ngramDictsForSentences=[keywords.getngrams(item) for item in negatedListOFSmallerSentences]
    # print ngramDictsForSentences

    #check if ngram nouns in graphdb node names
    # nounNgramNodeNameMatchings=[checkIfNgramInGraphDb(item["NOUN"]) for item in ngramDictsForSentences]
    # print nounNgramNodeNameMatchings

    allNGrams=neo4jNodeList.getAllNodes()
    personNames=[item[0] for item in allNGrams if item[1]=="Person"]
    movieNames=[item[2] for item in allNGrams if item[1]=="Movie"]

    personnamesInSmallStrings=[genFunc.doubleMatch(str(item),personNames) for item in negatedListOFSmallerSentences]
    movienamesInsmallstrings=[genFunc.doubleMatchWithNoDuplicates(str(item),movieNames) for item in negatedListOFSmallerSentences]

    relationWithMovie=[doubleMatchTheRelationWithMovie(item) for item in listOFSmallerSentences]
    print relationWithMovie

    #to extract performance in smaller sentences
    performanceArray=[searchForperformance(item) for item in negatedListOFSmallerSentences]

    nodeDictionary=[[personnamesInSmallStrings[int(i)],movienamesInsmallstrings[int(i)],relationWithMovie[int(i)],performanceArray[int(i)]] for i in range(0,len(listOFSmallerSentences))]
    Query=""
    print nodeDictionary
    for item in nodeDictionary:
        persons=movie=relation=performance=None
        if item[0]:
            persons=item[0]
        if item[1]:
            movie=item[1][0]
        if item[2]:
            relation=item[2][0]
        if item[3]:
            performance=item[3]
        if performance:
            good = bad = neutral = 0
            if performance == "good":
                good = 1
            if performance == "bad":
                bad = 1
            if performance == "neutral":
                neutral = 1

            if persons and movie and relation:
                for person in persons:
                    query="match(n:Movie{title:'"+movie+"'})-[p:"+relation+"]->(m:Person{name:'"+person+"'}) set p.performance_good=p.performance_good+"+str(good)+",p.performance_bad=p.performance_bad+"+str(bad)+",p.performance_neutral=p.performance_neutral+"+str(neutral)+";"
                    Query=Query+query
            elif persons and movie:
                for person in persons:
                    query = "match(n:Movie{title:'" + movie + "'})-[p]->(m:Person{name:'" + person + "'}) set p.performance_good=p.performance_good+"+str(good)+",p.performance_bad=p.performance_bad+"+str(bad)+",p.performance_neutral=p.performance_neutral+"+str(neutral)+";"
                    Query=Query+query
            elif movie:
                query = "match(n:Movie{title:'" + movie + "'})-[p]->(m) set n.performance_good=n.performance_good+"+str(good)+",n.performance_bad=p.performance_bad+"+str(bad)+",n.performance_neutral=n.performance_neutral+"+str(neutral)+";"
                Query=Query+query
            else:
                Query=""
    return Query



# print neo4jNodeList.getAllNodes()



# b=getUpdateNodesinfo("i liked the dark knight")
# c=getUpdateNodesinfo("i liked  christian bale in the dark knight")

