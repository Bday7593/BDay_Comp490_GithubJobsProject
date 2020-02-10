# Brian Day
# Comp 490 - Development Seminar

import sqlite3
from typing import Tuple

import GithubJobsAPI


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
    location TEXT NULL,
    title TEXT NOT NULL,
    job_type TEXT NOT NULL
    );''')
# description TEXT DEFAULT NULL


def insert_into_jobs_db(cursor: sqlite3.Cursor, list_id, list_company_url, list_company, list_location,
                        list_title, list_job_type):
    # list_description):
    # print(str(len(my_list)) + " jobs available.")
    # print(f'''INSERT INTO JOBS (id, company_url, company, location, title, description)
    cursor.execute(f'''INSERT INTO JOBS (id, company_url, company, location, title, job_type)
            VALUES ('{list_id}', '{list_company_url}', '{list_company}', '{list_location}', '{list_title}',
                '{list_job_type}')''')
    # , '{list_description}')''')


def get_github_jobs_data():
    return jobs_list


jobs_list = []


def main():
    # jobs_list = []
    GithubJobsAPI.github_jobs_search(jobs_list)  # run the job search to store the job data into the list.

    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    setup_db(cursor)
    print(str(len(jobs_list)) + " jobs available.")
    for item in jobs_list:  # cycle though the list
        insert_into_jobs_db(cursor, item['id'], item['company_url'], item['company'], item['location'], item['title'],
                            item['type'])
        # item['description'])
    # print(type(conn))
    close_db(conn)

    # GithubJobsTests.main(jobs_list)


if __name__ == '__main__':
    main()
