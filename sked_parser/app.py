import json
import logging
from time import sleep

from sked_parser import scraper

log = logging.getLogger("sked_parser")


def write_timetable_json(tables, file_path):
    with open(file_path, 'w') as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)
        f.write('\n')


def raise_for_duplicated_ids(dict_to_check):
    """Helper function that prints an error if key `id` of that dict list has duplicated values.
        Also raises if dict key 'id' does not exist."""
    ids = [item['id'] for item in dict_to_check]
    duplicated_ids = set([x for x in ids if ids.count(x) > 1])
    if len(duplicated_ids) > 0:
        log.critical(f"Zwei oder mehr Pläne haben die gleiche ID bekommen: {duplicated_ids}")


def is_valid_item(table):
    """Returns whether a table is allowed in spluseins. Used for filtering some unwanted items (Klausurenpläne)"""
    if "klausur" in table['label'].lower():
        # Klausurenpläne entfernen
        return False
    if "block" in table['skedPath'].lower():
        # Blockveranstaltungen (Fakultät E) erstmal raus
        return False
    if "ss2021" in table['skedPath'].lower():
        # irgendwas altes, raus damit
        return False
    if "ss 21" in table['label'].lower():
        # irgendwas altes, raus damit
        return False
    if "sose" in table['label'].lower():
        # irgendwas altes, raus damit
        return False
    if table['faculty'] == 'Soziale Arbeit' and "fernstudiengang" in table['label'].lower():
        # schlechte formatierung, wird ignoriert
        return False
    return True


def main(config, secrets, out_files):
    tables = []
    for plan in config["plans"]:
        tuples = scraper.get_links(plan['url'], secrets, plan['faculty'])
        if len(tuples) == 0:
            log.warning(f"URL {plan['url']} hat keine Pläne.")
        for label, sked_path in tuples:
            faculty_short = scraper.get_faculty_shortcode(sked_path)
            degree = scraper.guess_degree(label, sked_path)
            semester = scraper.extract_semester(label, sked_path) or "Sonstige"
            sked_id = scraper.create_id(sked_path, faculty_short, config['current_sem'], semester)
            label = scraper.optimize_label(label, plan.get('shorthand_syntax', False))
            plan_type = plan.get('type', 'graphical')
            if "alt" in sked_path:
                label += " alt"
            tables.append(dict(skedPath=sked_path, label=label, faculty=plan['faculty'],
                               type=plan_type, id=sked_id, semester=semester, degree=degree))
        sleep(1)
    tables = list(filter(is_valid_item, tables))
    # Sort first by faculty, then by master/bachelor, then by semester and last by alphabetical label
    tables = sorted(tables, key=lambda x: (x['faculty'], x['degree'], str(x['semester']), x['label'], x['id']))
    raise_for_duplicated_ids(tables)
    for out_file in out_files:
        write_timetable_json(tables, out_file)

    log.info(f"Parsed {len(tables)} timetables sucessfully into JSON.")
    return 0
