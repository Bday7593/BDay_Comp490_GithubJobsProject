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


def insert_github_jobs_into_jobs_db(github_jobs_list):
    # list_description):
    # print(str(len(my_list)) + " jobs available.")
    # print(f'''INSERT INTO JOBS (id, company_url, company, location, title, description)
    # cursor.execute(f'''INSERT INTO JOBS (id, company_url, company, location, title, job_type)
    #        VALUES ('{list_id}', '{list_company_url}', '{list_company}', '{list_location}', '{list_title}',
    #            '{list_job_type}')''')
    # , '{list_description}')''')
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    for item in github_jobs_list:  # cycle though the list
        task_1 = (item['id'], item['company_url'], item['company'], item['location'], item['title'],
                  item['type'])
        create_task(conn, task_1)
    close_db(conn)  # close database when all done.


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


def main():
    github_jobs_list = []
    # stack_overflow_jobs_data = StackOverflowJobsRSS.stack_overflow_jobs_search()
    GithubJobsAPI.github_jobs_search(github_jobs_list)  # run the job search to store the job data into the list.
    # StackOverflowJobsRSS.stack_overflow_jobs_search(stack_overflow_jobs_list)
    conn, cursor = open_db("JobsDB.sqlite")  # Open the database to store information.
    setup_db(cursor)

    # tasks
    # task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
    # task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

    # create tasks
    # create_task(conn, task_1)
    # create_task(conn, task_2)
    insert_github_jobs_into_jobs_db(github_jobs_list)
    print(str(len(github_jobs_list)) + " jobs available.")

    # for item in github_jobs_list:  # cycle though the list
    #    task_1 = (item['id'], item['company_url'], item['company'], item['location'], item['title'],
    #               item['type'])
    #     create_task(conn, task_1)
    # insert_into_jobs_db(cursor, item['id'], item['company_url'], item['company'], item['location'], item['title'],
    #                    item['type'])
    # item['description'])
    # print(type(conn))
    close_db(conn)


if __name__ == '__main__':
    main()
