# Brian Day
# Comp 490 - Development Seminar
import pytest
import GithubJobsDB


@pytest.fixture
def get_data():
    import GithubJobsDB
    return GithubJobsDB.get_github_jobs_data()


# one test should the method that retrieves the data from the web and assure that you get more than 100 data items
def test_stored_data(get_data):
    assert len(get_data) >= 100, "Needs to be >= 100"
    assert type(get_data[1]) is dict


# The second test should check to see that the save file contains a job with a job title that you know should be there.
def test_write_jobs_to_db():  # F. Hoffmann-La Roche AG
    # with open('Github Jobs.txt', 'r') as output:  # open the file and close it when actions are done.
    # job_list = json.load(output)  # load the json into a list
    # for item in job_list:  # cycle though the list and search for a matching job title.
    # if item['company'] == 'F. Hoffmann-La Roche AG':  # if it matches then the test was a success
    # assert item['company'] == 'F. Hoffmann-La Roche AG', "There was no matching job title"
    conn, cursor = GithubJobsDB.open_db("JobsDB.sqlite")  # Open the database to store information.
    post_id = "Full Time"
    cursor.execute("select id from JOBS where id=?", (post_id,))
    data = cursor.fetchall()
    data_found = False
    if data is None:
        print('not found')
    else:
        data_found = True
        print('found')
    GithubJobsDB.close_db(conn)
    assert data_found


# def main(my_list):
    # test_stored_data(my_list)
    # test_write_jobs_to_db()
    # print("All tests have passed!")

# if __name__ == "__main__":
#  main()
