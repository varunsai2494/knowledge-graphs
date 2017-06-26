import recipe
import json
#getting the verbs,noun grams,adjectives and pronouns
def tagwords(recipeoutput):
    tagwordsdictionary={}
    if "pos" in recipeoutput:
        print "123"
        for item in recipeoutput["pos"]:
            if item["pos_tag"] in ["NOUN","VERB","ADJECTIVE","PRONOUN"]:
                if item["pos_tag"] in tagwordsdictionary:
                    tagwordsdictionary[item["pos_tag"]].append(str(item["word"]))
                else:
                    tagwordsdictionary[item["pos_tag"]]=[str(item["word"])]
        l=int(len(recipeoutput["pos"]))
        for i in range(int(l)):
            if i == l-1:
                break
            elif recipeoutput["pos"][i]["pos_tag"] == "NOUN":
                for j in range(i,l):
                    print "123"
                    if recipeoutput["pos"][j]["pos_tag"] == "NOUN":
                        g=[k["word"] for k in recipeoutput["pos"][i:j+1]]
                        print g
                        tagwordsdictionary["NOUN"].append(str(" ".join(g)))
                    else:
                        break

    return tagwordsdictionary

#recipe pos call
def getngrams(text):
    recipeoutput =recipe.callrecipe("pos","spacy",text)
    if recipeoutput:
        return tagwords(recipeoutput)
    else:
        return None

#negation
def negation_sentence(text):
    filter= { "don't":"do not",
        "cant":"can not",
        "wasn't":"was not",
        "hasn't":"has not",
        "shouldn't":"should not",
        "shan't":"shall not",
        "wouldn't":"would not",
        "hadn't":"had not",
        "haven't":"have not",
        "weren't":"were not",
        "oughtn't":"ought not",
        "ain't":"is not",
        "couldn't":"could not",
        "won't":"will not",
        "mayn't":"may not",
        "mightn't":"might not",
        "dont":"do not",
        "can't":"can not",
        "cannot":"can not",
        "wasnt":"was not",
        "hasnt":"has not",
        "shouldnt":"should not",
        "shant":"shall not",
        "wouldnt":"would not",
        "hadnt":"had not",
        "havent":"have not",
        "werent":"were not",
        "oughtnt":"ought not",
        "aint":"is not",
         "couldnt":"could not",
         "wont":"will not",
         "maynt":"may not",
         "mightnt":"might not",
         "didn't":"did not",
          "didnt":"did not"}
    for item in filter:
        text=text.replace(str(item),str(filter[item]))
    if " not " in text:
        with open('good_bad synonyms.json') as json_data:
            d = json.load(json_data)
    for k in ["good","bad"]:
        for i in d[k]:
            if " not " in text:
                if str("not"+" "+ str(i)) in text:
                    text=text.replace(str("not"+" "+ str(i)),"bad")
            else:
                break
    return text

#to get all the verbs,n grams of nouns (n<=10),adj,pronouns
print getngrams("apple banana pineapple cat mouse")
print negation_sentence("i dont good  apples")