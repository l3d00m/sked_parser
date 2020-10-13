import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

log = logging.getLogger(__name__)


def get_links(link, auth):
    resp = requests.get(link, auth=HTTPBasicAuth(auth['user'], auth['pass']))
    soup = BeautifulSoup(resp.content, 'lxml')
    tables = []
    valid_url_regex = re.compile(r'^https://stundenplan\.ostfalia\.de/\w/.*\.html$', re.IGNORECASE)
    for this_url in soup.find_all('a', href=True):
        absolute_url = urljoin(link, this_url['href'])
        if valid_url_regex.match(absolute_url):
            sked_path = absolute_url[len("https://stundenplan.ostfalia.de"):]
            tables.append((this_url.text, sked_path))
    return tables


def extract_id(sked_path, faculty):
    # Get the id from the url, which is the last part excluding the (.).html
    # Also extract the faculty one character ID
    id_re = re.compile(r'(\w)\/.*\/(.*?)\.+html', re.IGNORECASE)
    m = id_re.search(sked_path)
    if not m:
        log.error(f"Path {sked_path} did not match to ID regex, should not happen")
        return ""
    faculty_id = m.group(1).lower()

    sked_id = m.group(2).lower().strip()
    # Replace any non alphanumeric chars with underscore
    sked_id = re.sub(r'\W+', '_', sked_id, flags=re.ASCII)
    # Remove any strings like SoSe, WS, SS including the year from the id
    sked_id = re.sub(r'((s|w)s|(so|w)se)(_?\d+)(_\d+)?_?', '', sked_id)
    sked_id = sked_id.strip("_")

    # Remove some faculty specific stuff to shorten the id:
    sked_id = sked_id.replace('soziale_arbeit', '')
    sked_id = sked_id.replace('wirtschaftsingenieur_', '')
    sked_id = sked_id.replace('energie_und_gebaeudetechnik_', '')
    sked_id = sked_id.replace('bio_und_umwelttechnik_', '')
    sked_id = sked_id.replace('bachelor_', '')
    sked_id = sked_id.replace('b_sc_', '')
    faculty_prefix = f"{faculty_id}_"
    if not sked_id.startswith(faculty_prefix):
        sked_id = faculty_prefix + sked_id
    return sked_id


def extract_semester(desc):
    sem = 0
    sem_regex = re.compile(r'(?:- )?(\d)\..*Sem(?:ester|\.)? ?', re.IGNORECASE)
    m = sem_regex.search(desc)
    if m:
        sem = int(m.group(1))
        desc = sem_regex.sub('', desc).strip()
    return desc, sem


def extract_desc(desc):
    desc = desc.replace('S-', '')

def extract_degree(desc):
    if "master" in desc.lower():
        return "Master"
    else:
        return "Bachelor"
