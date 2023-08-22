import json
import os
import time
from prometheus_client.core import REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
from urllib.request import Request, urlopen

JUDGE0_API_URL = os.getenv("JUDGE0_API_URL", "https://ce.judge0.com")
AUTH_TOKEN_HEADER = os.getenv("AUTH_TOKEN_HEADER", "X-Auth-Token")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
PORT = int(os.getenv("PORT", "8000"))

HEADERS = {
  AUTH_TOKEN_HEADER: AUTH_TOKEN
}

if AUTH_TOKEN == None:
    print('AUTH_TOKEN not provided')
    exit(1)

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        request = Request(JUDGE0_API_URL+'/workers', headers=HEADERS)
        response = urlopen(request)
        judge0_workers = json.loads(response.read())

        for queue in judge0_workers:
            queue_name = queue['queue']
            for metric in queue:
                # Queue name is not metric and we read it already above
                if metric == 'queue':
                    continue

                if metric == 'size':
                    description = 'Total number of submissions if queue'
                else:
                    description = 'Number of ' + metric + ' workers'

                print(queue_name, '_', metric, ":", queue[metric])
                c = CounterMetricFamily("judge0_queue_"+metric, description, labels=['queue'])
                c.add_metric([queue_name], queue[metric])
                yield c

if __name__ == '__main__':
    print('Start serving metrics from', JUDGE0_API_URL, 'on port', PORT)
    start_http_server(PORT)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
