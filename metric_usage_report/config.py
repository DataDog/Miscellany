# Your Datadog API Key
API_KEY = ""

# Your Datadog Application Key
APP_KEY = ""

# A list of metric names, values should match metrics present in your account
METRICS_TO_EVAL = ["system.cpu.user", "system.disk.in_use"]

### ADVANCED CONFIGS

# the filename where dashboard api responses are stored to avoid duplicate requests (you shouldn't need to change this)
DB_CACHE_PATH = "db_cache.txt"

# the filename where json results are placed
JSON_OUTPUT_PATH = "results/report.json"

# the filename where csv results are placed
CSV_OUTPUT_PATH = "results/report.csv"

# the filename where markdown results are placed
MARKDOWN_OUTPUT_PATH = "results/report.md"