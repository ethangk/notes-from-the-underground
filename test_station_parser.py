import unittest

import StationParser

def test_is_transit_table_line():
    assert StationParser.is_transit_table_line("Bakerloo line") == True
    assert StationParser.is_transit_table_line("Northern line") == True
    assert StationParser.is_transit_table_line("Docklands Light Railway") == True
    assert StationParser.is_transit_table_line("Something that doesn't look good") == False

def list_diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def test_extract_lines_from_links():
  links = [
    { "line": "Bakerloo" },
    { "line": "Northern" },
    { "line": "Northern" },
    { "line": "Docklands Light Railway" }
  ]

  assert len(list_diff(
    StationParser.extract_lines_from_links(links),
    ["Bakerloo", "Northern", "Docklands Light Railway"]
  )) == 0
