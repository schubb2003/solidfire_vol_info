#!/usr/local/bin/python
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been tested in lab situations, all use cases cannot be accounted for.
# Date: 13-Feb-2018
# This scripts shows how to gather volume information on volumeID 1 using requests and web calls
# output is in JSON formatted text.  This can be modified to be used in a more iterative fashion 
#   by switching from web calls to python CLI parsing
import requests
import base64
import json
import argparse
from solidfire.factory import ElementFactory
# QoS is a dataobject model and must be imported to set QoS
# it is not required to get/print QoS information
from solidfire.models import QoS

def get_inputs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', type=str,
                        required=True,
                        metavar='mvip',
                        help='MVIP/node name or IP')
    parser.add_argument('-u', type=str,
                        required=True,
                        metavar='username',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=True,
                        metavar='password',
                        help='password for user')
    parser.add_argument('-v', type=str,
                        required=True,
                        metavar='vol_id',
                        help='volume ID or comma separated list of IDs to return')
    args = parser.parse_args()

    mvip_ip = args.m
    user_name = args.u
    user_pass = args.p
    vol_id = args.v
    
    return mvip_ip, user_name, user_pass, vol_id
    
def build_auth(mvip_ip, user_name, user_pass):
    auth = (user_name + ":" + user_pass)
    encodeKey = base64.b64encode(auth.encode('utf-8'))
    basicAuth = bytes.decode(encodeKey)

    # Be certain of your API version path here
    url = "https://" + mvip_ip + "/json-rpc/9.0"
    
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic %s" % basicAuth,
        'Cache-Control': "no-cache",
        }

    return headers, url

def get_vol_info(headers, url, vol_id):
    # Web/REST auth credentials build authentication


    # Various payload params in one liner
    # payload = "{\n\t\"method\": \"ListVolumes\",\n    \"params\": {\n        \"volumeIDs\": [<A list of volumeIDs>],\n        \"volumeName\": \"<Optional Volume Name>\",\n        \"isPaired\": <Return paired volumes: true, Return unpaired volumes: false>,\n        \"volumeStatus\": \"<creating, snapshotting, active, or deleted>\",\n        \"volumeName\": \"<Optional Volume Name>\",\n        \"includeVirtualVolumes\": <Boolean true or false>\n    },\n    \"id\": 1\n}"

    # payload in JSON multi-line
    payload = "{" + \
                    "\n  \"method\": \"ListVolumes\"," + \
                    "\n    \"params\": {" + \
                    "\n    \t\"volumeIDs\": [" + str(vol_id) + "]" + \
                    "\n    }," + \
                    "\n    \"id\": 1" + \
                "\n}"

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)

    raw = json.loads(response.text)

    print(json.dumps(raw, indent=4, sort_keys=True))

def main():
    mvip_ip, user_name, user_pass, vol_id = get_inputs()
    headers, url = build_auth(mvip_ip, user_name, user_pass)
    get_vol_info(headers, url, vol_id)

if __name__ == "__main__":
    main()
