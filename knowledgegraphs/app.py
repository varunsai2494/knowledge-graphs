import recipe
import constants
import json
import keywords
import neo4jNodeList

conjunctionList=["and", "or", "but", "nor", "so", "for", "yet", "after", "although", "as", "as if", "as long as", "because", "before", "even if", "even though", "once", "since", "so that", "though", "till", "unless", "until", "what", "when", "whenever", "wherever", "whether", "while","."]

#function to split reviewtext at conjuctions into list of smaller sentences
def sentenceBrokenAtConjunctions(rawtextAFterSpellCheck):
    rawtextConjReplacedwithStar=rawtextAFterSpellCheck
    for item in conjunctionList:
        rawtextConjReplacedwithStar=(" "+rawtextConjReplacedwithStar+" ").lower().replace(str(" "+item+" ")," * ")
    textSplitatStarList=rawtextConjReplacedwithStar.split(" * ")
    return textSplitatStarList

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
    return outputList

def doubleMatchTheRelationWithMovie(sentence):
    relationsDict=constants.relationWithMovie
    doubleMatch=[]
    for item in relationsDict:
        doubleMatch=doubleMatch+[item for i in relationsDict[item] if str(" "+i+" ") in str(" "+sentence+" ")]
    return doubleMatch

def getUpdateNodesinfo(rawtext):

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
    ngramDictsForSentences=[keywords.getngrams(item) for item in negatedListOFSmallerSentences]
    print ngramDictsForSentences

    #check if ngram nouns in graphdb node names
    nounNgramNodeNameMatchings=[checkIfNgramInGraphDb(item["NOUN"]) for item in ngramDictsForSentences]
    print nounNgramNodeNameMatchings


    relationWithMovie=[doubleMatchTheRelationWithMovie(item) for item in listOFSmallerSentences]
    print relationWithMovie

    nodeDictionary=[[nounNgramNodeNameMatchings[int(i)],relationWithMovie[int(i)]] for i in range(0,len(listOFSmallerSentences))]
    print nodeDictionary

    return nodeDictionary




