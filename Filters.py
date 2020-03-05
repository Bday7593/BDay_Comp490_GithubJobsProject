# Brian Day
# Comp 490 - Development Seminar

from datetime import datetime
import JobsDB
import JobsMap


# Allow the user to filter by job technology, - DONE
# age of the job posting - DONE
# or company. - DONE
# Allow one other kind of filter of your choice. Tell me about it in your readme.


def reset_job_locations():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")
    JobsDB.drop_table(conn, "job_locations")
    JobsDB.setup_db(cursor)
    JobsDB.close_db(conn)


def filter_by_technology(technology_string):
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")
    location_list = JobsDB.show_technology_from_job_table(conn, technology_string)
    JobsMap.cache_coordinates_in_db(conn, location_list)
    tech_combined_table = JobsDB.show_select_with_join_lat_lon(conn)
    print("TECH_COMBINED_TABLE:")
    tech_df = JobsMap.create_dataframe(tech_combined_table)
    JobsDB.close_db(conn)
    return tech_df


def filter_by_company(company_string):
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")
    location_list = JobsDB.show_company_from_job_table(conn, company_string)
    JobsMap.cache_coordinates_in_db(conn, location_list)
    company_combined_table = JobsDB.show_select_with_join_lat_lon(conn)
    print("COMPANY_COMBINED_TABLE:")
    company_df = JobsMap.create_dataframe(company_combined_table)
    JobsDB.close_db(conn)
    return company_df


def filter_by_age_of_post(day_month_year):
    try:
        stripped_date = datetime.strptime(day_month_year, '%d/%m/%Y')
        # print("stripped_date: {}".format(str(stripped_date)))
    except ValueError:
        print("Date in improper format.")
        return
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")
    location_list = JobsDB.select_all_rows("jobs")
    job_list = []
    for item in location_list:
        try:
            item_date = datetime.strptime(item[7], '%a, %d %b %Y %H:%M:%S Z')
            # print("item_date: {}".format(str(item_date)))
        except ValueError:
            item_date = datetime.strptime(item[7], '%a %b %d %H:%M:%S UTC %Y')
            # print("item_date: {}".format(str(item_date)))
        try:
            if stripped_date.date() <= item_date.date():
                job_list.append(item)
        except ValueError:
            print("The date is in the wrong format.")
            # print("Appending the job: {} {} {}".format(item[2], item[3], item[7]))
    JobsMap.cache_coordinates_in_db(conn, job_list)
    date_combined_table = JobsDB.show_select_with_join_lat_lon(conn)
    print("DATE_COMBINED_TABLE:")
    date_df = JobsMap.create_dataframe(date_combined_table)
    JobsDB.close_db(conn)
    return date_df


def filter_by_title(title_string):
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")
    location_list = JobsDB.show_title_from_job_table(conn, title_string)
    JobsMap.cache_coordinates_in_db(conn, location_list)
    title_combined_table = JobsDB.show_select_with_join_lat_lon(conn)
    print("title_COMBINED_TABLE:")
    title_df = JobsMap.create_dataframe(title_combined_table)
    JobsDB.close_db(conn)
    return title_df
