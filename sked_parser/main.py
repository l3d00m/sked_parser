"""Main module."""
import json
import logging

import yaml

from sked_parser import scraper

log = logging.getLogger(__name__)


def load_yaml_conf():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    with open("secrets.yaml", 'r') as stream:
        secrets = yaml.safe_load(stream)
    return config, secrets


def write_json(tables):
    with open("timetables.json", 'w') as outfile:
        json.dump(tables, outfile, indent=2, ensure_ascii=False)


def main():
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(name)s: %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    config, secrets = load_yaml_conf()
    tables = []
    for plan in config["plans"]:
        tuples = scraper.get_links(plan['url'], secrets['sked'])
        for label, sked_path in tuples:
            degree = scraper.extract_degree(label, sked_path)
            sked_id = scraper.extract_id(sked_path, plan['faculty'])
            label, semester = scraper.extract_semester(label)
            label = scraper.optimize_label(label)
            tables.append(dict(skedPath=sked_path, label=label, faculty=plan['faculty'],
                               graphical=plan['graphical'], id=sked_id, semester=semester, degree=degree))
    write_json(tables)

    for table in tables:
        log.debug(table['label'])


if __name__ == "__main__":
    main()
