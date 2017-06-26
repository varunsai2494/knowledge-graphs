import requests
import json
# the word you want to search for
GL=["good"]
goodlist=[]
# increase the count and get more synonyms
count=2
for item in range(count):
    print item
    goodlist=list(set(GL))
    for j in goodlist:
        if " " not in j:
            print j
            urlg= "http://words.bighugelabs.com/api/2/83d0640747929c9e6b5ae66a2d24ca38/"+str(j)+"/json"
            result=requests.get(url=urlg)
            a= result.json()
            for i in a.keys():
                GL=GL+a[str(i)]["syn"]
finallist=list(set([str(i) for i in GL]))
print len(list(set(GL)))

