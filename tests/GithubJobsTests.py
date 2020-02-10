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
