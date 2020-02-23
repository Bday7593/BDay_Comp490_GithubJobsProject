# Brian Day
# Comp 490 - Development Seminar

import sqlite3
from typing import Tuple
from geotext import GeoText

import GithubJobsAPI
import StackOverflowJobsRSS


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS jobs(
    id TEXT PRIMARY KEY,
    company_url TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT DEFAULT NULL,
    title TEXT NOT NULL,
    job_type TEXT DEFAULT NULL
    );''')


# description TEXT DEFAULT NULL


# from https://www.sqlitetutorial.net/sqlite-python/insert/
def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO JOBS(id, company_url, company, location, title, job_type)
              VALUES(?,?,?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, task)
    return cursor.lastrowid


def insert_github_jobs_into_jobs_db(github_jobs_list):
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    for item in github_jobs_list:  # cycle though the list
        # place = GeoText(item['location'])
        task_1 = (item['id'], item['company_url'], item['company'], item['location'], item['title'], item['type'])
        create_task(conn, task_1)
    close_db(conn)  # close database when all done.
    print("Github jobs available:           " + str(len(github_jobs_list)))


def get_geotext_location(places):
    city, country = "", ""
    found_city, found_country = False, False
    # print(str(places.cities) + ", " + str(places.countries))
    if len(places.cities) > 0:
        # print("city: " + places.cities[0])
        city = places.cities
        found_city = True
    if len(places.countries) > 0:
        # print("country: " + places.countries[0])
        country = places.countries
        found_country = True
    if found_city is True and found_country is True:
        location = str(city[0] + ", " + country[0])
        # print("location:    " + location)
    elif found_city is True:
        location = str(city[0])
        # print("location:    " + location)
    elif found_country is True:
        location = str(country[0])
        # print("location:    " + location)
    else:
        location = "Remote"
    return location


def insert_stack_overflow_jobs_into_jobs_db(stack_overflow_jobs_data):
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    for post in stack_overflow_jobs_data:  # cycle though the list
        places = GeoText(post.title)
        location = get_geotext_location(places)
        if post.title.find("full-time") <= 9:
            job_type = "Full-time"
        elif post.title.find("full time") <= 1:
            job_type = "Full-time"
        else:
            job_type = "part-time"
        task_1 = (post.guid, post.link, post.author, location, post.title, job_type)
        create_task(conn, task_1)
    close_db(conn)  # close database when all done.
    print("Stack Overflow jobs available:   " + str(len(stack_overflow_jobs_data)))


# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
def select_all_jobs(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM jobs")

    rows = cur.fetchall()

    # for row in rows:
    #    print("Company: " + row[2] + "      Location: " + row[3])
    return rows


def main():
    github_jobs_list = GithubJobsAPI.github_jobs_search()  # store github job data into the list.
    stack_overflow_jobs_data = StackOverflowJobsRSS.stack_overflow_jobs_search()  # store stack overflow jobs
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    setup_db(cursor)

    # methods to do the inserting into db.
    insert_github_jobs_into_jobs_db(github_jobs_list)
    insert_stack_overflow_jobs_into_jobs_db(stack_overflow_jobs_data)
    select_all_jobs(conn)
    close_db(conn)


if __name__ == '__main__':
    main()
