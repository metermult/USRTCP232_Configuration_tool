# USR-TCP232-302 Controller

Hello! This is a tool I made that can be integrated into a larger script base for configuring RS232 converters that are networked. Specifically the USR-TCP232-302. I would imagine this would also work across other PUSR devices but it has yet to be attempted. This allows an admin/user to make a few requests to one of these devices and configure them without having to access the web UI. 

## Concepts

Using get requests, one can use a script to control a network of tcp to rs232 traffic converters and communicate out to hosts. This allows for a non web interface way to communicate with the device and can be nested in a larger script for configuration. This method works by taking RS232 traffic and sending it to a predefined host:port configured in the webserver. The webserver is very minimal, making it easy to configure and setup for testing purposes. The creds across devices will be `admin:admin` as they are default. The device can also maintain a static IP after a reboot but will come up on `192.168.0.7` if the reset button is pressed. Which makes adding to a specific VLAN very easy and doable. 

## Webs

In firefox you can simply plugin the IP of the device to access. Again, pressing the reset will bring it up at 192.168.0.7. Here is a screenshot of the web interface. 

![web](/images/WebInterface.png)

The only thing we care about is the actual requests being sent though. End goal is to automate all of this so it is best to start using `curl` or some other web interactive program or library to start navigating this device and configuring it how we need it. 

## Interaction

To login to the device with a curl request `curl -u admin:admin http://[ip addr]`. In this case I will be accessing the default with `curl -u admin:admin http://192.168.0.7`. There will be a webpage that spits out. This is the logged in page and now will allow us to access some of the configuration fucntions for the device. Simple enough, you can just hover over the configuration tabs or monitor the requests made in your web browser/wireshark for the webpage it is sending a get request for. Here is a tcpstream for a get request for the serial configuration page located at `/sernet1.shtml`. With the ability to navigate webpages now, it is trivial to plug in a few keys and actually adjust what we want to change on. 

![serial](/images/Wireshark.png)

## Configuration script

``` 
usage: config_rs232.py [-h] [-d DEST] [-s SOURCE] [-dpt DPORT] [-spt SPORT]
 
 Configure RS232 to ETH adapters.
 
 optional arguments:
   -h, --help            show this help message and exit
   -d DEST, --dest DEST  Destination listener IP address to communicate to
   -s SOURCE, --source SOURCE
                         Source IP address
   -dpt DPORT, --dport DPORT
                         Destination listener port to communicate to
   -spt SPORT, --sport SPORT
                         Source port
```
                         
The configuration script will make 2 GET requests and can be changed statically for values that are not passed as args (this is because these values can be messed with but may be needed for a larger script). Yes, in order to make a valid request I have found that sending less than all 20+ of these parameters will cause the device to drop the request and configurations will not be set. Then after the 20+ requests are sent, a reset is sent and the device will come up with its new configurations. 

## RS232/TTL

After configuring the device, start a netcat listener on your host with `nc -l [port]` and you should have an interactive shell with the endpoint. 


