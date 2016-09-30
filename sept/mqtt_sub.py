
import paho.mqtt.client as mqtt
import io

def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))

    client.subscribe("topic1",2)

cnt=0
def on_message(client, userdata, msg):
    global cnt

    print(cnt),
    print(msg.topic + " -> " + str(msg.payload))
    cnt+=1
    data=str(msg.payload)
    file.write(unicode(data))
    # file.write(unicode(str(msg.payload)))
    file.write(u"\n")



client = mqtt.Client()
client.tls_set("/etc/mosquitto/certs/ca.crt")
client.on_connect = on_connect

file = io.open("outputfile.txt", "a")
print(" Output file is created as outputfile.txt")
client.on_message = on_message
client.connect("localhost", 8883, 60)

client.loop_forever()