# Documentation
This is a simple service that connects to the NAD serial port and sends received data to a MQTT broker.
It also subscribes to a command topic from the MQTT broker and sets the corresponding valur on the NAS through the serial port.

To start the service manually run the command:

    python3 NadMqttBridge.py <connfig file name>  <log file name>

The bridge publis the NAD settings to the MQTT broker on the format:  "NAD/<deviceType>/<deviceName>/<nad setting same>"
The deviceType and deviceName is set in the configuration file and the nad setting name is the name that can be found in the documentation for the given setting. Any dots in the settiong name will be replaced with a slash in the MQTT topic.
For example given the following config:
    
    deviceType=T757
    deviceName=Receiver

the setting Main.Volume will result in the topic "NAD/T757/Receiver/Master/Volume" 



The commands/settings names and legal values can be found in the NAD command documentation. The ones I have found can be found under "NAD Integration Protocol Documentation" on [NADs web site](https://nadelectronics.com/software/)

##Configuration



##Service
There is an example service definition to sun this python service as a systemd service and it can be found in the service directory [here](service/nadMqttBridge.service).

