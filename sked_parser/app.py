import json
import logging

from sked_parser import scraper

log = logging.getLogger("sked_parser")


def write_timetable_json(tables, file_path):
    with open(file_path, 'w') as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)


def main(config, secrets, out_file="timetables.json"):
    tables = []
    for plan in config["plans"]:
        tuples = scraper.get_links(plan['url'], secrets['sked'])
        for label, sked_path in tuples:
            faculty_short = scraper.get_faculty_shortcode(plan['url'])
            degree = scraper.guess_degree(label, sked_path)
            sked_id = scraper.create_id(sked_path, faculty_short)
            semester = scraper.extract_semester(label, sked_path) or "Ohne Semester"
            label = scraper.optimize_label(label, plan.get('shorthand_syntax', False))
            is_graphical = plan.get('graphical', True)
            tables.append(dict(skedPath=sked_path, label=label, faculty=plan['faculty'],
                               graphical=is_graphical, id=sked_id, semester=semester, degree=degree))
    write_timetable_json(tables, out_file)

    log.info(f"Successfully parsed {len(tables)} timetables and wrote them to {out_file}.")

    for table in tables:
        # print(table['label'])
        pass
    return 0
