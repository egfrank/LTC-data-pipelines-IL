import argparse
import csv
import os

import googlemaps
from dotenv import load_dotenv


def write_csv(filename, data_dict):
    with open(filename, "w", newline="") as outfile:
        headers = list(data_dict[0].keys())
        writer = csv.DictWriter(outfile, headers, delimiter=",", quotechar='"')
        writer.writeheader()
        writer.writerows(data_dict)


parser = argparse.ArgumentParser()
parser.add_argument("input", help="CSV with facilties to geolocate")
parser.add_argument(
    "output_geolocated", help="CSV with geolocation information appended to facilties."
)
parser.add_argument(
    "output_not_located", help="CSV with those facilities we failed to locate."
)
args = parser.parse_args()

# Load API KEY from .env
load_dotenv()
gmaps = googlemaps.Client(os.getenv("GOOGLE_MAPS_API_KEY"))

with open(args.input, newline="") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
    facilities = [row for row in reader]


located_facilities = []
not_located_facilities = []

for ltc_fac in facilities:
    lookup = "{}, {} County, IL".format(ltc_fac["facility_name"], ltc_fac["county"])
    print("looking up facility {}".format(lookup))
    result = gmaps.geocode(lookup)

    if len(result) == 0:
        not_located_facilities.append(ltc_fac)
        continue

    result = result[0]
    if "health" in result["types"]:
        ltc_fac["address"] = result["formatted_address"]
        ltc_fac["latitude"] = result["geometry"]["location"]["lat"]
        ltc_fac["longitude"] = result["geometry"]["location"]["lng"]
        located_facilities.append(ltc_fac)
    else:
        not_located_facilities.append(ltc_fac)

write_csv(args.output_geolocated, located_facilities)
if len(not_located_facilities) > 0:
    write_csv(args.output_not_located, not_located_facilities)
