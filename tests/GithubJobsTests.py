# Brian Day
# Comp 490 - Development Seminar

import GithubJobsDB


# one test should the method that retrieves the data from the web and assure that you get more than 100 data items
def test_stored_data():
    conn, cursor = GithubJobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    cursor.execute("select * from jobs")
    results = cursor.fetchall()
    print(len(results))
    GithubJobsDB.close_db(conn)
    assert len(results) >= 100, "Needs to be >= 100"


# The second test should check to see that the database contains a field that you know should be there.
def test_write_jobs_to_db():
    conn, cursor = GithubJobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    post_id = "Full Time"
    cursor.execute("select id from JOBS where id=?", (post_id,))
    data = cursor.fetchall()
    data_found = False
    if data is None:
        GithubJobsDB.close_db(conn)
    else:
        data_found = True
    GithubJobsDB.close_db(conn)
    assert data_found


# write a test to make sure that the table exists in the database after your program runs
def test_does_table_exits():
    conn, cursor = GithubJobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    cursor = conn.cursor()
    # get the count of tables with the name
    cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='jobs' ''')
    # if the count is 1, then table exists
    if cursor.fetchone()[0] == 1:
        # print('Table exists.')
        GithubJobsDB.close_db(conn)
        assert True


def good_data():
    g_id, g_url, g_company, g_location, g_title, g_job_type = "GOOD DATA", "GOOD DATA", "GOOD DATA", "GOOD DATA", \
                                                              "GOOD DATA", "GOOD DATA "
    return g_id, g_url, g_company, g_location, g_title, g_job_type


# write a series of tests to make sure your function/method that saves to the database works properly. (send some
# data as a parameter to your function, and have it save the data to the database). Try to save some good data,
# try to save some bad data and make sure that this test fails (and mark it as expected to fail so that the rest of
# the tests continue)
def insert_into_jobs_db(g_id, g_url, g_company, g_location, g_title, g_job_type):
    # g_id, g_url, g_company, g_location, g_title, g_job_type = good_data()
    conn, cursor = GithubJobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    cursor = conn.cursor()
    # this will attempt to insert a series of strings into the database which should pass no problem.
    try:
        cursor.execute(f'''INSERT INTO JOBS (id, company_url, company, location, title, job_type)
                        VALUES ('{g_id}', '{g_url}', '{g_company}', '{g_location}', '{g_title}', '{g_job_type}')''')
        GithubJobsDB.close_db(conn)
    except ValueError:
        print("Oops! There was no valid string data input")
        GithubJobsDB.close_db(conn)


def test_inserting_data_into_db():
    b_id, b_url, b_company, b_location, b_title, b_job_type = 100, "bAd DaTa", "This is bad data", 75, '!', 8.6
    insert_into_jobs_db(b_id, b_url, b_company, b_location, b_title, b_job_type)
    g_id, g_url, g_company, g_location, g_title, g_job_type = good_data()
    insert_into_jobs_db(g_id, g_url, g_company, g_location, g_title, g_job_type)

# write one more automated test
# sometimes my program fails before it starts and i think it is because it the connection to the website fails.
# I will write an automated test on testing the url connection.
# def test_url_connection():
