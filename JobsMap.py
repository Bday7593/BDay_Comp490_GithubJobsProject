# Brian Day
# Comp 490 - Development Seminar

# import plotly.graph_objects as go
# import pandas as pd
# import plotly.express as px
from geopy import Nominatim
# from geotext import GeoText

import JobsDB


# us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")


def main():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    us_cities = JobsDB.select_all_jobs(conn)

    for item in us_cities:
        locator = Nominatim(user_agent="myGeocoder")
        # location = locator.geocode("Paris, France")
        # places = GeoText(item.title)
        location = locator.geocode(item[3])
        if "Remote" in item[3]:
            print("Remote")
        else:
            try:
                print("Location: {} Latitude = {}, Longitude = {}".format(item[3], location.latitude,
                                                                          location.longitude))
            except AttributeError:
                print("Not a valid location")
    """
    fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State"],
                            color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()
    """


if __name__ == '__main__':
    main()
