import asyncio
import os
import time
from aiohttp import ClientSession, ClientConnectionError, ClientResponseError
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, GaugeMetricFamily

JUDGE0_API_URL = os.getenv("JUDGE0_API_URL", "https://ce.judge0.com")
AUTH_TOKEN_HEADER = os.getenv("AUTH_TOKEN_HEADER", "X-Auth-Token")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
PORT = int(os.getenv("PORT", 8000))
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", 15))  # Fetch every 60 seconds

HEADERS = {
  AUTH_TOKEN_HEADER: AUTH_TOKEN
}

# Shared storage of fetched data
judge0_workers = {}


if AUTH_TOKEN == None:
    print('AUTH_TOKEN not provided')
    exit(1)

class CustomCollector(object):
    def collect(self):
        # Track created metrics
        metrics = {}
        for queue in judge0_workers:
            queue_name = queue['queue']
            for metric in queue:
                # Queue name is not metric and we read it already above
                if metric == 'queue':
                    continue
                if metric == 'size':
                    description = 'Total number of submissions in queue'
                else:
                    description = 'Number of ' + metric + ' workers'


                metric_name = f'judge0_workers_{metric}'
                # register each metric only once
                if metric_name not in metrics:
                    metrics[metric_name] = GaugeMetricFamily(metric_name, description, labels=['queue'])
                metrics[metric_name].add_metric([queue_name], queue[metric])
        for name in metrics:
            yield metrics[name]

async def fetch_data(session):
    global judge0_workers

    while True:
        try:
            async with session.get(JUDGE0_API_URL+'/workers', headers=HEADERS) as response:
                response.raise_for_status()  # Raise exception for non-2xx responses
                judge0_workers = await response.json()

        except (ClientConnectionError, ClientResponseError) as e:
            print(f"Error fetching data: {e}")

        await asyncio.sleep(REFRESH_INTERVAL)

async def main():
    # Start Prometheus metrics server on port 8000
    start_http_server(PORT)

    # Register custom collector with Prometheus registry
    custom_collector = CustomCollector()
    REGISTRY.register(custom_collector)

    # Create a session for fetching JSON data
    async with ClientSession() as session:
        # Create separate tasks for JSON fetching and metric serving
        json_fetching_task = asyncio.create_task(fetch_data(session))

        # Run task concurrently
        await asyncio.gather(json_fetching_task)

if __name__ == '__main__':
    print('Start serving metrics from', JUDGE0_API_URL, 'on port', PORT)
    # Start asynchronous event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
