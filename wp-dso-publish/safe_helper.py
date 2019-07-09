__author__ = "Ilya Baldin"
__version__ = "0.1"
__maintainer__ = "Ilya Baldin"

import hashlib, base64
from Crypto.PublicKey import RSA
import requests

"""set of helper functions to interface with a SAFE server"""

SAFE_HTTP_POST_SUCCESS = 200
SAFE_RESULT_FIELD = "result"
SAFE_MESSAGE_FIELD = "message"
SAFE_SUCCESS = "succeed"

def hashKey(keyName):
    """ create a safe-compatible hash string of a public key file."""

    try:
        f = open(keyName, 'rb')
    except IOError:
        raise SafeException(f"Unable to read key file {keyName}")

    with f:
        try:
            r = RSA.importKey(f.read(), passphrase='')
        except:
            raise SafeException(f"Unable to parse key file: {keyName}")

        s = hashlib.sha256()
        s.update(r.exportKey(format='DER'))
        encoded = base64.urlsafe_b64encode(s.digest())

        return encoded.decode('utf-8')


def postRawIdSet(headUrl, principal):
    """ post a raw ID set of the principal """
    params = {"principal": principal, "methodParams": [principal]}
    resp = requests.post(headUrl + 'postRawIdSet', json=params)
    if resp.status_code != SAFE_HTTP_POST_SUCCESS:
        raise SafeException(f"Unable to post id set due to error: {resp.status_code}")

    json = resp.json()
    if json[SAFE_RESULT_FIELD] != SAFE_SUCCESS:
        raise SafeException(f"Failed to post id set due to error: {json[SAFE_MESSAGE_FIELD]}")
    return json[SAFE_MESSAGE_FIELD]

def postPerFlowRule(headUrl, principal, flowId):
    """ post a single per-workflow rule """
    params = {"principal": principal, "methodParams": [flowId]}
    resp = requests.post(headUrl + 'postPerFlowRule', json=params)
    if resp.status_code != SAFE_HTTP_POST_SUCCESS:
        raise SafeException(f"Unable to post workflow policy due to error: {resp.status_code}")

    json = resp.json()
    if json[SAFE_RESULT_FIELD] != SAFE_SUCCESS:
        raise SafeException(f"Failed to post workflow set due to error: {json[SAFE_MESSAGE_FIELD]}")
    return json[SAFE_MESSAGE_FIELD]

def postTwoFlowDataOwnerPolicy(headUrl, principal, dataset, wf1, wf2):
    """ post a ruleset for two workflows associated with the dataset """
    params = {"principal": principal, "methodParams": [dataset, wf1, wf2]}
    resp = requests.post(headUrl + 'postTwoFlowDataOwnerPolicy', json=params)
    if resp.status_code != SAFE_HTTP_POST_SUCCESS:
        raise SafeException(f"Unable to post dataset policy due to error: {resp.status_code}")

    json = resp.json()
    if json[SAFE_RESULT_FIELD] != SAFE_SUCCESS:
        raise SafeException(f"Failed to post dataset set due to error: {json[SAFE_MESSAGE_FIELD]}")
    return json[SAFE_MESSAGE_FIELD]

class SafeException(Exception):
    """ SAFE-related exception. Behaves like Exception """
    pass