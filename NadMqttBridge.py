import configparser
import io
import logging
import paho.mqtt.client as mqtt
import serial
import signal
import sys
import threading

configParser = configparser.ConfigParser()
#logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')


######
# MQTT
######
def mqtt_on_connect(client, userdata, flags, rc):
    topic = "NAD/" + client.config["deviceType"] + "/" + client.config["deviceName"] + "/Commands/#"
    client.subscribe(topic)
    logging.info("subscribing to topic: " + topic)

def mqtt_on_message(client, userdata, msg):
    logging.debug("[MQTT] Message on '" + str(msg.topic) + "': " + str(msg.payload))
    topic = msg.topic.split("/")
    setting = ".".join(topic[4:])
    value = msg.payload.decode("utf-8")
    client.serialPort.flushOutput()

    if value == '?':
        logging.debug("Writing to NAD: " + setting + "?")
        client.serialPort.write(bytes("\r" + setting + "?\r", 'utf-8'))
    else:
        logging.debug("Writing to NAD: " + setting + "=" + value)
        client.serialPort.write(bytes("\r" + setting + "=" + value + "\r", 'utf-8'))

########
# serial
########
def listenSerial(config, client, serialReader):
    while True:
        incomming = serialReader.readline()
        incomming = incomming[:-1] #Strip the trailing '\r' character.
        logging.debug("Incomming from NAD: "  + incomming)
        data = incomming.split("=")
        if (len(data) == 2):
            logging.debug("publishing " + "NAD/" + config["deviceType"] + "/" + config["deviceName"] + "/" + data[0].replace(".","/") + " " + data[1])
            client.publish("NAD/" + config["deviceType"] + "/" + config["deviceName"] +"/" + data[0].replace(".","/"), data[1], retain=True)
        elif (data[0] == ""):
            None
        else:
            logging.debug("publishing " + "NAD/" + config["deviceType"] + "/" + config["deviceName"] + "/" + data[0].replace(".","/"))
            client.publish("NAD/" + config["deviceType"] + "/" + config["deviceName"] +"/" + data[0].replace(".","/"), "", retain=True)
        
def main(args):
    configParser.read(args[0])
    config = configParser['settings']
    logging.basicConfig(level=logging.getLevelName(config["logLevel"]),
                       format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                       datefmt='%m-%d %H:%M',
                       filename=args[1],
                       filemode='w')

    try:
        serialPort = serial.Serial(port=config["serialPort"], baudrate=int(config["serialSpeed"]), xonxoff=False, rtscts=False, dsrdtr=False, timeout=5)
        serialReader = io.TextIOWrapper(io.BufferedRWPair(serialPort, serialPort, 1000),
                                       newline = '\r',
                                       line_buffering = True)

        logging.debug("[SERIAL] Connected to " + config["serialPort"] + " with " + str(config["serialSpeed"]) + " Baud")
    except Exception as e:
        logging.critical("Error creating serial port thread: " + str(e))
        sys.exit(1)

    try:
        client = mqtt.Client(config['deviceName'], protocol=mqtt.MQTTv311)
        client.on_connect = mqtt_on_connect
        client.on_message = mqtt_on_message
        client.connect(config["mqttBroker"], int(config["mqttPort"]))
        client.config = config
        client.loop_start()
    except Exception as e:
        logging.critical("Could not setup mqtt session. " + str(e))
        sys.exit(1)

    client.serialPort = serialPort
    readerThread = threading.Thread(target=listenSerial, args=(config, client, serialReader))
    readerThread.deamon = True
    logging.info("Starting serial port thread")
    readerThread.start();
        
if __name__ == '__main__':
    main(sys.argv[1:])    
