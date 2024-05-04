from prometheus_client import Counter, Histogram, start_http_server


API_CALLS_TOTAL = Counter('api_calls_total', 'Total number of API calls')
API_CALLS_SUCCESSFUL = Counter('api_calls_successful', 'Number of successful API calls')
API_CALLS_FAILED = Counter('api_calls_failed', 'Number of failed API calls')
API_RESPONSE_TIME = Histogram('api_response_time_seconds', 'API response time in seconds')


@API_RESPONSE_TIME.time()
def api_endpoint():
    API_CALLS_TOTAL.inc()
    success = True  
    if success:
        API_CALLS_SUCCESSFUL.inc()
    else:
        API_CALLS_FAILED.inc()

start_http_server(8000)
