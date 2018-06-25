# Apple Airport hass devicetracker and Internet Connection Sensor (binary)
Turn the Apple Airport Wireless Router to a homeassistant devicetracker.
Tested on Apple Airport Timecapsule AC with the newest firmware.

Apple's wireless router can send out syslogs containing important and useful information for HA.
These syslog messages can be used to track wireless devices and monitoring the connection of Internet (a binary_sensor)
It's should also work with other routers that throw syslogs (maybe little modification is required)

# Steps:

0. Save the python script on homeassistant host, for example, in the home path of homeassistant:
   /home/homeassistant
   If device_tracker is not enabled on HA, enable it.
   If either frontend or api is not enabled on HA, enable one of them.

1. Enable syslog and set target address on airport router.
  This could be done via Windows version of Airport Utility.
  target address should be, of course, the homeassistant host.
  
2. Enable rsyslog server and it's configuration in /etc/rsyslog.conf:

` 
     module(load="imudp")

     input(type="imudp" port="514" ruleset="apple_airport")
     
     module(load="omprog")
     
     ruleset(name="apple_airport"){
     
       action( type="omprog"
       
       binary="/home/homeassistant/apple_airport.py")
       
       }`

3. Restart the rsyslog service:

    `$ sudo service rsyslog restart`

or

    `$ sudo systemctl restart rsyslog`

depending on the system.

That's all.

Below is just for confirming and testing.

4. Confirm

    run:

`$ sudo netstat -tulpn | grep rsyslog`

the output should looks like this:

`udp    0 0    0.0.0.0:514    0.0.0.0:*      551/rsyslogd 

udp6    0 0    :::514        :::*          551/rsyslogd`

then run:

`$ ps ax |grep apple`

there should be the process of apple_airport.py 

`15321 ?        S      0:00 /usr/bin/python3 /home/homeassistant/apple_airport.py`

5. Make a simple test:

On another computer (unix like), send a message to the rsyslog service:

`$ echo '<54> <133>Feb 11 22:32:00 timecapsuleu pppoe: Disconnected.' >/dev/udp/ha-host/514`

Then check on the frontend of ha, the new binary_sensor named "Internet" will appear.
