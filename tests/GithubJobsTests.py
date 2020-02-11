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
