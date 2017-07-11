import requests
import json
import jsonify

url="http://botman-v2-loadbalancer-1600796766.us-west-2.elb.amazonaws.com"


def callrecipe(nlpmodule,lib,text):

    body={
        "library": lib,
        "text":text }
    headers = {
        "content-type": "application/json"
    }
    r=requests.post(str(url+"/"+nlpmodule),headers=headers,json=body)
    print r
    return r.json()


