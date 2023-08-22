import time
import json
from prometheus_client.core import REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server


class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        input_json_string = '[{"queue":"default","size":0,"available":0,"idle":0,"working":0,"paused":0,"failed":0},{"queue":"1.13.0","size":0,"available":0,"idle":0,"working":0,"paused":0,"failed":0}]'

        judge0_workers = json.loads(input_json_string)
        for queue in judge0_workers:
            queue_name = queue['queue']
            for metric in queue:
                # Queue name is not metric and we read it already above
                if metric == 'queue':
                    continue

                if metric == 'size':
                    description = 'Total number of workers'
                else:
                    description = 'Number of ' + metric + ' workers'

                print(queue_name, '_', metric, ":", queue[metric])
                c = CounterMetricFamily("judge0_queue_"+metric, description, labels=['queue'])
                c.add_metric([queue_name], queue[metric])
                yield c

if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1)
