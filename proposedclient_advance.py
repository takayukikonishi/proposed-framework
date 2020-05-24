import struct
import json_lines
import json
import sys
import subprocess
import requests

#with open('filebeat.1')as f:
#    for item in json_lines.reader(f):
#        print(item)
cmd = ["sudo", "/usr/bin/filebeat", "-e"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for line in iter(proc.stdout.readline, b''):
    flowdata = json.loads(line.rstrip().decode("utf8"))
    print(flowdata)
    if (flowdata["netflow"]["source_ipv4_address"] == "133.19.57.103") and (flowdata["netflow"]["destination_ipv4_address"] == "133.19.170.14"): 
        print("anomaly detection")
        anomaly_traffic = {
            "ietf-dots-data-channel:anomaly-traffic": {
                "srcip": flowdata["netflow"]["source_ipv4_address"],
                "dstip": flowdata["netflow"]["destination_ipv4_address"],
                "srcport": flowdata["netflow"]["source_transport_port"],
                "dstport": flowdata["netflow"]["destination_transport_port"],
                "protcolnumber": flowdata["netflow"]["protocol_identifier"]
            }
        }
        data = json.dumps(anomaly_traffic)
        response = requests.put("http://133.19.57.102:8080", data=data)
        print(response)

