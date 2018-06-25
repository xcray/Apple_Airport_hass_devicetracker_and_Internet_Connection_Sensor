# Apple Airport hass devicetracker and Internet Connection Sensor (binary)
Turn the Apple Airport Wireless Router to a homeassistant device tracker, and an Internet Connection binary sensor.

Tested on Apple Airport Timecapsule AC with the newest firmware (7.7.9).

Working process:

- Apple's wireless router send out syslogs containing important and useful information for HA (WAN connection events and wireless devices connection events).

- The rsyslog service collecting the syslog messages come from Apple Airport router.

- The messages are transfered to the python script (via omprog interface of rsyslog).

- The python script parse the messages and triggers the states of the wireless devices (by mac) and the binary_sensor representting the Internet connection, via the API of homeassistant.

rsyslog service could runs on any host inside the same network, the HA host is a good choice for most people.

It's should also work with other routers that throw syslogs (maybe little modification is required).

It's totally event-driven, sensitive, and no active scan required. 

# Steps:

0. Save the python script on homeassistant host, for example, in the home path of homeassistant:
   /home/homeassistant

If device_tracker is not enabled on HA, enable it.

If either frontend or api is not enabled on HA, enable one of them.

1. Enable syslog and set target address on airport router.

  This could be done via Windows version of Airport Utility.

  The default level 5 is fine for this purpose.

  Target address should be, of course, the homeassistant host.


2. Enable rsyslog server and it's configuration in /etc/rsyslog.conf:

``` 
module(load="imudp")

input(type="imudp" port="514" ruleset="apple_airport")

module(load="omprog")

ruleset(name="apple_airport"){

       action( type="omprog"

       binary="/home/homeassistant/apple_airport.py")

       } 
```

3. Restart the rsyslog service:

`
$ sudo service rsyslog restart
`

or

`
$ sudo systemctl restart rsyslog
`

depending on the system.

That's all.

Below is just for confirming and testing.

4. Confirm

    run:

`
$ sudo netstat -tulpn | grep rsyslog
`

the output should looks like this:

```
udp    0 0    0.0.0.0:514    0.0.0.0:*      551/rsyslogd 

udp6    0 0    :::514        :::*          551/rsyslogd
```

then run:

`
$ ps ax |grep apple
`

there should be the process of apple_airport.py 

`
15321 ?        S      0:00 /usr/bin/python3 /home/homeassistant/apple_airport.py
`

5. Make a simple test:

On another computer (unix like), send a message to the rsyslog service:

`
$ echo '<54> <133>Feb 11 22:32:00 timecapsuleu pppoe: Disconnected.' >/dev/udp/ha-host/514
`

Then check on the frontend of ha, the new binary_sensor named "Internet" will appear.

# Notes:
Because the wireless devices will disconnect from the AP and reconnect in very short time (less than 1 second) frequently, and some times the router itself will disconnect and reconnect the pppoe connection rapidly, if the states of the sensor been used in automations, a suitable timer should be involved to avoid un-necessary actions.

For the device_tracker，there already is a timer (consider_home) can leverage this problem. 
