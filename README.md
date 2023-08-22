Judge0 exporter
===============

Read Judge0 API endpoints and expose them in Prometheus format

Configuration variables
-----------------------

| Environment variable | Default value | Description |
+----------------------+---------------+-------------+
| JUDGE0_API_URL | `https://ce.judge0.com` | API to read metrics from |
| AUTH_TOKEN_HEADER | `X-Auth-Token` | Authentication token (a.k.a. API key) header |
| AUTH_TOKEN | `` | Actual authentication token (a.k.a. API key) value |
| PORT | `8000` | Port to expose Prometheus metrics |

Limitations
-----------

* for now exporter read only /workers endpoint
