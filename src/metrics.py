from prometheus_client import Counter, Histogram, start_http_server

# Metric Definitions
FILES_SORTED_TOTAL = Counter(
    "files_sorted_total",
    "Total count of files organized into target directories",
    ["category", "status"]  # Status: success, failed
)

FILE_PROCESSING_SECONDS = Histogram(
    "file_processing_seconds",
    "Time spent processing and moving a single file",
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

UNMATCHED_FILES_TOTAL = Counter(
    "unmatched_files_total",
    "Count of files that did not match any tag rule"
)

def start_metrics_server(port: int = 8000):
    start_http_server(port)
    print(f"Prometheus Metrics Endpoint live at http://localhost:{port}/metrics")