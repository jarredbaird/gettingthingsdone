import json, base64

def subPub(request_args):
    # get the request from the subscription to the email topic 
    subRequest = json.loads(request_args)
    # convert message.data from a b64-like string to a decoded string
    subPubDataByteLikeString = subRequest['message']['data']
    subPubDataB64 = subPubDataByteLikeString.encode('utf-8')
    return json.loads(base64.b64decode(subPubDataB64).decode('utf-8'))