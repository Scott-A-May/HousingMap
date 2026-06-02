import requests
import pandas as pd
import geopandas as gpd
import folium
from mapclassify import NaturalBreaks

# ── 1. CONFIGURATION ──────────────────────────────────────────────
API_KEY   = "REDACTED"      # paste your Census API key
STATE     = "27"                 # 27 = Minnesota, change to your state
YEAR      = 2022

# ACS variables we want:
# B25077_001E = Median home value
# B25002_003E = Vacant housing units
# B25003_002E = Owner-occupied units
# B25003_003E = Renter-occupied units
VARIABLES = "NAME,B25077_001E,B25002_003E,B25003_002E,B25003_003E"

# ── 2. PULL DATA FROM CENSUS API ──────────────────────────────────
url = (
    f"https://api.census.gov/data/{YEAR}/acs/acs5"
    f"?get={VARIABLES}"
    f"&for=county:*"
    f"&in=state:{STATE}"
    f"&key={API_KEY}"
)

response = requests.get(url)
data     = response.json()

# First row is column headers
df = pd.DataFrame(data[1:], columns=data[0])

# ── 3. CLEAN AND SHAPE THE DATA ───────────────────────────────────
df = df.rename(columns={
    "B25077_001E": "median_home_value",
    "B25002_003E": "vacant_units",
    "B25003_002E": "owner_occupied",
    "B25003_003E": "renter_occupied",
})

# Convert to numbers (Census returns everything as strings)
for col in ["median_home_value","vacant_units","owner_occupied","renter_occupied"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Create a FIPS code to join to geographic data (state + county codes)
df["FIPS"] = df["state"] + df["county"]

print(f"Pulled {len(df)} counties")
print(df[["NAME","median_home_value"]].head())

# ── 4. GET COUNTY SHAPEFILE (GEOGRAPHIC BOUNDARIES) ───────────────
# Census TIGER shapefile for counties - no download needed, reads directly
shapefile_url = (
    "https://www2.census.gov/geo/tiger/GENZ2022/shp/"
    "cb_2022_us_county_500k.zip"
)
gdf = gpd.read_file(shapefile_url)

# Filter to our state and create matching FIPS
gdf = gdf[gdf["STATEFP"] == STATE].copy()
gdf["FIPS"] = gdf["STATEFP"] + gdf["GEOID"].str[-3:]

# ── 5. JOIN DATA TO GEOGRAPHY ─────────────────────────────────────
merged = gdf.merge(df, on="FIPS", how="left")
merged = merged.dropna(subset=["median_home_value"])

# ── 6. BUILD THE INTERACTIVE MAP ──────────────────────────────────
# Center map on state centroid
center = [merged.geometry.centroid.y.mean(),
          merged.geometry.centroid.x.mean()]

m = folium.Map(location=center, zoom_start=7, tiles="CartoDB positron")

# Choropleth layer - color counties by median home value
folium.Choropleth(
    geo_data    = merged.__geo_interface__,
    data        = merged,
    columns     = ["FIPS", "median_home_value"],
    key_on      = "feature.properties.FIPS",
    fill_color  = "YlOrRd",
    fill_opacity= 0.75,
    line_opacity= 0.3,
    legend_name = "Median Home Value ($)",
    bins        = 6,
).add_to(m)

# Clickable tooltips showing detail for each county
folium.GeoJson(
    merged.__geo_interface__,
    style_function  = lambda x: {"fillOpacity": 0, "weight": 0},
    tooltip = folium.GeoJsonTooltip(
        fields  = ["NAME_x", "median_home_value", "vacant_units",
                   "owner_occupied", "renter_occupied"],
        aliases = ["County", "Median Home Value ($)",
                   "Vacant Units", "Owner Occupied", "Renter Occupied"],
        localize= True,
    )
).add_to(m)

# ── 7. SAVE AND VIEW ──────────────────────────────────────────────
output_file = "housing_opportunity_map.html"
m.save(output_file)
print(f"Map saved! Open '{output_file}' in your browser.")