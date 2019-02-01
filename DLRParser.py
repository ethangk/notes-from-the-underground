import Common

# Parse a row from the DLR index page
def parse_index_table_row(row):
  tds = row.find_all('td')
  if len(tds) == 0:
    return (None, None)

  # Get the station name and href, clean them up a little
  station_name = Common.clean_name(row.select("td")[0].text)
  station_link = row.select("td a")[0]['href'].split("#")[0]

  # Looks like we didn't get a station
  if (len(station_link) == 0):
    print("Skipping empty station link")
    return (None, None)

  tds = row.select("td")
  station_data = {'station_link': station_link,
                  'name': station_name, "lines": []}

  # I haven't mapped the column names to something that I can reference easy
  for i, td in enumerate(tds):
    if (i == 3):
      station_data['zones'] = Common.clean_name(td.text).split(" & ")

  return (station_name, station_data)



# Parse the DLR index page
def parse_index(source):
  stations = {}
  tables = source.select('.wikitable')

  if (len(tables) != 1):
    print("Got the wrong number of tables for the DLR index, something unexpected has happened with the page")
  else:
    rows = tables[0].find('tbody').find_all('tr')
    for tr in rows:
      (station_name, station_data) = parse_index_table_row(tr)
      if station_name is not None and station_data is not None:
        stations[station_name] = station_data

  return stations

