
## Problem Statement

*Using Wikipedia as your datasource, build a representation of the London Underground. Deploy your model in the cloud, then build a web API that will allow it to be queried.*

Attempt the following goals in order, see how far you can get in the time you have available.

*Step 1* - Fetch the list of stations from:
https://en.wikipedia.org/wiki/List_of_London_Underground_stations

*Step 2* - Build a representation of the stations and the connections between them.

*Step 3* - Now, add a new source, and update your model with DLR stations from:
https://en.wikipedia.org/wiki/List_of_Docklands_Light_Railway_stations

*Step 4* - Can you use your model to answer some simple questions? Which station has the most interchanges? Which line is the longest?

*Step 5* - Can you use your model for route-planning? For instance, can it tell you the best route from Farringdon to Canary Wharf?

*Step 6* - If you haven't already, create a server in the cloud, and deploy what you've written to it.

*Step 7* - Now expose your model through a REST API, so a caller can make the following queries:

    GET /station/{station-name}
    GET /station/{station-name}/interchanges
    GET /line/{line-name}/list-stations
    GET /route/{start-station-name}/{destination-station-name}

## Implementation
I've completed steps 1-3. I've given some examples of what's possible with the generated graph structure in `index.py > show_graph_ops/1`

When deciding the best route, the graph traversal algorithms just have least number of edges to go by. There's no information about the length of each edge.

I was unfamiliar with data scraping in Python, as a lot of my recent experience of scraping and parsing has been with Elixir. I've tried to make the functions not rely on external state, as I'd do in Elixir. I've written some very basic tests, but didn't have time to write more.

I've used the NetworkX library for graphing. Given more time, I would have wired up a Neo4j instance with Docker.

Just for ease of development, I've built some basic caching functionality, but these won't be available using Docker.

To run using Docker, just run `docker-compose up`. There's an `output` directory, that'll have `data.json` placed into it. The data in that file is a dictionary of objects, in the format:

```
"Abbey Road": {
	"lines": [
		"Docklands Light Railway"
	],
	"links": [
		{
			"line": "Docklands Light Railway",
			"station": "Stratford High Street"
		},
		{
			"line": "Docklands Light Railway",
			"station": "West Ham"
		}
	],
	"name": "Abbey Road",
	"station_link": "/wiki/Abbey_Road_DLR_station",
	"zones": [
		"3"
	]
}
```

It's easy to build a graph given this data structure, which I've done in the `index.py > build_graph/1` function.