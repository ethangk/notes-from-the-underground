
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import json

import UndergroundParser
import DLRParser
import StationParser
import NetworkManager

WIKI_LINK = "https://en.wikipedia.org"

# Fetch the index pages for the provided systems
def fetch_station_index_pages(station_sources):
  parsed_sources = []
  for station_source in station_sources:
    list_of_stations_html = NetworkManager.fetch(
      WIKI_LINK, station_source
    )
    source_type = None
    if "dockland" in station_source.lower():
      source_type = "dockland"
    if "underground" in station_source.lower():
      source_type = "underground"

    parsed_sources.append((BeautifulSoup(list_of_stations_html, 'html.parser'), source_type))

  return parsed_sources

# Parse fetch and parse individual station pages
def fetch_and_parse_station(station_link):
  content = NetworkManager.fetch(
    WIKI_LINK, station_link
  )

  return BeautifulSoup(
    content, 'html.parser'
  )

def entry():
  stations = {}
  for (source, source_type) in fetch_station_index_pages(
    [
      "/wiki/List_of_London_Underground_stations",
      "/wiki/List_of_Docklands_Light_Railway_stations"
      ]):
    t_stations = {}

    # Take the parsed contents of the index page, and extract the station information
    if source_type == "underground":
      t_stations = UndergroundParser.parse_index(source)
    if source_type == "dockland":
      t_stations = DLRParser.parse_index(source)
    
    # Add the parsed stations into the overall station dictionary
    for station in t_stations:
      stations[station] = t_stations[station]

    # Fetch the individual station pages, extract the preceeding and following stations from it
    for station in stations:
      print("Working through {}".format(station))
      parsed_station_page = fetch_and_parse_station(stations[station]['station_link'])

      table_rows = parsed_station_page.find_all('tr')

      stations[station]["links"] = StationParser.generate_links_from_tables(table_rows, ["underground", "dlr"])
      stations[station]["lines"] = StationParser.extract_lines_from_links(stations[station]["links"])

  with open('./output/data.json', 'w') as fp:
    json.dump(stations, fp, sort_keys=True, indent=4)
  return

def load_dict_from_cache():
  with open('data.json', 'r') as fp:
    stations = json.load(fp)
  draw_graph(stations)

# This is a method I was using to visualise the graph that I was buildling
# It serves as an example of what can be done with the generated data structure
def draw_graph(stations):
  G = nx.Graph()
  nodes = []
  for station in stations:
    station_data = stations[station]
    station_attrs = {
      "lines": station_data["lines"],
      "zones": station_data["zones"]
    }
    nodes.append((station, station_attrs))
    G.add_node(station, **station_attrs)
  
  for station in stations:
    for link in stations[station]["links"]:
      if link["line"] == "Northern":
        G.add_edge(station, link["station"], color='r')
      else:
        G.add_edge(station, link["station"], color='black')

  pos = nx.spring_layout(G)

  edges = G.edges()
  colors = [G[u][v]['color'] for u, v in edges]

  nx.draw(G, pos, edges=edges, edge_color=colors, with_labels=True)
  plt.show()


entry()
