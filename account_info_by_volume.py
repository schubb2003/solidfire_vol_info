#!/usr/local/bin/python
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been tested in lab situations, all use cases cannot be accounted for.
# Script allows you to enter a volume ID and it will return the name and the account that owns the volume
# Date: 8-Jan-2019
# Updated: 9-Jan-2019
#	Allow multiple volumes to be entered and gathered at once


import requests
import base64
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-sm', type=str,
                    required=True,
                    metavar='mvip',
                    help='MVIP/node name or IP')
parser.add_argument('-su', type=str,
                    required=True,
                    metavar='username',
                    help='username to connect with')
parser.add_argument('-sp', type=str,
                    required=True,
                    metavar='password',
                    help='password for user')
parser.add_argument('-v', type=str,
                    required=True,
                    metavar='vol_id',
                    help='volume ID or comma separated list of IDs to return')
args = parser.parse_args()

mvip_ip = args.sm
user_name = args.su
user_pass = args.sp
vol_id = args.v

def main():
    # Web/REST auth credentials build authentication
    auth = (user_name + ":" + user_pass)
    encodeKey = base64.b64encode(auth.encode('utf-8'))
    basicAuth = bytes.decode(encodeKey)

    # Be certain of your API version path here
    url = "https://" + mvip_ip + "/json-rpc/9.0"

    # Various payload params in one liner
    # payload = "{\n\t\"method\": \"ListVolumes\",\n    \"params\": {\n        \"volumeIDs\": [<A list of volumeIDs>],\n        \"volumeName\": \"<Optional Volume Name>\",\n        \"isPaired\": <Return paired volumes: true, Return unpaired volumes: false>,\n        \"volumeStatus\": \"<creating, snapshotting, active, or deleted>\",\n        \"volumeName\": \"<Optional Volume Name>\",\n        \"includeVirtualVolumes\": <Boolean true or false>\n    },\n    \"id\": 1\n}"
    for vol in vol_id:
        if vol != ",":
            # payload in JSON multi-line
            payload = "{" + \
                            "\n  \"method\": \"ListVolumes\"," + \
                            "\n    \"params\": {" + \
                            "\n    \t\"volumeIDs\": [" + str(vol) + "]" + \
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

            #print(json.dumps(raw, indent=4, sort_keys=True))
            id_num = (raw['result']['volumes'][0]['accountID'])
            vol_name = (raw['result']['volumes'][0]['name'])

            payload_id = "{" + \
                               "\n  \"method\": \"GetAccountByID\"," + \
                               "\n    \"params\": {" + \
                               "\n    \t\"accountID\": " + str(id_num) + \
                               "\n    }," + \
                               "\n    \"id\": 1" + \
                               "\n}"

            response_id = requests.request("POST", url, data=payload_id, headers=headers, verify=False)
            raw_id = json.loads(response_id.text)
            account_name = raw_id['result']['account']['username']
            
            print("Volume ID is: {}\nVolume name is: {}\nUsername is: {}\n\n".format(vol,vol_name,account_name))
          
if __name__ == "__main__":
    main()
