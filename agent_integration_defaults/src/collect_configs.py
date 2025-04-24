# This script collects configuration files from the Datadog Agent's conf.d directory
# and outputs them into a single YAML file for easy review.
# It looks for both conf.yaml and conf.yaml.example files, prioritizing conf.yaml if both exist.
# It also handles YAML parsing errors gracefully, including them in the output.

# Usage: Run this script in an environment where the Datadog Agent's conf.d directory is accessible.
import os
import yaml

CONF_ROOT = "/etc/datadog-agent/conf.d"
OUTPUT_FILE = "collected_integrations.yaml"

def normalize_integration_name(name):
    return name[:-2] if name.endswith(".d") else name

def normalize_config_path(path):
    return path.replace("conf.yaml.example", "conf.yaml")

def find_configs():
    integrations = {}
    for entry in os.scandir(CONF_ROOT):
        if entry.is_dir():
            raw_name = entry.name
            conf_dir = entry.path
            conf_file = os.path.join(conf_dir, "conf.yaml")
            example_file = os.path.join(conf_dir, "conf.yaml.example")

            selected_file = None
            if os.path.exists(conf_file):
                selected_file = conf_file
            elif os.path.exists(example_file):
                selected_file = example_file

            if selected_file:
                try:
                    with open(selected_file, "r") as f:
                        config = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    config = {"_error": f"Failed to parse YAML: {str(e)}"}

                name = normalize_integration_name(raw_name)
                path = normalize_config_path(selected_file)

                integrations[name] = {
                    "config_path": path,
                    "config": config
                }

    return integrations

def main():
    integrations = find_configs()
    with open(OUTPUT_FILE, "w") as out:
        yaml.dump(integrations, out, default_flow_style=False, sort_keys=False)
    print(f"✅ Collected {len(integrations)} integrations into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
