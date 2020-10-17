from sked_parser.scraper import extract_semester, optimize_label


def test_extract_semester_normal():
    """Test normal/default string"""
    sem_str = "Angewandte Informatik - 1. Semester"
    assert extract_semester(sem_str, "") == 1


def test_extract_semester_multiple_numbers():
    """Test string with other numbers"""
    sem_str = "Wasser- und Bodenmanagement - PO 2018 - 3. Semester"
    assert extract_semester(sem_str, "") == 3
    sem_str = "Wasser- und Bodenmanagement - 20. Sem"
    assert extract_semester(sem_str, "") is None


def test_extract_semester_abbrevation():
    """Test string with shortened Sem."""
    sem_str = "1. Sem. EIT"
    assert extract_semester(sem_str, "") == 1


def test_extract_semester_no_delimiter():
    """Test that strings with no delimiter or non-digit after number match as well"""
    sem_str = "IVG_1_1.Sem"
    assert extract_semester(sem_str, "") == 1
    sem_str = "1 Sem Informatik"
    assert extract_semester(sem_str, "") == 1


def test_extract_semester_no_semester():
    """Test string without semester returns a string, not an int"""
    sem_str = "IMES Teilzeit 2018"
    assert extract_semester(sem_str, "") is None


def test_extract_semester_duplicated_sem():
    """Test string with duplicated semesters"""
    sem_str = "Soziale Arbeit - 5. Semester - PO 2018 - 5. Semester - Soziale Arbeit"
    assert extract_semester(sem_str, "") == 5


def test_extract_semester_multiple_semesters():
    """Test that in case of multiple semesters, only the last one is returned (for now)"""
    sem_str = "Bio- und Umwelttechnik (BEE ) - 3. - 4.  Semester"
    assert extract_semester(sem_str, "") == 4


def test_extract_semester_url_fallback():
    """Test that URL parsing is used when no desc is provided"""
    url_str = "i/Semester/Semester-Liste/I-B.Sc. WI 1. Sem..html"
    assert extract_semester("Nothing in here", url_str) == 1


def test_optimize_label_strip_semester():
    """Verify the semester is correctly stripped from the label"""
    # Semester at end
    in_str = "Bauingenieurwesen - 1. Semester"
    assert optimize_label(in_str, False) == "Bauingenieurwesen"
    # Semester at start
    in_str = "4. Semester Servicetechnik und Prozesse"
    assert optimize_label(in_str, False) == "Servicetechnik und Prozesse"
    # Duplicated / multiple semester strings
    in_str = "5. Semester - PO 2018 - 5. Semester - Handel"
    assert optimize_label(in_str, False) == "PO 2018 - Handel"
    # Multiple semesters in one substring
    in_str = "Umwelttechnik - 3. - 4.  Semester"
    assert optimize_label(in_str, False) == "Umwelttechnik"
    # Semester shorthand used
    in_str = "Wirtschaftsinformatik 5. Sem."
    assert optimize_label(in_str, False) == "Wirtschaftsinformatik"
    # Even shorter semester shorthand used
    in_str = "Wirtschaftsinformatik 5 Sem"
    assert optimize_label(in_str, False) == "Wirtschaftsinformatik"


def test_optimize_label_shorthand_strip():
    """Verify that the shorthand is correctly used instead of the longform if requested"""
    # Simple shorthand and text after it
    in_str = "Energie- und Gebäudetechnik (EGT) - TGA"
    assert optimize_label(in_str, True) == "EGT - TGA"
    # Shorthand with special chars and extra whitespace
    in_str = "Energie- und Gebäudetechnik ( EGT / EGTiP ) - TGA"
    assert optimize_label(in_str, True) == "EGT / EGTiP - TGA"
    # Shorthand string with numbers in it should not be replaced/used
    in_str = "Vertiefung CE (PO18)"
    assert optimize_label(in_str, True) == "Vertiefung CE (PO18)"
