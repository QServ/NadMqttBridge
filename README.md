# Documentation
This is a simple service that connects to the NAD serial port and sends received data to a MQTT broker.
It also subscribes to a command topic from the MQTT broker and sets the corresponding valur on the NAS through the serial port.


##Configuration



##Service
There is an example service definition to sun this python service as a systemd service and it can be found in the service directory [here](service/nadMqttBridge.service).

