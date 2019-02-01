import unicodedata
import Common

# Take every table row from a page, and extract the indicies of the start and end of the transport links for a given system
def parse_easy_table_rows(rows, system):
  start_index = -1
  end_index = -1
  found_easy_table = False
  for i, row in enumerate(rows):
    row_text = row.text.lower()
    if ("preceding station" in row_text and "following station" in row_text):
      found_easy_table = True

    # I found that I needed to be fairly specific with what I'm looking for when trying to find links for a given system
    # The tables include an image with an alt text of the system name, which is the giveaway
    if (found_easy_table and system in row_text and row.find('img') is not None and system in row.find('img')["alt"].lower()):
      if system in row.find('img')["alt"].lower():
        start_index = i
    elif (found_easy_table):
      if (start_index is not -1):
        if (row.has_attr('style') or len(row.find_all('td')) == 0):
          end_index = i
          break

  return (start_index, end_index)

# Looks for Bakerloo line, Northern line, etc or Docklands Light Railway
def is_easy_table_line(content):
  return " line" in content or "Docklands Light Railway" in content

# I've called the table that lists the preceeding and following stations, and their line, for a given station the 'easy table'
# When I first started looking at the problem, I didn't notice the table existed for every page (as it's below the references in some cases)
# so I was checking if a given station had an 'easy table', but the name has stuck


def parse_easy_table(rows, start_index, end_index):
  if end_index is not -1:
    wanted_rows = rows[start_index:end_index]
  else:
    wanted_rows = rows[start_index:]
  links = []

  # This is a risky move. The layout of the table is such that sometimes there'll be
  # a station named in the preceding or following column, but don't have a line attached to it
  line = None
  for row in wanted_rows:
    if (row is None or row.text.strip() == ''):
      continue

    tds = row.find_all('td')
    partial_links = []
    for td in tds:
      td_text = unicodedata.normalize("NFKD", td.text)
      if is_easy_table_line(td_text):
        line = td.find("a").text.replace(" line", "")

      # could also do ' or "Terminus"' in td_text, but it's not neccessary at the moment, that can be inferred from the graph
      # If there's only one link for a given line, it's the end of the line
      if "towards" in td_text:
        station = Common.clean_name(td.find("div").text)
        partial_links.append({"station": station})
    for i in range(len(partial_links)):
      partial_links[i]["line"] = line

    links += partial_links

  return links

# Take every table row and extract the transport links for both the underground and DLR
def generate_links_from_tables(table_rows, sources):
  links = []
  for easy_source in sources:
    (start_index, end_index) = parse_easy_table_rows(table_rows, easy_source)

    parsed_easy_table = parse_easy_table(table_rows, start_index, end_index)
    links += parsed_easy_table
  return links

# Generate a list of unique lines from the links array
def extract_lines_from_links(links):
  partial_links = []
  for link in links:
    partial_links.append(link["line"])
  return list(set(partial_links))
