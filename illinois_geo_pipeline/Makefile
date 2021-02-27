GENERATED_FILES = shp/cb_2019_17_tract_500k.zip \
	shp/cb_2019_17_tract_500k.shp \
	geo/il.json \
	geo/il-albers.json \
	geo/il-albers.ndjson \
	geo/il-albers-id.ndjson \
	data/cb_2019_17_tract_B01003.json \
	data/cb_2019_17_tract_B01003.ndjson \
	geo/il-albers-join.ndjson \
	geo/il-albers.density.ndjson \
	topo/il-tracts-topo.json \
	topo/il-simple-topo.json \
	topo/il-quantized-topo.json \
	topo/il-counties.json

GENERATED_SVGS = svg/il-albers.svg \

INTERMEDIATE	= data/cb_2019_17_tract_B01003_cat.ndjson \
	data/cb_2019_17_tract_B01003_split.ndjson

.INTERMEDIATE: $(INTERMEDIATE)

topo/il-counties.json: topo/il-quantized-topo.json
	topomerge -k 'd.id.slice(0, 3)' counties=tracts < $^ > $@

topo/il-quantized-topo.json: topo/il-simple-topo.json
	topoquantize 1e5 < $^ > $@

topo/il-simple-topo.json: topo/il-tracts-topo.json
	toposimplify -p 1 -f \
	< $^ > $@

topo/il-tracts-topo.json: geo/il-albers.density.ndjson
	geo2topo -n \
		tracts=$^ \
		> $@

geo/il-albers.density.ndjson: geo/il-albers-join.ndjson
	ndjson-map 'd[0].properties = {density: Math.floor(d[1].B01003 / d[0].properties.ALAND * 2589975.2356)}, d[0]' \
	< $^ > $@

geo/il-albers-join.ndjson: geo/il-albers-id.ndjson data/cb_2019_17_tract_B01003.ndjson
	ndjson-join 'd.id' $^ > $@

data/cb_2019_17_tract_B01003.ndjson: data/cb_2019_17_tract_B01003_split.ndjson
	@echo "Intermediate step (3/3) to convert population data to NDJSON" 
	ndjson-map '{id: d[2] + d[3], B01003: +d[0]}' < $< > $@

data/cb_2019_17_tract_B01003_split.ndjson: data/cb_2019_17_tract_B01003_cat.ndjson
	@echo "Intermediate step (2/3) to convert population data to NDJSON"
	ndjson-split 'd.slice(1)' < $< > $@

data/cb_2019_17_tract_B01003_cat.ndjson: data/cb_2019_17_tract_B01003.json
	@echo "Intermediate step (1/3) to convert population data to NDJSON"
	ndjson-cat $< > $@

data/cb_2019_17_tract_B01003.json: 
	curl \
	'https://api.census.gov/data/2019/acs/acs5?get=B01003_001E&for=tract:*&in=state:17&key=$(CENSUS_API_KEY)' \
	-o data/cb_2019_17_tract_B01003.json

geo/il-albers-id.ndjson: geo/il-albers.ndjson
	@echo "Extract tract ID as own property"
	ndjson-map 'd.id = d.properties.GEOID.slice(2), d' \
		< $< > $@

geo/il-albers.ndjson: geo/il-albers.json
	@echo "Split projected GeoJSON features into NDJSON"
	ndjson-split 'd.features' \
	< $< \
	> $@

svg/il-albers.svg: geo/il-albers.json
	@echo "Convert projected GeoJSON to SVG and open"
	geo2svg -w 960 -h 960 < $< > $@
	open -a "Google Chrome" $@

geo/il-albers.json: geo/il.json
	@echo "Project GeoJSON using a custom Albers"
	geoproject 'd3.geoConicEqualArea().parallels([38.82, 40.67]).rotate([89.5, 0]).fitSize([960, 960], d)' \
	< $< \
	> $@

geo/il.json: shp/cb_2019_17_tract_500k.shp
	@echo "Convert shapefile to GeoJSON"
	shp2json $< -o $@

shp/cb_2019_17_tract_500k.shp: shp/cb_2019_17_tract_500k.zip
	@echo "Unzip census tracts to extract shapefiles"
	unzip -o $< -d shp
	touch $@

shp/cb_2019_17_tract_500k.zip:
	@echo "Download 2019 census tracts"
	curl 'https://www2.census.gov/geo/tiger/GENZ2019/shp/cb_2019_17_tract_500k.zip' -o $@

all: $(GENERATED_FILES)

allsvgs: $(GENERATED_SVGS)

clean: 
	rm -rf $(GENERATED_FILES) cb_2019* shp/*

install: 
	npm install -g shapefile d3-geo-projection ndjson-cli d3 topojson d3-scale-chromatic

makedir:
	mkdir svg shp geo data topo

.PHONY: install makedir