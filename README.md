# Documentation
This is a simple service that connects to the NAD serial port and sends received data to a MQTT broker.
It also subscribes to a command topic from the MQTT broker and sets the corresponding valur on the NAS through the serial port.

To start the service manually run the command:

    python3 NadMqttBridge.py <connfig file name>  <log file name>

The bridge publish the NAD settings to the MQTT broker on the format:

    NAD/\<deviceType\>/\<deviceName\>/\<nad setting same\>
    
The deviceType and deviceName is set in the configuration file and the nad setting name is the name that can be found in the documentation for the given setting. Any dots in the setting name will be replaced with a slash in the MQTT topic.
For example given the following config:
    
    deviceType=T757
    deviceName=Receiver

the setting Main.Volume will result in the topic "NAD/T757/Receiver/Master/Volume"

The bridge listens to the topic
    NAD/\<deviceType\>/\<deviceName\>/Commands
for updates to the receiver. So given the config above the following message sets the volume to -50dB:

    NAD/T757/Receiver/Commands/Master/Volume -50


The commands/settings names and legal values can be found in the NAD command documentation. The ones I have found can be found under "NAD Integration Protocol Documentation" on [NADs web site](https://nadelectronics.com/software/)

##Configuration

| name           | description                                                              |
|----------------|--------------------------------------------------------------------------|
| serialPort     | The serial port that the NAD receiver is connected to.                   |
| serialSpeed    | The baud rate to use when connecting to the NAD receiver. Usually 115200 |
| mqttBroker     | The hostname or ip of the MQTT broker to be used.                        |
| mqttPort       | The port used by the MQTT broker                                         |
| deviceType     | The model of the NAD receiver. Right now it only impacts the MQTT topic. |
| deviceName     | The name of the NAD receiver. Right now it only impacts the MQTT topic.  |
| logLevel       | The log level used when loggin to the log file.                          |

##Service
There is an example service definition to run this python service as a systemd service and it can be found in the service directory [here](service/nadMqttBridge.service).

## Known issues
The bridge doesn not support secure connections to the MQTT broker.