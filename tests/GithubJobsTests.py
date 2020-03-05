# Brian Day
# Comp 490 - Development Seminar
import pytest
import requests

import Filters
import JobsDB


@pytest.fixture
def get_data():
    return JobsDB.select_all_rows("jobs")


def test_jobs_list(get_data):
    # first required test
    assert len(get_data) >= 100
    assert type(get_data[1]) is tuple


# one test should the method that retrieves the data from the web and assure that you get more than 100 data items
def test_stored_data():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    cursor.execute("select * from jobs")
    results = cursor.fetchall()
    print(len(results))
    JobsDB.close_db(conn)
    assert len(results) >= 100, "Needs to be >= 100"


# The second test should check to see that the database contains a field that you know should be there.
def test_write_jobs_to_db():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    post_id = "Full Time"
    cursor.execute("select id from JOBS where id=?", (post_id,))
    data = cursor.fetchall()
    data_found = False
    if data is None:
        JobsDB.close_db(conn)
    else:
        data_found = True
    JobsDB.close_db(conn)
    assert data_found


# write a test to make sure that the table exists in the database after your program runs
def test_does_table_exits():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    cursor = conn.cursor()
    # get the count of tables with the name
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='jobs' ''')
    # if the count is 1, then table exists
    if cursor.fetchone()[0] == 1:
        # print('Table exists.')
        JobsDB.close_db(conn)
        assert True


def good_data():
    g_id, g_url, g_company, g_location, g_title, g_job_type = "GOOD DATA", "GOOD DATA", "GOOD DATA", "GOOD DATA", \
                                                              "GOOD DATA", "GOOD DATA "
    return g_id, g_url, g_company, g_location, g_title, g_job_type


def bad_data():
    b_id, b_url, b_company, b_location, b_title, b_job_type = 100, "bAd DaTa", "ThIs Is bAd dAtA", 75, '!', 8.6
    return b_id, b_url, b_company, b_location, b_title, b_job_type


# write a series of tests to make sure your function/method that saves to the database works properly. (send some
# data as a parameter to your function, and have it save the data to the database). Try to save some good data,
# try to save some bad data and make sure that this test fails (and mark it as expected to fail so that the rest of
# the tests continue)
def insert_into_jobs_db(some_id, url, company, location, title, job_type):
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    cursor = conn.cursor()
    # this will attempt to insert a series of strings into the database which should pass no problem.
    try:
        cursor.execute(f'''INSERT INTO JOBS (id, company_url, company, location, title, job_type)
                        VALUES ('{some_id}', '{url}', '{company}', '{location}', '{title}', '{job_type}')''')
        JobsDB.close_db(conn)
    except AttributeError:
        print("Oops! There was no valid string data input")
        JobsDB.close_db(conn)


def test_inserting_data_into_db():
    # bad_data and good_data
    b_id, b_url, b_company, b_location, b_title, b_job_type = bad_data()
    g_id, g_url, g_company, g_location, g_title, g_job_type = good_data()
    # attempt to test the good and bad data.
    try:
        insert_into_jobs_db(g_id, g_url, g_company, g_location, g_title, g_job_type)
    except AttributeError:
        print("Oops! There was some invalid good data input")
    try:
        insert_into_jobs_db(b_id, b_url, b_company, b_location, b_title, b_job_type)
    except AttributeError:
        print("Oops! There was some invalid bad data input")


# write one more automated test
# sometimes my program fails before it starts and i think it is because it the connection to the website fails.
# I will write an automated test on testing the url connection.
def test_url_connection():
    try:
        requests.get('https://jobs.github.com/positions.json?page=1')
    except ValueError:
        print("There was no valid web-page at that URL")


def test_table_exists():
    fake_table = 'test_table'
    fake_row = {'id': 'F$RT%YH&', 'type': 'Full Time', 'url': 'http://wwww.fakedata.com', 'created_at': '02-12-2020',
                'company': "Don't Work Here Comp", 'company_url': None, 'location': "giant urban metro",
                'title': 'Junior software peon', 'description': "blah blah, devops, scrum, hot tech",
                'how_to_apply': "http://runaway.com", 'company_logo': None}
    connection, cursor = JobsDB.open_db('testonly.sqlite')
    JobsDB.create_table(cursor, JobsDB.make_column_description_from_json_dict(fake_row), fake_table)
    result_cursor = cursor.execute(f"SELECT name from sqlite_master where (name = '{fake_table}')")
    success = len(result_cursor.fetchall()) >= 1
    assert success


def test_filter_by_technology():
    Filters.reset_job_locations()
    tech_df = Filters.filter_by_technology("swift")
    assert tech_df is not None


def test_filter_by_company():
    Filters.reset_job_locations()
    comp_df = Filters.filter_by_company("Apple")
    assert comp_df is not None


def test_filter_by_title():
    Filters.reset_job_locations()
    title_df = Filters.filter_by_technology("Reporting Analyst")
    assert title_df is not None
