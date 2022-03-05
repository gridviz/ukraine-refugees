import pandas as pd
import urllib.request, json

# Pull the refugee data by day

totals_url = "https://data2.unhcr.org/population/get/timeseries?widget_id=283561&sv_id=54&population_group=5457&frequency=day&fromDate=1900-01-01&currentSeries=0"

with urllib.request.urlopen(totals_url) as url:
    totals = json.loads(url.read().decode())

total_df = (
    pd.DataFrame(totals["data"]["timeseries"])
    .rename(columns={"data_date": "date"})
    .drop(["unix_timestamp"], axis=1)
)

total_df["cumsum"] = total_df["individuals"].cumsum()

# Pull the refugee data by country 

locations_url = "https://data2.unhcr.org/population/get/sublocation?geo_id=0&forcesublocation=1&widget_id=283557&sv_id=54&color=%233c8dbc&color2=%23303030&population_group=5460"

with urllib.request.urlopen(locations_url) as url:
    locations = json.loads(url.read().decode())

locations_df = (
    pd.DataFrame(locations["data"])
    .rename(columns={"geomaster_name": "country", "geomaster_id": "id"})
    .drop(
        [
            "admin_level",
            "source",
            "population_groups_concat",
            "population_group_id",
            "individuals_type",
            "demography_type",
            "households",
            "population_groups",
            "color",
            "published",
            "lat_max",
            "lon_max",
            "lat_min",
            "lon_min",
        ],
        axis=1,
    )
)

## Exports

total_df.to_csv("../data/processed/ukraine_refugees_totals_timeseries.csv", index=False)
locations_df.to_csv("../data/processed/ukraine_refugees_totals_countries.csv", index=False)