import logging
import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

# Helpful for testing
# import requests_cache
# requests_cache.install_cache()

log = logging.getLogger("sked_parser")


def get_links(overview_url, auth):
    """Scrape all valid timetable URLS from `overview_url`.

    Args:
        overview_url (str): Faculty timetable overview URL that has all single timetable URLs on it
        auth (dict): Dict containing `user` and `pass` to access the ostfalia timetable module

    Returns:
        List[Tuple]: List of tuples with (url description, sked path)
    """
    resp = requests.get(overview_url, auth=HTTPBasicAuth(auth['user'], auth['pass']))
    soup = BeautifulSoup(resp.content, 'lxml')
    tables = []
    valid_url_regex = re.compile(r'^https://stundenplan\.ostfalia\.de/\w/.+\.html$', re.IGNORECASE)
    for this_url in soup.find_all('a', href=True):
        absolute_url = urljoin(overview_url, this_url['href'])
        if valid_url_regex.match(absolute_url):
            sked_path = absolute_url[len("https://stundenplan.ostfalia.de/"):]
            tables.append((this_url.text, sked_path))
    return tables


def create_id(sked_path, faculty_short, current_sem_str, extracted_semester):
    """Create a unique ID from the `sked_path` (timetable URL) and keep it as short as possible while maintaining readability"""
    # First, get the basic id from the url page, which is the last part excluding the (.).html
    id_re = re.compile(r'\w\/.+\/(.+?)\.+html', re.IGNORECASE)
    m = id_re.search(sked_path)
    if not m:
        raise Exception(f"Path {sked_path} did not match to ID regex, so we can't extract an ID")
    sked_id = m.group(1).lower().strip()

    # Replace any non alphanumeric chars with underscore and remove duplicated underscores
    sked_id = re.sub(r'\W+', '_', sked_id, flags=re.ASCII)
    sked_id = sked_id.replace('__', '_')
    # Remove any strings like SoSe, WS, SS including the year from the id
    sked_id = re.sub(r'((s|w)s|(so|w)se)(_?\d+)(_\d+)?_?', '', sked_id)
    sked_id = sked_id.strip("_")

    # Remove some faculty specific stuff to shorten the id:
    sked_id = sked_id.replace('soziale_arbeit', '')
    sked_id = sked_id.replace('wirtschaftsingenieur_', '')
    sked_id = sked_id.replace('energie_und_gebaeudetechnik_', '')
    sked_id = sked_id.replace('bio_und_umwelttechnik_', '')
    sked_id = sked_id.replace('bachelor', '')
    sked_id = sked_id.replace('b_sc', '')
    sked_id = sked_id.replace('semester_', '')
    sked_id = sked_id.replace('energie_', '')
    sked_id = sked_id.replace('umwelt_', '')
    sked_id = sked_id.replace('_sem', '')
    # Again remove duplicated underscores that have been introduced by the removals before
    sked_id = sked_id.replace('__', '_')
    sked_id = sked_id.strip("_ ")

    if (isinstance(extracted_semester, int)):
        # If semester was successfully extracted, scrape all single digits from ID and add extracted semester back
        sked_id = re.sub(f"_{extracted_semester}" + r'(?=_|$)', '', sked_id)
        sked_id = f"{sked_id}_{extracted_semester}"

    # Prefix the label with the faculty shortcut
    faculty_prefix = f"{faculty_short}_"
    if not sked_id.startswith(faculty_prefix):
        sked_id = faculty_prefix + sked_id
    # Append the current semester string (sth like ws20) at the end
    sked_id = f"{sked_id}_{current_sem_str}"
    return sked_id.lower()


def extract_semester(desc, url):
    """Extract/guess the current semester from the link description or the link using regex."""
    # Find any timetables that are "Wahlpflichfächer"
    for keyword in ["wahlpflicht", "wpf"]:
        if keyword in desc.lower() or keyword in url.lower():
            return "WPF"
    # Try to extract the semester by finding a number followed by non word characters and something starting with Sem
    sem_regex = re.compile(r'(?:^|\D)(\d)\W+Sem', re.IGNORECASE)
    m_desc = sem_regex.search(desc)
    m_url = sem_regex.search(url)
    if m_desc:
        return int(m_desc.group(1))
    elif m_url:
        # Only use the semester from URL if description search was unsuccessful
        return int(m_url.group(1))
    else:
        log.warning(f"Kein Semester bestimmbar bei \"{desc}\" mit sked path \"{url}\")")
        return None


def get_faculty_shortcode(overview_url):
    """Strip the faculty one letter shortcode from the provided overview url"""
    shortcode = overview_url.split("/")[3]
    if len(shortcode) != 1 or not shortcode.isalpha():
        raise Exception("Could not get faculty shorthand from URL")
    return shortcode


def optimize_label(desc, uses_shorthand_syntax):
    """Optimize the user visible label by removing faculty names and try to use only the shorthand of that course if possible"""
    desc = desc.replace('S-', '')
    desc = desc.replace('I-', '')
    desc = desc.replace('B.Sc.', '')
    desc = desc.replace('I-M.Sc.', '')
    desc = desc.replace('Soziale Arbeit -', '')
    if uses_shorthand_syntax:
        # Those faculties writes their modules as "long name (shorthand) additional info"
        # So discard the long name and use only the shorthand but keep the info
        shorthand_re = re.compile(r'^.*?\((\D+?)\)(.*)$')
        m = shorthand_re.search(desc)
        if m:
            shorthand = m.group(1).strip()
            additional_stuff = m.group(2).strip()
            desc = f"{shorthand} {additional_stuff}"
    # Remove any semester related information
    desc = re.sub(r'(\d\. ?-)?-? ?\d\.?\W+Sem(?:ester|\.)?', '', desc)
    # Remove duplicated spaces
    desc = desc.replace('  ', ' ')
    return desc.strip("- ")


def guess_degree(desc, link):
    """Return an estimation whether it's a master or bachelor degree"""
    if "master" in desc.lower() or "m.sc" in desc.lower() or "-m-" in link.lower():
        return "Master"
    else:
        return "Bachelor"
