#!/usr/bin/python3
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the naaid or volume ID of a volume depending on which parameter you provide

import json
import base64
import argparse
import requests
from getpass import getpass
from prettytable import PrettyTable

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
                        required=False,
                        metavar='password',
                        help='password for user')
    parser.add_argument('-i', type=int,
                        required=False,
                        metavar='vol_id',
                        help='vol id to search on')
    parser.add_argument('-s', type=str,
                        required=False,
                        metavar='naa_id',
                        help='naaid to search on')                    
    args = parser.parse_args()

    mvip = args.m
   user = args.u
    naa_id = args.s
    vol_id = args.i
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p
    
    return mvip, user, user_pass, naa_id, vol_id

def build_auth(mvip, user, user_pass):
    auth = (user + ":" + user_pass)
    encodeKey = base64.b64encode(auth.encode('utf-8'))
    basicAuth = bytes.decode(encodeKey)

    # Be certain of your API version path here
    url = "https://" + mvip + "/json-rpc/9.0"
    
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic %s" % basicAuth,
        'Cache-Control': "no-cache",
        }

    return headers, url    

def build_payload():
    payload = json.dumps({"method": "ListActiveVolumes","params":{"startVolumeID": 1},"id": 1})
    #payload = json.dumps({"method": "ListReports","params":{},"id": 1})
    return payload
    
def connect_cluster(headers, url, payload):
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    response_json = json.loads(response.text)
    print
    return response_json

def compare_scsi_id(response_json, naa_id):
    for scsi_id in response_json['result']['volumes']:
        if scsi_id['scsiNAADeviceID'] == naa_id:
            print(json.dumps(scsi_id,sort_keys=True,indent=4))

def compare_vol_id(response_json, vol_id):
    for vol in response_json['result']['volumes']:
        if vol['volumeID'] == vol_id:
            print(json.dumps(vol,sort_keys=True,indent=4))

def main():
    mvip, user, user_pass, naa_id, vol_id = get_inputs()
    headers, url = build_auth(mvip, user, user_pass)
    payload = build_payload()
    response_json = connect_cluster(headers, url, payload)
    if naa_id !=None:
        print(naa_id)
        compare_scsi_id(response_json, naa_id)
    if vol_id !=None:
        print(vol_id)
        compare_vol_id(response_json, vol_id)
    
if __name__ == "__main__":
    main()
