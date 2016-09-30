# ("Frequency", "FLOAT", 1, "H", ""),
#     ("Voltage", "FLOAT", 2, "V", ""),
#     ("ActivePower", "FLOAT", 3, "W", ""),
#     ("Energy", "FLOAT", 4, "Wh", ""),
#     ("Cost", "FLOAT", 5, "", ""),
#     ("Current", "FLOAT", 6, "A", ""),
#     ("ReactivePower", "FLOAT", 7, "W", ""),
#     ("ApparentPower", "FLOAT", 8, "VA", ""),
#     ("PowerFactor", "FLOAT", 9, "", ""),
#     ("PhaseAngle", "FLOAT", 10, "", ""),
#     ("Timestamp", "DATE", 11, "", "%H:%M:%S:%d/%m/%y"),
#     ("MACAddress", "MAC", 12, "", ""),
#     ("Appliance", "STRING", 13, "", ""),
# #     ("Counter", "INTEGER", 14, "", "")]
#
#
# data_file_reader = open("dataset.txt","r")
# for row in data_file_reader:
#     x=float(row[2])
#     print x
# import csv
# with open('dataset.txt', 'rU') as csvfile:
#     reader=csv.reader(csvfile)
#
#     for row in reader:
#
#         x=row.split(" ")
#
#         print x



# x=io.open('datafile.txt',mode='r')
import time
import io

x=io.open('spam.txt','a',1000)
d="ddd111"
# x.write(d)
x.write(unicode(d))
x.write(u"\n")
# print x.next()
# d="dddd"
# x.write(d)
#
# with io.open('spam.txt', 'w') as file:
#     file.write(u'Spam and eggs!')
#     time.sleep(1)

with io.open('spam.txt', 'r') as file:
    print file.next()