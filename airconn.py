#!/usr/bin/python2

import sys
from socket import *
from requests import post
headers = {'Authorization': "Bearer xxxxxxxxxx", 'content-type': 'application/json'}
host = '0.0.0.0'
port = 514
addr = (host,port)

try:
  s = socket(AF_INET,SOCK_DGRAM)
  s.bind(addr)
except:
  print "error binding"
  sys.exit(1)

try:
  while 1:
    try:
      rdata,raddr = s.recvfrom(8092)
      rmes = str(rdata)
      #print 'got message from ',raddr,': ',rmes

      if 'pppoe: Disconnected.' in rmes or 'ether: (WAN) link state is Down' in rmes:
        postData = '{"state":"off","attributes": {"wan_ip":""}}'
        #print postData
        post('http://127.0.0.1:8123/api/states/binary_sensor.Internet',data=postData,headers=headers)
      elif 'pppoe: Connection established' in rmes:
        wan_ip = rmes[rmes.find('established')+12:rmes.find('->')-1]
        postData = '{"state":"on","attributes": {"wan_ip":"'+wan_ip+'"}}'
        #print postData
        post('http://127.0.0.1:8123/api/states/binary_sensor.Internet',data=postData,headers=headers)
      elif 'Disassociated with station' in rmes:
        mac = rmes[-18:-1]
        postData = '{"mac":"'+mac+'","source_type":"router","consider_home":"3"}'
        #print postData
        post('http://127.0.0.1:8123/api/services/device_tracker/see',data=postData,headers=headers)
      elif 'Installed unicast CCMP key for supplicant' in rmes:
        mac = rmes[-18:-1]
        postData = '{"mac":"'+mac+'","source_type":"router","consider_home":"99:00:00"}'
        #print postData
        post('http://127.0.0.1:8123/api/services/device_tracker/see',data=postData,headers=headers)
    except socket.error:
      pass
except KeyboardInterrupt:
    print('good bye')
    sys.exit()
