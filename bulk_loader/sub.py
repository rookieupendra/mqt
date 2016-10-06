
import sys
import paho.mqtt.client as mqtt
import time
def on_connect(mqttc, obj, flags, rc):
    print("rc: "+str(rc))
cnt=0
t1=0.0
def on_message(mqttc, obj, msg):
    global cnt
    global t1
    # t1=0.0
    if cnt==0:
        t1 = time.time()


    # print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    # print cnt
    print (msg.payload)

    cnt+=1

    if cnt==1002:
        t2 = time.time()
        download_time = "%0.2f" % ((t2 - t1) * 1000.0)
        print "Time taken to download  " +download_time

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)


mqttc = mqtt.Client()
mqttc.tls_set("/etc/mosquitto/certs/ca.crt")
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
mqttc.connect("localhost", 8883, 60)
mqttc.subscribe("topic1", 1)


mqttc.loop_forever()

