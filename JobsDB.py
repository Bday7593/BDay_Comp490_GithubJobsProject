# Brian Day
# Comp 490 - Development Seminar

import sqlite3
from typing import Tuple, Dict, Any
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
    company_url TEXT DEFAULT NULL,
    company TEXT DEFAULT NULL,
    location TEXT DEFAULT NULL,
    title TEXT DEFAULT NULL,
    job_type TEXT DEFAULT NULL,
    description TEXT DEFAULT NULL,
    created_at TEXT DEFAULT NULL
    );''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_locations(
    location TEXT DEFAULT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL
    );''')


def create_table(cursor: sqlite3.Cursor, description: Dict[str, str], table_name: str):
    # build a create table statement, the column names are the keys in the dictionary
    # the column type and constraints are the values in the dictionary
    statement_start = f'''CREATE TABLE IF NOT EXISTS {table_name} ('''
    column_text = ""
    for column_name in description:
        if len(column_text) > 0:
            column_text = f"{column_text},"
        column_text = f"""{column_text}
{column_name} {description[column_name]}"""
    create_statement = f"{statement_start} {column_text});"
    cursor.execute(create_statement)
    return create_statement


def make_column_description_from_json_dict(json_rep: Dict[str, Any]) -> Dict[str, str]:
    """This is a first pass at what the Pragmatic programmer talks about in the DRY section
    In this case we don't want to represent the structure of the json data we download in our
    code if we can help it, so I'm building the description of the table columns by analyzing the
    dictionary"""
    descriptor = {}  # this is our output a mapping of column names to descriptions to build our table
    for key in json_rep:
        # column_constraint = ''  # start with empty constraint then find the type of the data and choose the correct
        # SQL type
        if type(json_rep[key]) is str:
            column_constraint = 'TEXT'
        elif type(json_rep[key]) is int:
            column_constraint = 'INTEGER'
        elif type(json_rep[key]) is float:
            column_constraint = 'REAL'
        else:
            column_constraint = 'BLOB'  # Blob data type is a generic byte by byte type
        if len(descriptor) == 0:  # we will assume that the first item in the JSON dict is the primary key
            column_constraint = f"{column_constraint} PRIMARY KEY"  # WARNING! this only works in python 3.6+
        descriptor[key] = column_constraint
    return descriptor


def drop_table(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE {}".format(table_name))
    print("Table: '{}' has been dropped ".format(table_name))


# from https://www.sqlitetutorial.net/sqlite-python/insert/
def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO JOBS(id, company_url, company, location, title, job_type, description, created_at)
              VALUES(?,?,?,?,?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, task)
    return cursor.fetchall()


# from https://www.sqlitetutorial.net/sqlite-python/insert/
def create_task_insert_locations_db(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    sql = ''' INSERT INTO JOB_LOCATIONS(location, lat, lon)
              VALUES(?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, task)
    return cursor.lastrowid


def create_task_filter(conn, task):
    """
        Create a new task
        :param conn:
        :param task:
        :return:
        """
    sql = ''' SELECT * 
                FROM jobs 
                INNER JOIN job_locations ON jobs.location = job_locations.location
                WHERE ? = ? '''
    cursor = conn.cursor()
    cursor.execute(sql, task)
    result = cursor.fetchall
    print(result)
    return result


def insert_locations_into_job_locations_db(job_location, lat, lon):
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    task_1 = (job_location, lat, lon)
    create_task_insert_locations_db(conn, task_1)
    close_db(conn)  # close database when all done.


def insert_github_jobs_into_jobs_db(github_jobs_list):
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    for item in github_jobs_list:  # cycle though the list
        # place = GeoText(item['location'])
        task_1 = (item['id'], item['company_url'], item['company'], item['location'], item['title'], item['type'],
                  item['description'], item['created_at'])
        create_task(conn, task_1)
    close_db(conn)  # close database when all done.
    print("Github jobs available:           " + str(len(github_jobs_list)))


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
        task_1 = (post.guid, post.link, post.author, location, post.title, job_type, post.description, post.published)
        create_task(conn, task_1)
    close_db(conn)  # close database when all done.
    print("Stack Overflow jobs available:   " + str(len(stack_overflow_jobs_data)))


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


# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
def select_all_rows(table):
    """
    Query all rows in the tasks table
    :param table:
    :return:
    """
    conn, cursor = open_db("JobsDB.sqlite")
    cursor.execute("SELECT * FROM {}".format(table))

    rows = cursor.fetchall()
    close_db(conn)
    return rows


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


def show_technology_from_job_table(conn, search_term):
    """
       Query all rows in the tasks table
       :param search_term:
       :param conn: the Connection object
       :return:
       """
    cursor = conn.cursor()
    # task = ("description", search_term)
    # result = create_task_filter(conn, task)
    cursor.execute(" SELECT * FROM jobs WHERE description LIKE '%{}%'".format(search_term))
    result = cursor.fetchall()
    # result = cursor.fetchall()
    # for row in result:
    # print(f' jobs.location: {row[0]}. lat: {row[1]}. lon: {row[2]}. company: {row[3]}. title: {row[4]}.')
    return result


def show_company_from_job_table(conn, search_term):
    """
       Query all rows in the tasks table
       :param search_term:
       :param conn: the Connection object
       :return:
       """
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM jobs WHERE company LIKE '%{}%'".format(search_term))
    result = cursor.fetchall()
    # for row in result:
    # print(f' jobs.location: {row[0]}. lat: {row[1]}. lon: {row[2]}. company: {row[3]}. title: {row[4]}.')
    return result


def show_title_from_job_table(conn, search_term):
    """
       Query all rows in the tasks table
       :param search_term:
       :param conn: the Connection object
       :return:
       """
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM jobs WHERE title LIKE '%{}%'".format(search_term))
    result = cursor.fetchall()
    # for row in result:
    # print(f' jobs.location: {row[0]}. lat: {row[1]}. lon: {row[2]}. company: {row[3]}. title: {row[4]}.')
    return result


def show_created_at_from_job_table(conn):
    """
       Query all rows in the tasks table
       :param conn: the Connection object
       :return:
       """
    cursor = conn.cursor()
    cursor.execute(" SELECT * FROM jobs WHERE created_at ")
    result = cursor.fetchall()
    # for row in result:
    # print(f' jobs.location: {row[0]}. lat: {row[1]}. lon: {row[2]}. company: {row[3]}. title: {row[4]}.')
    return result


# This code constructs a query for the given table, column, and value and
# returns True if there is at least one row with the required value, otherwise it returns False.
# https://stackoverflow.com/questions/39282991/python-checking-sql-database-column-for-value
def has_value(cursor, table, column, value):
    query = 'SELECT * from {} WHERE {} = ? LIMIT 1'.format(table, column)
    return cursor.execute(query, (value,)).fetchone() is not None


def fill_jobs_table():
    github_jobs_list = GithubJobsAPI.github_jobs_search()  # store github job data into the list.
    stack_overflow_jobs_data = StackOverflowJobsRSS.stack_overflow_jobs_search()  # store stack overflow jobs
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    setup_db(cursor)

    # methods to do the inserting into db.
    insert_github_jobs_into_jobs_db(github_jobs_list)
    insert_stack_overflow_jobs_into_jobs_db(stack_overflow_jobs_data)
    select_all_rows("jobs")
    close_db(conn)


def main():
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    setup_db(cursor)


if __name__ == '__main__':
    main()
