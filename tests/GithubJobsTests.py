# Brian Day
# Comp 490 - Development Seminar
import json


# one test should the method that retrieves the data from the web and assure that you get more than 100 data items
def test_store_data(my_list):
    assert len(my_list) >= 100, "Needs to be >= 100"


# The second test should check to see that the save file contains a job with a job title that you know should be there.
def test_write_jobs_to_file():  # F. Hoffmann-La Roche AG
    with open('Github Jobs.txt', 'r') as output:  # open the file and close it when actions are done.
        job_list = json.load(output)  # load the json into a list
        for item in job_list:  # cycle though the list and search for a matching job title.
            if item['company'] == 'F. Hoffmann-La Roche AG':  # if it matches then the test was a success
                assert item['company'] == 'F. Hoffmann-La Roche AG', "There was no matching job title"


# for reference purposes
# def test_sum():
# assert sum([1, 2, 3]) == 6, "Should be 6"
def main(my_list):
    # test_sum() # for reference purposes
    test_store_data(my_list)
    # test_write_jobs_to_file()
    print("All tests have passed!")


if __name__ == "__main__":
    # test_sum() # for reference purposes
    # test_store_data()
    # test_write_jobs_to_file()
    # print("All tests have passed!")
    the_list = []
    main(the_list)
