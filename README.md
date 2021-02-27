# Illinois-ltc-covid-data


The two data pipelines in this repo were used to create the visualization of covid outbreaks in long-term care (ltc) facilities here:

https://observablehq.com/d/97189a57f1ee1079

Both pipelines are written with Python, commandline tools, and Makefiles, per Datamade's [data making guidelines](https://github.com/datamade/data-making-guidelines)

The pipeline to download and clean the data about ltc outbreaks lives in the `illinois_ltc_pipeline`. The data was collected by volunteers from the [Covid Tracking Project](https://covidtracking.com/) from the Illinois Department of Public Health (IDPH)'s [website](https://www.dph.illinois.gov/covid19/long-term-care-facility-outbreaks-covid-19).

A notable part of that data pipeline is that ltc outbreaks on IDPH's page are only reported by facility name and county, not by address or unique ID that CMS assigns long-term care facilities. To geolocate these entities then, the name and county are searched via the Google Maps API and if the facility is found, the lat and long are recorded. The script for that is `processors/geocode_locations.py`


The underlying map of Illinois in the above visualization was created through D3's mapping module and TopoJSON. The pipeline downloads the Census shapefile for Illinois counties and transforms it into TopoJSON that can be easily mapped by D3's functions. The process for those geographic transformations basically matches Mike Bostock's tutorial [here](https://medium.com/@mbostock/command-line-cartography-part-1-897aa8f8ca2c).


The two Juptyer notebooks in the repo were used for initial data exploration and cleaning.



### Data recreation instructions

Clone this repo

#### Long-term Care data

`cp example.env .env`

You will need to actually get a Google Maps Geolocation API Key and place it in your `.env` file.
`cd illinois_ltc_pipeline`
`make all`

The Makefile should perform all steps, including setting up a virtual environment, downloading the data from Covid Tracking Project's Github, geolocating it, and shaping it into a format suitable for the data visualization.

`cd ../illinois_geo_pipeline`
`make all`

This Makefile  downloads Shapefiles from the Census Bureau website, transforms them into GeoJSON, projects them with an Illinois specific projection, and then transforms them again to TopoJSON.

 




