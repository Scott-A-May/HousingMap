# Housing Opportunity Map

An interactive choropleth map of Minnesota county-level housing metrics using Census data and Folium.

## Overview

This project pulls 2022 ACS 5-Year Estimates from the U.S. Census Bureau API for Minnesota counties, joins the data to Census TIGER shapefiles, and renders an interactive choropleth map color-coded by median home value with county-level tooltips.

## Notes
- Data sourced from the U.S. Census Bureau ACS 5-Year Estimates (2022)
- Geography: Minnesota counties (87 total)
- Interactive map saved as `housing_opportunity_map.html`
- Folium maps require a live environment to render interactively — view the live map via GitHub Pages

## Data Source

- **Dataset:** American Community Survey (ACS) 5-Year Estimates
- **Vintage:** 2022
- **Source:** U.S. Census Bureau API
- **Geography:** Minnesota counties (FIPS: 27)
- **Variables:**
  - Median home value
  - Vacant housing units
  - Owner-occupied units
  - Renter-occupied units

## Features

- Pulls live county-level housing data from the U.S. Census Bureau API
- Joins Census data to TIGER shapefiles for accurate county boundaries
- Renders an interactive choropleth map color-coded by median home value
- Displays county-level tooltips with median home value, vacancy, and occupancy data
- Outputs a standalone HTML map file viewable in any browser

## Project Structure# HousingMap

HousingMap/
├── housing_map.py     # Main script
├── index.html         # GitHub Pages entry point
└── requirements.txt   # Python dependencies

## Technologies Used

- Python 3.14
- pandas
- geopandas
- folium
- mapclassify
- U.S. Census Bureau API
- Census TIGER Shapefiles (GENZ2022)

## Setup

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Census API key to a `.env` file:  CENSUS_API_KEY=your_key_here
4. Run the script:  python housing_map.py
5. Open `housing_opportunity_map.html` in your browser

## Author

Scott A. May | [GitHub](https://github.com/Scott-A-May)
