#!/usr/bin/python3
from requests import post
headers = {'x-ha-access': 'http_password', 'content-type': 'application/json'}
while True:
    try:
        str = input()
    except EOFError:
        break
    if 'pppoe: Disconnected.' in str or 'ether: (WAN) link state is Down' in str:
        postData = '{"state":"off","attributes": {"wan_ip":""}}'
        post('http://127.0.0.1:8123/api/states/binary_sensor.Internet',data=postData,headers=headers)
    elif 'pppoe: Connection established' in str:
        wan_ip = str[str.find('established')+12:str.find('->')-1]
        postData = '{"state":"on","attributes": {"wan_ip":"'+wan_ip+'"}}'
        post('http://127.0.0.1:8123/api/states/binary_sensor.Internet',data=postData,headers=headers)
    elif 'Disassociated with station' in str:
        mac = str[-17:len(str)]
        postData = '{"mac":"'+mac+'","source_type":"router","consider_home":"3"}'
        post('http://127.0.0.1:8123/api/services/device_tracker/see',data=postData,headers=headers)
    elif 'Installed unicast CCMP key for supplicant' in str:
        mac = str[-17:len(str)]
        postData = '{"mac":"'+mac+'","source_type":"router","consider_home":"99:00:00"}'
        post('http://127.0.0.1:8123/api/services/device_tracker/see',data=postData,headers=headers)
