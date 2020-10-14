# Sked Parser

[![image](https://img.shields.io/travis/l3d00m/sked_parser.svg)](https://travis-ci.com/l3d00m/sked_parser)

Parses Ostfalia sked timetables into JSON

# How it works

## Scraping
The sked URLs are scraped from the specified timetable overview pages. The link itself and its description is stored.

## Semester
The current semester is retrived by parsing the stored description with a regex searching for a number followed by Sem. or Semester.

TODO

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
