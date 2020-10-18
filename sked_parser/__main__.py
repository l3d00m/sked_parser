"""Console script for sked_parser."""
import argparse
import logging
import sys
from pathlib import Path

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
    parser = argparse.ArgumentParser(description='Convert sked timetables from overview URLs into a readable format for spluseins.de',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-c", "--config-file", type=str, default="config.yaml", help="Path to the main yaml configuration file")
    parser.add_argument("-s", "--secrets-file", type=str, default="secrets.yaml", help="Path to the yaml secrets file containing ostfalia user and password")
    parser.add_argument("-o", "--out-file", type=str, default="timetables.json", help="Where to store the resulting json file")
    args = parser.parse_args()
    # Contains the urls and other configuration
    config = load_yaml_conf(Path(args.config_file).resolve())
    # Contains only the secrets to access ostfalia sked URLs
    secrets = load_yaml_conf(Path(args.secrets_file).resolve())

    app.main(config, secrets, Path(args.out_file).resolve())


if __name__ == "__main__":
    sys.exit(main())
