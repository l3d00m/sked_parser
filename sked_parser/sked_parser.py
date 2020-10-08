"""Main module."""
import json
import re
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth


def load_yaml_conf():
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)
    with open("secrets.yaml", 'r') as stream:
        secrets = yaml.safe_load(stream)
    return config, secrets


def write_json(tables):
    with open("timetables.json", 'w') as outfile:
        json.dump(tables, outfile, indent=2, ensure_ascii=False)


def get_links(link, auth):
    resp = requests.get(link, auth=HTTPBasicAuth(auth['sked_user'], auth['sked_pass']))
    soup = BeautifulSoup(resp.content, 'lxml')
    tables = []
    valid_url_regex = re.compile(r'^https://stundenplan\.ostfalia\.de/\w/.*\.html$', re.IGNORECASE)
    for this_url in soup.find_all('a', href=True):
        absolute_url = urljoin(link, this_url['href'])
        if valid_url_regex.match(absolute_url):
            tables.append((this_url.text, absolute_url))
    return tables


def main():
    config, secrets = load_yaml_conf()
    tables = []
    for plan in config["plans"]:
        tuples = get_links(plan['url'], secrets)
        for desc, url in tuples:
            if not url.startswith(config['general']['base_url']):
                raise Exception(f"Url {url} did not start with specified base URL")
            sked_path = url[len("https://stundenplan.ostfalia.de"):]
            edited_desc, semester = extract_semester(desc)
            tables.append(dict(skedPath=sked_path, label=edited_desc, faculty=plan['faculty'],
                               graphical=plan['graphical'], id='', semester=semester, degree=''))
    write_json(tables)

    for table in tables:
        print(f"{table['label']}")


def extract_semester(desc):
    sem = 0
    sem_regex = re.compile(r'(?:- )?(\d)\..*Sem(?:ester|\.)? ?', re.IGNORECASE)
    m = sem_regex.search(desc)
    if m:
        sem = int(m.group(1))
        desc = sem_regex.sub('', desc).strip()
    return desc, sem


if __name__ == "__main__":
    main()
