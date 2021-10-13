# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import threading

#TODO Serial bluetooth connection
#
#Serial bluetooth connection 


# Define ENDPOINT, CLIENT_ID, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a1jepn4zys8yy5-ats.iot.us-east-1.amazonaws.com"
CLIENT_ID = "RaspberyPi_One"
PATH_TO_CERT = "certificates/Advanced.cert.pem"
PATH_TO_KEY = "certificates/Advanced.private.key"
PATH_TO_ROOT = "certificates/root.pem"

##############################################
#TODO READ VALUES FROM BLUETOOTH AND ASSIGN THEM TO "MESSAGE" VARIABLE
# EXAMPLE using regular expressions. But can be done another way:
# rawserial = ser.readline()
#         cookedserial = rawserial.decode('utf-8').strip('\r\n')
#         print('The raw data is:')
#         print(cookedserial)
#         num = re.findall("\d+\.\d+",str(cookedserial))
#         print('Only numbers are:')
#         print(num)
#         b_wind = num[0]  
#         b_hum = num[1] 
#         b_temp = num[2]  
#         b_photo = num[3]           
##############################################


#TOPICS:
TOPIC_WIND = "laundry/wind"
b_wind = 301
MESSAGE_WIND = b_wind ##TODO change with value from bluetooth "MESSAGE_WIND = b_wind"##

TOPIC_HUMIDITY = "laundry/humidity"
b_hum = 97
MESSAGE_HUMIDITY = b_hum ##TODO change with value from bluetooth "MESSAGE_HUMIDITY = b_hum"##

TOPIC_TEMP = "laundry/temperature"
b_temp = 27
MESSAGE_TEMP = b_temp ##TODO change with value from bluetooth "MESSAGE_TEMP = b_temp"##

TOPIC_PHOTO = "laundry/photoresistor"
b_photo = 30
MESSAGE_PHOTO = b_photo ##TODO change with value from bluetooth "MESSAGE_PHOTO = b_photo"




# Spin up resources
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERT,
            pri_key_filepath=PATH_TO_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_ROOT,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
            )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
# Publish message to server desired number of times.
print('Begin Publish')

bluetooth = 1 #Testing variable while bluetooth is not connected
i = 0
while True:
    t.sleep(1.5)
    if bluetooth > 0:  #TODO Change "bluetooth" to "ser.in_waiting > 0" to check connection from bluetooth
        def wind_sensor(TOPIC_WIND, MESSAGE_WIND):
            data_wind = "{}".format(MESSAGE_WIND)
            message_wind = {"Wind" : int(data_wind)}
            mqtt_connection.publish(topic=TOPIC_WIND, payload=json.dumps(message_wind), qos=mqtt.QoS.AT_LEAST_ONCE)
            print('Publish wind sensor data')
            t.sleep(1)
        def hum_sensor(TOPIC_HUMIDITY, MESSAGE_HUMIDITY):
            data_hum = "{}".format(MESSAGE_HUMIDITY)
            message_hum = {"Humidity" : int(data_hum)}
            mqtt_connection.publish(topic=TOPIC_HUMIDITY, payload=json.dumps(message_hum), qos=mqtt.QoS.AT_LEAST_ONCE)
            print('Publish humidity sensor data')
            t.sleep(1)
        def temp_sensor(TOPIC_TEMP, MESSAGE_TEMP):
            data_temp = "{}".format(MESSAGE_TEMP)
            message_temp = {"Temperature" : int(data_temp)}
            mqtt_connection.publish(topic=TOPIC_TEMP, payload=json.dumps(message_temp), qos=mqtt.QoS.AT_LEAST_ONCE)
            print('Publish temperature sensor data')
            t.sleep(1)
        def photo_sensor(TOPIC_PHOTO, MESSAGE_PHOTO):
            data_photo = "{}".format(MESSAGE_PHOTO)
            message_photo = {"Photoresistor" : int(data_photo)}
            mqtt_connection.publish(topic=TOPIC_PHOTO, payload=json.dumps(message_photo), qos=mqtt.QoS.AT_LEAST_ONCE)
            print('Publish photoresistor sensor data')
            t.sleep(1)

            #Threading
        t_wind = threading.Thread(target=wind_sensor, args=(TOPIC_WIND, MESSAGE_WIND))
        t_hum = threading.Thread(target=hum_sensor, args=(TOPIC_TEMP, MESSAGE_TEMP)) 
        t_temp = threading.Thread(target=temp_sensor, args=(TOPIC_TEMP, MESSAGE_TEMP)) 
        t_photo = threading.Thread(target=photo_sensor, args=(TOPIC_PHOTO, MESSAGE_PHOTO))


        t_wind.start()
        t_temp.start()
        t_hum.start()
        t_photo.start()

        t_wind.join()
        t_temp.join()
        t_hum.join()
        t_photo.join()

        t.sleep(5)
    else:
        print("No connection")
        t.sleep(1)

    
    i += 1
    print('Total number of publishings is {}'.format(i))
    t.sleep(2)


    

###### WE CAN USE THE FOLLOWING FUCNTION TO STOP PYTHON WITH A COMMAND WITHOUT CMD+C  begin
# print('Publish End')
# disconnect_future = mqtt_connection.disconnect()
# disconnect_future.result()
###### WE CAN USE THE FOLLOWING FUCNTION TO STOP PYTHON WITH A COMMAND WITHOUT CMD+C  end