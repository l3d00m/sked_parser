"""Console script for sked_parser."""
import argparse
import logging
import sys

import yaml

from sked_parser import app

log = logging.getLogger("sked_parser")


def load_yaml_conf(yaml_file):
    """Helper function to load the configuration yaml files"""
    with open(yaml_file, 'r') as stream:
        return yaml.safe_load(stream)


def main():
    # Add helpfullogging handler
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s (%(filename)s:%(lineno)d) %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    # Add argparse for help text and future enhancements
    parser = argparse.ArgumentParser(description='Convert sked timetables from overview URLs into a readable format for spluseins.de')
    parser.parse_args()
    # Contains the urls and other configuration
    config = load_yaml_conf("config.yaml")
    # Contains only the secrets to access ostfalia sked URLs
    secrets = load_yaml_conf("secrets.yaml")

    app.main(config, secrets)


if __name__ == "__main__":
    sys.exit(main())
