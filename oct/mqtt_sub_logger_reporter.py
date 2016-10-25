import paho.mqtt.client as mqtt
import os

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("topic2",0)
cn=0
def on_message(client, userdata, msg):
    global cn


    cn+=1
    # print(msg.topic+" "+str(msg.payload))
    print(str(msg.payload))

    # repfile.write('dddd')
    # print "trying to write on file"
    file.write(str(msg.payload))
    file.write("\n")
    # if cn>1:
    file.flush()
    # client.publish("topic2", "sent via a subscriber909090")


client = mqtt.Client("subscriber111")
client.tls_set("/etc/mosquitto/certs/ca.crt")

client.on_connect = on_connect
if os.path.exists('/home/upendra/DataGlen/oct/report.txt'):
    print "report.txt exist opening in append mode"
    file = open("report.txt", "a")
else:
    print "Creating new file named report.txt"
    file=open("report.txt",'w')
    print file
    file.write('upload/download,qos,timestamp,upload_time/download_time,counter,slice,sender')
    file.write('\n')

client.on_message = on_message

client.connect("localhost", 8883, 60)

client.loop_forever()
