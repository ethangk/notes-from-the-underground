import Common

# Parse a row from the underground stations index, return a tuple
# with the station name and station data in
def parse_index_table_row(row):
  station_name = Common.clean_name(row.select("th")[0].text)
  station_link = row.select("th a")[0]['href'].split("#")[0]
  if (len(station_link) == 0):
    # skip it
    print("Skipping empty station link for {}".format(station_name))
    return (None, None)
  else:
    tds = row.select("td")
    station_data = { 'station_link': station_link, 'name': station_name }
    for i, td in enumerate(tds):
      if (i == 3):
        station_data['zones'] = td.text.split(" & ")
  return (station_name, station_data)

# Parse the Underground index page
def parse_index(source):
  stations = {}
  tables = source.select('.wikitable')
  if (len(tables) != 2):
    print("Got the wrong number of tables for the underground index, something unexpected has happened with the page")
  else:
    rows = tables[0].select('tbody tr')
    for tr in rows:
      (station_name, station_data) = parse_index_table_row(tr)
      if station_name is not None and station_data is not None:
        stations[station_name] = station_data

  return stations
