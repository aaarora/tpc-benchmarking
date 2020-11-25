#!/usr/bin/python3

import requests
import json
import time

with open('/home/maddash_conf.json') as maddash_conf:
    conf = json.load(maddash_conf)
maddash_conf.close()

url = conf['url']
key = conf['key']
headers = conf['headers']

with open('/home/rates.json') as f:
    data = json.load(f)
f.close()

for hosts, rate in data.items():
    host_str = hosts.split('~')
    payload = {
        "subject-type": "point-to-point",
        "source": host_str[1].split(':')[0],
        "destination": host_str[3].split(':')[0],
        "tool-name": "gridftp-tpc-single-stream",
        "measurement-agent": host_str[1].split(':')[0],
        "input-source": host_str[0],
        "input-destination": host_str[2],
        "event-types": [{"event-type": "throughput","summaries":[{"summary-type": "aggregation","summary-window": 3600},{"summary-type": "aggregation","summary-window": 86400}]}]
    }

    m = requests.post(url, data=json.dumps(payload), headers=headers)

    returnJSON = m.json()
    metadataKey = returnJSON['metadata-key']

    dat = {
        "ts": int(time.time()),
        "val": rate
    }
    d = requests.post("{0}{1}/throughput/base".format(url,metadataKey), data=json.dumps(dat), headers=headers)
