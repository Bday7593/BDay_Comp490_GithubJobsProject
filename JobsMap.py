# Brian Day
# Comp 490 - Development Seminar

import pandas as pd
import plotly.express as px
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

import JobsDB


# us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")


# This code constructs a query for the given table, column, and value and
# returns True if there is at least one row with the required value, otherwise it returns False.
# https://stackoverflow.com/questions/39282991/python-checking-sql-database-column-for-value
def has_value(cursor, table, column, value):
    query = 'SELECT * from {} WHERE {} = ? LIMIT 1'.format(table, column)
    return cursor.execute(query, (value,)).fetchone() is not None


def do_geocode(address):
    locator = Nominatim(user_agent="myGeocoder")
    geocode_location = locator.geocode(address)
    return geocode_location.latitude, geocode_location.longitude


def cache_coordinates_in_db(job_locations_list):
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    for item in job_locations_list:
        print("Trying to find Remote:   " + str(item[3].find("Remote")))
        if str(item[3].find("Remote")) != "-1":
            print("This is a remote job")
        else:
            if has_value(cursor, "job_locations", 'location', item[3]) is True:
                print("We found " + item[3] + " in the database.")
            else:
                print(item[3] + " does not exist!!! inserting into database.")
                try:
                    latitude, longitude = do_geocode(item[3])
                    JobsDB.insert_locations_into_jobs_locations_db(item[3], latitude, longitude)
                except GeocoderTimedOut:
                    print("GEOCODER TIMEDOUT!!!!! BEGIN RECURSIVE FUNCTION.")
                    latitude, longitude = do_geocode(item[3])
                    JobsDB.insert_locations_into_jobs_locations_db(item[3], latitude, longitude)
                except AttributeError:
                    print("Not a valid location or unknown location.")
    JobsDB.close_db(conn)


def create_dataframe(job_lat_lon):
    dict_of_locations = {i: job_lat_lon[i] for i in range(0, len(job_lat_lon))}
    df = pd.DataFrame.from_dict(dict_of_locations, orient='index',
                                columns=['location', 'lat', 'lon', 'company', 'title'])
    print("dataframe:")
    print(df)
    return df


def map_jobs(df):
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="location", hover_data=["company", "title"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=900)

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


def show_select_with_join_lat_lon(conn):
    """
       Query all rows in the tasks table
       :param conn: the Connection object
       :return:
       """
    cursor = conn.cursor()
    cursor.execute(f'''SELECT jobs.location, job_locations.lat, job_locations.lon, company, title
    FROM jobs
    INNER JOIN job_locations ON
    jobs.location = job_locations.location''')
    result = cursor.fetchall()
    # for row in result:
    # print(f' jobs.location: {row[0]}. lat: {row[1]}. lon: {row[2]}. company: {row[3]}. title: {row[4]}.')
    return result


def main():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    # job_locations_list = JobsDB.select_all_jobs(conn, "jobs")
    # cache_coordinates_in_db(job_locations_list)
    # job_lat_lon = JobsDB.select_all_jobs(conn, "job_locations")

    testing = show_select_with_join_lat_lon(conn)
    print("Testing:")
    print(testing)
    print()

    df = create_dataframe(testing)
    map_jobs(df)

    # show_select_with_join_lat_lon(conn, cursor)

    JobsDB.close_db(conn)


if __name__ == '__main__':
    main()
