import requests
import sys
import getopt
from datetime import *
import os
import csv
from csv import Dialect
# import pytz
import time
import json
import paho.mqtt.client as mqtt

SUCCESSFUL_DATA_REQUEST = 200
SUCCESSFUL_REQUEST = 201
BAD_REQUEST = 400
UNAUTHENTICATED_REQUEST = 401
DUPLICATE_REQUEST = 409


ERROR_FILE_NAME = ""
ERROR_FILE_HANDLE = None
ERROR_FILE_WRITER = None

PERF_FILE_NAME = ""
PERF_FILE_HANDLE = None
PERF_FILE_WRITER = None

LOG_FILE_NAME = ""
LOG_FILE_HANDLE = None
LOG_FILE_WRITER = None

DATA_FORMAT = "CSV"  # One of XM/JS/CS
REGISTRATION_PARAMS = {"name": None,
                       "dataFormat": DATA_FORMAT,
                       "isActive": True,
                       "isMonitored": True,
                       "csvDataKeyName": "datapoint",
                       "dataTimezone": "Asia/Kolkata"
                       }

PERF_FILE_HEADERS = ["Uploading", "Registration", "Fields", "Activation"]
# Record counters
RECORD_COUNTER = 0
SKIP_COUNTER = 0
VALID_RECORD_COUNTER = 0
INVALID_RECORD_COUNTER = 0
POSTED_RECORD_COUNTER = 0

# Field positions
# sample packet - +49.77 +235.26 +5.92 +54.57 +0.87 +0.03 +5.5 +7.7 +0.7 +40.2
# Time: 00:05:29 06/10/14  00:1E:C0:0C:C4:94 iopex_AC1 54
FREQUENCY_POS = 0
VOLTAGE_POS = 1
ACTIVE_POS = 2
ENERGY_POS = 3
COST_POS = 4
CURRENT_POS = 5
REACTIVE_POS = 6
APPARENT_POS = 7
POWER_FACTOR_POS = 8
ANGLE_POS = 9
TIME_STRING_POS = 10
TIME_POS = 11
DATE_POS = 12
MAC_ADDRESS_POS = 13
PREMISE_LOAD_POS = 14
PACKET_COUNTER_POS = 15

# the character that separates premise and load names. for eg, rajesh_tv
NAME_FIELD_SEPARATOR = "_"
DATA_TIME_OFFSET = 330  # in minutes

jplug_dict = {}

# The field structure is as follows: name, type, position and format (only for date/time fields)
JPLUG_FIELDS = [
    ("Frequency", "FLOAT", 1, "H", ""),
    ("Voltage", "FLOAT", 2, "V", ""),
    ("ActivePower", "FLOAT", 3, "W", ""),
    ("Energy", "FLOAT", 4, "Wh", ""),
    ("Cost", "FLOAT", 5, "", ""),
    ("Current", "FLOAT", 6, "A", ""),
    ("ReactivePower", "FLOAT", 7, "W", ""),
    ("ApparentPower", "FLOAT", 8, "VA", ""),
    ("PowerFactor", "FLOAT", 9, "", ""),
    ("PhaseAngle", "FLOAT", 10, "", ""),
    ("Timestamp", "DATE", 11, "", "%H:%M:%S:%d/%m/%y"),
    ("MACAddress", "MAC", 12, "", ""),
    ("Appliance", "STRING", 13, "", ""),
    ("Counter", "INTEGER", 14, "", "")]


