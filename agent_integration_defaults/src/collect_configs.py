# This script collects configuration files from the Datadog Agent's conf.d directory
# and outputs them into a single YAML file for easy review.
# It looks for both conf.yaml and conf.yaml.example files, prioritizing conf.yaml if both exist.
# It also handles YAML parsing errors gracefully, including them in the output.

# Usage: Run this script in an environment where the Datadog Agent's conf.d directory is accessible.
# The output will be saved to /output/collected_integrations.yaml.
import os
import yaml

BASE_DIR = "/app/integrations-core"
output = {}

# Get sorted list of directory names
for item in sorted(os.listdir(BASE_DIR)):
    full_path = os.path.join(BASE_DIR, item)

    # Skip non-configuration directories
    if item.startswith(".") or item == "__pycache__":
        # Skip hidden files and directories
        continue
    if item == "tests":
        # Skip tests directory
        continue
    if item.startswith("datadog_checks_"):
        # Skip datadog_checks_ directories
        continue
    
    # Check if the item is a directory
    if os.path.isdir(full_path):
        # Check for conf.yaml and conf.yaml.example files
        conf_path = os.path.join(full_path, "datadog_checks", item, "data", "conf.yaml")
        example_path = os.path.join(full_path, "datadog_checks", item, "data", "conf.yaml.example")

        config = None

        if os.path.isfile(conf_path):
            with open(conf_path, "r") as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError:
                    config = None

        if config is None and os.path.isfile(example_path):
            with open(example_path, "r") as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError:
                    config = None

        output[item] = {"config": config}

# Dump with top-level keys sorted
with open("/output/collected_integrations.yaml", "w") as f:
    yaml.dump(dict(sorted(output.items())), f, sort_keys=True)
