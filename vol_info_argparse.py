#!/usr/local/bin/python
# Author: Scott Chubb scott.chubb@netapp.com
# Written for Python 3.4 and above
# No warranty is offered, use at your own risk.  While these scripts have been tested in lab situations, all use cases cannot be accounted for.
# Windows install: python -m pip install -U pip setuptools
# pip install solidfire-sdk-python

import argparse
from solidfire.factory import ElementFactory
# QoS is a dataobject model and must be imported to set QoS
# it is not required to get/print QoS information
from solidfire.models import QoS

def get_inputs():
    # Set vars for connectivity using argparse
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
    parser.add_argument('-v', type=int,
                        required=False,
                        metavar='vol_id',
                        help='volume ID')                        
    args = parser.parse_args()

    mvip_ip = args.m
    user_name = args.u
    user_pass = args.p
    vol_id = args.v
    
    return mvip_ip, user_name, user_pass, vol_id

def connect_cluster(mvip_ip, user_name, user_pass):
   # Use ElementFactory to get a SolidFireElement object.
    sfe = ElementFactory.create(mvip_ip, user_name, user_pass)
    return sfe
    
def get_vol_info(sfe, vol_id):
    print(vol_id)
    # This script returns information on volume ID 1, remove 
    # the volume ID to return all volumes
    list_volumes_result = sfe.list_volumes()
    for volume in list_volumes_result.volumes:
        if vol_id == None:
            print(volume.name, volume.qos.max_iops)
        else:
            if volume.volume_id == vol_id:
                print(volume.name, volume.qos.max_iops)
            

    # Printable outputs
        # print(volume.access) will print the access type of the volume
        # print(volume.account_id) will print the account ID that has access
        # if the output is in parens (), then you can "sub" print using the attribute, and sub-property
        # example - print(volume.qos.max_iops)
        
    # Volume(
        # access='readWrite', 
        # account_id=1, 
        # attributes={}, 
        # block_size=4096, 
        # create_time='2016-08-19T22:31:16Z', 
        # delete_time='', 
        # enable512e=True, 
        # enable_snap_mirror_replication=None, 
        # iqn='iqn.2010-01.com.solidfire:n6o7.linuxvol1.11', 
        # last_access_time=None, 
        # last_access_time_io=None, 
        # name='LinuxVol1', 
        # purge_time='', 
        # qos=VolumeQOS(burst_iops=6500, burst_time=60, 
            # curve={'1048576': 15000, '131072': 1950, '16384': 270, '262144': 3900, '32768': 500, '4096': 100, '524288': 7600, '65536': 1000, '8192': 160}, 
            # max_iops=6000, 
            # min_iops=5000), 
        # qos_policy_id=None, 
        # scsi_euidevice_id='6e366f370000000bf47acc0100000000', 
        # scsi_naadevice_id='6f47acc1000000006e366f370000000b', 
        # slice_count=1, 
        # status='active', 
        # total_size=20000538624, 
        # virtual_volume_id=None, 
        # volume_access_groups='[1]', 
        # volume_consistency_group_uuid=None, 
        # volume_id=11, 
        # volume_pairs='[]', 
        # volume_uuid=None)	

def main():
    mvip_ip, user_name, user_pass, vol_id = get_inputs()
    sfe = connect_cluster(mvip_ip, user_name, user_pass)
    get_vol_info(sfe, vol_id)

if __name__ == "__main__":
    main()
    
