#!/usr/local/bin/python
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been tested in lab situations, all use cases cannot be accounted for.
# Date: 13-Feb-2018
# This scripts shows how to gather volume information by volumeID using requests and web calls
# output is in JSON formatted text.  This can be modified to be used in a more iterative fashion 
#   by switching from web calls to python CLI parsing
import requests
import base64
import json
import sys
from solidfire.factory import ElementFactory
# QoS is a dataobject model and must be imported to set QoS
# it is not required to get/print QoS information
from solidfire.models import QoS

if len(sys.argv) < 5:
    print("Insufficient arguments"
          "Usage python <script> <cluster> <username> <password> <volumeID,volumeID,volumeID>")

mvip_ip = sys.argv[1]
user_name = sys.argv[2]
user_pass = sys.argv[3]
vol_id = sys.argv[4]

def main():
    # Web/REST auth credentials build authentication
    auth = (user_name + ":" + user_pass)
    encodeKey = base64.b64encode(auth.encode('utf-8'))
    basicAuth = bytes.decode(encodeKey)

    # Be certain of your API version path here
    url = "https://" + mvip_ip + "/json-rpc/9.0"

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

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic %s" % basicAuth,
        'Cache-Control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)

    raw = json.loads(response.text)

    print(json.dumps(raw, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
