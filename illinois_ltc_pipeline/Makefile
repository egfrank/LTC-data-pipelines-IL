join: 
	sql2csv --db sqlite:///db/IL_covid.db --query \
	"select c.*, g.address, g.latitude, g.longitude from clean_covid_cases c JOIN geo_covid_cases g ON (g.facility_name = c.facility_name and g.county = c.county) ORDER BY c.facility_name, c.date" \
	> finished/joined_covid_facilities.csv

insert:
	csvsql --db sqlite:///db/IL_covid.db --table geo_covid_cases --insert intermediate/geo_covid_cases.csv --overwrite
	csvsql --db sqlite:///db/IL_covid.db --table clean_covid_cases --insert intermediate/clean_covid_cases.csv --overwrite

intermediate/geo_covid_cases.csv: intermediate/facility_names.csv venv
	@echo "Geolocating the provided facility names."
	$(VENV)/python3 processors/geocode_locations.py $< $@ intermediate/unlocated_covid_cases.csv

intermediate/facility_names.csv: raw/covid_cases.csv venv
	@echo "Getting data to geolocate distinct facilities."
	csvcut -c "facility_name,county,state" $< \
	| csvsql --query 'SELECT DISTINCT facility_name, county, state FROM stdin ORDER BY facility_name' \
	> $@

intermediate/clean_covid_cases.csv: raw/covid_cases.csv venv
	@echo "Selecting the columns that we want to keep."
	csvcut -c "facility_name,date,county,state,facility_cms_id,outbreak_status,resident_staff_positives,resident_staff_deaths" \
	$< > $@

raw/covid_cases.csv:
	@echo "Downloading the COVID19Tracking project csv of Illinois data"
	wget --no-use-server-timestamps \
	https://github.com/COVID19Tracking/long-term-care-data/raw/master/facilities_il.csv -O $@
	touch $@

raw/facility_list.csv:
	@echo "Downloading the CMS directory of LTC faciltiies"
	wget --no-use-server-timestamps \
	https://data.cms.gov/provider-data/sites/default/files/resources/e8e81a0158f5934d38fcd5d8db1d0458_1605453862/NH_ProviderInfo_Nov2020.csv \
	-O $@
	touch $@

raw/facility_covid_info.csv:
	@echo "Downloading the covid data LTC faciltiies have reported to CMS"
	wget --no-use-server-timestamps \
	https://data.cms.gov/api/views/s2uc-8wxp/rows.csv?accessType=DOWNLOAD \
	-O $@
	touch $@

.PHONY: all clean insert join view

all: intermediate/geo_covid_cases.csv intermediate/facility_names.csv intermediate/clean_covid_cases.csv

clean:
	rm -Rf finished/*
	rm -Rf intermediate/*
	rm -Rf *.csv
	rm -Rf db
	rm -Rf *.db

include Makefile.venv