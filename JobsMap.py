# Brian Day
# Comp 490 - Development Seminar

import pandas as pd
import plotly.express as px
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

import Filters
import JobsDB


def do_geocode(address):
    locator = Nominatim(user_agent="myGeocoder")
    geocode_location = locator.geocode(address)
    return geocode_location.latitude, geocode_location.longitude


def cache_coordinates_in_db(cursor, job_locations_list):
    # conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    for item in job_locations_list:
        print("Trying to find Remote:   " + str(item[3].find("Remote")))
        if str(item[3].find("Remote")) != "-1":
            print("This is a remote job")
        else:
            if JobsDB.has_value(cursor, "job_locations", 'location', item[3]) is True:
                print("We found " + item[3] + " in the database.")
            else:
                print(item[3] + " does not exist!!! inserting into database.")
                try:
                    latitude, longitude = do_geocode(item[3])
                    JobsDB.insert_locations_into_job_locations_db(item[3], latitude, longitude)
                except GeocoderTimedOut:
                    print("GEOCODER TIMEDOUT!!!!! BEGIN RECURSIVE FUNCTION.")
                    latitude, longitude = do_geocode(item[3])
                    JobsDB.insert_locations_into_job_locations_db(item[3], latitude, longitude)
                except AttributeError:
                    print("Not a valid location or unknown location.")
    # JobsDB.close_db(conn)
    print()


def create_dataframe(combined_table):
    dict_of_locations = {i: combined_table[i] for i in range(0, len(combined_table))}
    df = pd.DataFrame.from_dict(dict_of_locations, orient='index',
                                columns=['location', 'lat', 'lon', 'company', 'title'])
    print("DATAFRAME:")
    print(df)
    return df


# https://plot.ly/python/mapbox-layers/
def map_jobs(df):
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="location", hover_data=["company", "title"],
                            color_discrete_sequence=[""], zoom=3, height=900)

    fig.update_layout(
        mapbox_style="white-bg",
        mapbox_layers=[
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": [
                    "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                ]
            },
            {
                "sourcetype": "raster",
                "source": ["https://geo.weather.gc.ca/geomet/?"
                           "SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&BBOX={bbox-epsg-3857}&CRS=EPSG:3857"
                           "&WIDTH=1000&HEIGHT=1000&LAYERS=RADAR_1KM_RDBR&TILED=true&FORMAT=image/png"],
            }
        ])
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


def main():
    # JobsDB.fill_jobs_table()
    # display_map(df)
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")

    # test_location_list = JobsDB.show_technology_from_job_table(conn, "swift")
    # cache_coordinates_in_db(conn, test_location_list)
    # test_combined_table = JobsDB.show_select_with_join_lat_lon(conn)
    # print("TEST_COMBINED_TABLE:")
    # print()

    # Filters.reset_job_locations()
    df = Filters.filter_by_technology("swift")
    # df = Filters.filter_by_company("Apple")
    # map_jobs(df)

    # df = Filters.filter_by_age_of_post("25/02/2020")
    map_jobs(df)
    JobsDB.close_db(conn)


if __name__ == '__main__':
    main()