def initialize():
    global ERROR_FILE_NAME, ERROR_FILE_HANDLE, ERROR_FILE_WRITER
    global PERF_FILE_NAME, PERF_FILE_HANDLE, PERF_FILE_WRITER
    global LOG_FILE_NAME, LOG_FILE_HANDLE

    csv.register_dialect('jplug_data_file', delimiter=' ', skipinitialspace=True)
    csv.register_dialect('upload_metrics_file', delimiter='\t', skipinitialspace=True)

    try:
        LOG_FILE_HANDLE = open(LOG_FILE_NAME, 'wt')
    except IOError:
        print('Not able to open the ', LOG_FILE_NAME, ' for printing error records.')
        sys.exit()

    try:
        ERROR_FILE_HANDLE = open(ERROR_FILE_NAME, 'wt')
        ERROR_FILE_WRITER = csv.writer(ERROR_FILE_HANDLE, dialect='jplug_data_file')
    except IOError:
        LOG_FILE_HANDLE.write('Not able to open the ' + ERROR_FILE_NAME + ' for printing error records.')
        LOG_FILE_HANDLE.write("\n")
        sys.exit()

    try:
        PERF_FILE_HANDLE = open(PERF_FILE_NAME, 'wt')
        PERF_FILE_WRITER = csv.writer(PERF_FILE_HANDLE, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        PERF_FILE_WRITER.writerow(PERF_FILE_HEADERS)
    except IOError:
        LOG_FILE_HANDLE.write('Not able to open the ' + PERF_FILE_NAME + ' for printing performance records.')
        LOG_FILE_HANDLE.write("\n")
        sys.exit()


def finalize():
    global ERROR_FILE_HANDLE
    global LOG_FILE_HANDLE
    global PERF_FILE_HANDLE
    global RECORD_COUNTER, VALID_RECORD_COUNTER, INVALID_RECORD_COUNTER, SKIP_COUNTER

    ERROR_FILE_HANDLE.close()
    PERF_FILE_HANDLE.close()

    LOG_FILE_HANDLE.write('Read ' + str(RECORD_COUNTER) + ' records from the file.')
    LOG_FILE_HANDLE.write("\n")
    LOG_FILE_HANDLE.write('Skipped ' + str(SKIP_COUNTER) + ' records from the file.')
    LOG_FILE_HANDLE.write("\n")
    LOG_FILE_HANDLE.write(str(VALID_RECORD_COUNTER) + ' valid records.')
    LOG_FILE_HANDLE.write("\n")
    LOG_FILE_HANDLE.write(str(INVALID_RECORD_COUNTER) + ' invalid records.')
    LOG_FILE_HANDLE.write("\n")
    LOG_FILE_HANDLE.write('Posted ' + str(POSTED_RECORD_COUNTER) + ' records.')
    LOG_FILE_HANDLE.write("\n")

    LOG_FILE_HANDLE.flush()
    LOG_FILE_HANDLE.close()


# this function reads each line in the file specified in_file_name and uploads to cassandra.
# NOTE - it assumes that all lines are correct and does not do any error checking.
# for profiling uncomment following line
# @profile
def process_records(in_file_name, skip=0):
    global jplug_dict, ERROR_FILE_WRITER
    global RECORD_COUNTER, VALID_RECORD_COUNTER, INVALID_RECORD_COUNTER, SKIP_COUNTER, POSTED_RECORD_COUNTER
    global LOG_FILE_HANDLE

    with open(in_file_name, 'rU') as data_file:

        data_file_reader = csv.reader(data_file, dialect='jplug_data_file')

        print " about to start sending"

        t1 = time.time()

        mqttc = mqtt.Client()
        # mqttc.loop_start()
        mqttc.tls_set("/etc/mosquitto/certs/ca.crt")
        # mqttc.loop_start()
        mqttc.connect("localhost", 8883)


        for row in data_file_reader:

            RECORD_COUNTER += 1
            # print row
            print "record counter is %d"%RECORD_COUNTER

            x =' '.join(row)


            mqttc.publish("topic1", x, 1)
            # time.sleep(0.001)


        print "just came out of for loop"

        t2 = time.time()
        upload_time = "%0.2f" % ((t2 - t1) * 1000.0)

        mqttc.publish("topic1", "Uplaod time : " + upload_time + " and no of packets sent= %d" % RECORD_COUNTER,1)
        if RECORD_COUNTER==1000:
            # time.sleep(2)
            mqttc.disconnect()

        mqttc.loop_forever()
        # mqttc.loop_stop(force=False)







def usage():
    print('Usage: ' + sys.argv[0] + '-i <inputfile> ' + \
          ' [-s <number-of-records-to-skip>]' + ' [-o <output directory>]')


def main(argv):
    global ERROR_FILE_NAME, PERF_FILE_NAME, LOG_FILE_NAME
    in_file = ''
    skip = 0
    outdir = "."

    try:
        # print(argv)
        opts, args = getopt.getopt(argv, "hi:s:o:", ["ifile=", "skip=", "outdir="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()

        elif opt in ("-i", "--ifile"):
            in_file = arg

        elif opt in ("-o", "--outdir"):
            outdir = arg

        elif opt in ("-s", "--skip"):
            skip = int(arg.strip())

        else:
            assert False, "unhandled option"

    if in_file == '':
        usage()
        sys.exit(2)

    file_name = os.path.basename(in_file)

    file_prefix = file_name.split('.')[0]

    ERROR_FILE_NAME = outdir + "/" + file_prefix + '-errors' + '.txt'
    PERF_FILE_NAME = outdir + "/" + file_prefix + '-timing' + '.csv'
    LOG_FILE_NAME = outdir + "/" + file_prefix + '-debug' + '.log'

    sys.setcheckinterval(1000)
    print "initializing"
    initialize()

    process_records(in_file, skip)
    finalize()


if __name__ == "__main__":
    main(sys.argv[1:])
