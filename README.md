# Sked Parser

[![image](https://img.shields.io/travis/l3d00m/sked_parser.svg)](https://travis-ci.com/l3d00m/sked_parser)

Parses Ostfalia University [`sked`](https://www.sked.de/) timetables into a JSON format than can be used inside [SplusEins](https://github.com/SplusEins/SplusEins).

# Installation & Usage

1. Install python>=3.8, git and pip
2. Clone this repository: `git clone git@github.com:l3d00m/sked_parser.git` and `cd sked_parser`.
2. Install the tool with pip from the cloned (i.e. current) folder: `python -m pip install .`.
3. Copy `secrets.example.yaml` into `secrets.yaml` and fill it with your Ostfalia credentials.
4. Modify `config.yaml` with your timetable URLs. See below for syntax reference.
5. Run the tool by executing `sked-parser`. It'll then create the desired `timetables.json`.

## `config.yaml` syntax reference
This is how the file looks like: 

```yaml
plans:
  - url: https://stundenplan.ostfalia.de/e/ # Required, the "overview" URL which directly lists the single timetables for that faculty
    faculty: Elektrotechnik # Required, faculty name which will be displayed to the user on spluseins.de
  - url: https://stundenplan.ostfalia.de/i/Semester/Semester-Liste/
    faculty: Informatik
    graphical: false # Optional, defaults to true. Only needs to be specified if the timetables are in "list" form.
  - url: https://stundenplan.ostfalia.de/v/stundenplan/bee/
    faculty: Versorgungstechnik
    shorthand_syntax: True # Optional, defaults to false. See section shorthand syntax further below.
current_sem: "ws20" # Current semester string that will be appended to the IDs (to have unique IDs for each semester)
```


## Command line options

usage: `sked-parser [-h] [-c CONFIG_FILE] [-s SECRETS_FILE] [-o OUT_FILE]`

* `-c CONFIG_FILE`: Path to the main YAML configuration file (default: `config.yaml` in current directory)
* `-s SECRETS_FILe` Path to the YAML secrets file containing ostfalia user and password (default: `secrets.yaml` in current directory)
* `-o OUT_FILE` Where to store the resulting JSON file (default: `timetables.json` in current directory)


# How it works

The single timetable are scraped from each specified timetable overview page. The link of that timetable (called `skedPath` in SplusEins) and its description/label are then stored and further processed:

## Label optimization
The label is optimized by removing any faculty names, duplicated white spaces and any current semester strings (like `4. Semester` or `- 5. Sem.`). Optionally it's possible to only use the abbreviation of the course name:

### Shorthand syntax optimization
If the timetables of the current faculty are listed as `long form of course (Abbreviation) - additional info`, it is possible to set `shorthand_syntax` to true in the `config.yaml`. In that case the tool will remove the `long form of course` and only keep `Abbreviation - additional info` to keep the label as short as possible in the UI. For example the faculty "Versorgungstechnik" uses course names like `Bio- und Umwelttechnik (BEE) - PO18`, which will be simplified to `BEE - PO18` when `shorthand_syntax` is set to true for that faculty / overview page.

## Semester extraction
The semester of that timetable is retrieved by parsing the stored description with a regex searching for a number followed by any non-alphanumeric character and then `Sem`. See [the tests for extract_semester](tests/test_scraper.py) for all allowed/possible variants.


## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
