#!/usr/bin/python3
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been
#   tested in lab situations, all use cases cannot be accounted for.
# This script gets the replication partner for a given cluster or all volumes
# Example successful outputs:
#   Volume - 
#           Passed:
#           Total number of replication destinations is: {1}
#   Cluster -
#           +-----------------+--------------------+
#           | Cluster Pair ID |    Cluster Name    |
#           +-----------------+--------------------+
#           |        1        | SFDEMO1            |
#           +-----------------+--------------------+
#           Passed: only one replication target

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
                        metavar='user',
                        help='username to connect with')
    parser.add_argument('-p', type=str,
                        required=False,
                        metavar='user_pass',
                        help='password for user')
    parser.add_argument('-o', type=str,
                        required=False,
                        metavar='check_opt',
                        choices=['cluster', 'volume'],
                        help='option for cluster or volume')
    args = parser.parse_args()

    mvip = args.m
    user = args.u
    check_opt = args.o
    if not args.p:
        user_pass = getpass("Enter password for user {} "
                            "on cluster {}: ".format(user,
                                                     mvip))
    else:
        user_pass = args.p
    
    return mvip, user, user_pass, check_opt

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

def build_payload(check_opt):
    if check_opt == "cluster":
        payload = json.dumps({"method": "ListClusterPairs","params":{},"id": 1})
    else:
        payload = json.dumps({"method": "ListActivePairedVolumes","params":{},"id": 1})
    return payload
    
def connect_cluster(headers, url, payload):
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    try:
        if response.status_code == 200:
            response_json = json.loads(response.text)
            return response_json
        elif response.status_code == 401:
            print("Please check username and password and try again")
        else:
            print("Unexpected HTTP response detected: {}".format(response.status_code))
    except Exception as e:
        print("Exception returned: \n\t{}".format(e))

def build_table(cls_column1, cls_column2, cls_id, cls_name):
    out_tbl = PrettyTable()
    out_tbl.field_names = [cls_column1, cls_column2]
    out_tbl.add_row([cls_id, cls_name])
    print(out_tbl)

def compare_pair_ids(response_json, check_opt):
    cluster_pair_count = []
    vol_pair_count = []
    if check_opt == "cluster":
        for id in response_json['result']['clusterPairs']:
            cluster_pair_count.append(id)
            cls_column1 = "Cluster Pair ID"
            cls_column2 = "Cluster Name"
            cls_id = id['clusterPairID']
            cls_name = id['clusterName']
            build_table(cls_column1, cls_column2, cls_id, cls_name)
        if (len(cluster_pair_count)) == 1:
            print("Passed: only one replication target")
        elif (len(cluster_pair_count)) > 1:
            print("Failed: more than one replication target")
        else:
            print("No replication found")
    else:
        for pair in response_json['result']['volumes']:
            for id in pair['volumePairs']:
                vol_pair_count.append(id['clusterPairID'])
        distinct_pair = set(vol_pair_count)
        if len(distinct_pair) == 1:
            print("Passed:\nTotal number of replication destinations is: {}".format(distinct_pair))
        elif len(distinct_pair) >  1:
            print("Failed:\nTotal number of replicaiton destinations is {}".format(distinct_pair))
        else:
            print("No replication found")

def main():
    mvip, user, user_pass, check_opt = get_inputs()
    headers, url = build_auth(mvip, user, user_pass)
    payload = build_payload(check_opt)
    response_json = connect_cluster(headers, url, payload)
    compare_pair_ids(response_json, check_opt)
    
if __name__ == "__main__":
    main()
