# BDay_Comp490_GithubJobsProject
Brian Day
Comp 490
Project 1: Github Jobs API


The readme should have:
SPRINT 1:
    a.) Any install and run directions I need beyond the basics.
        -only basic installation should be required to run.
    b.) A brief description of what your project does.
        - This project pulls the API data from the website: https://jobs.github.com/positions.json?page=1
            and stores the .json dictionaries from the website into a list. The list is tested to see
            that it has stores the proper amount of dictionaries and the list is also written onto a text
            document. The text document is opened and read to be tested against an existing company name
            ensuring the correct data was written into the text document.  
    c.) A brief description of what is missing from the project (if anything)
        - No missing material.
        
SPRINT 2, 3:
    a.) update the install and running instructions in the readme.
        - If there are no files in the database the program MUST be run before being
            pushed to git. The database needs to populate with the jobs from github API
            to be test properly. 
            
SPRINT 4:
    I could not get a GUI to work so there is not one. I wanted a project that would actually map locations
    instead of a project with a broken GUI. As for mapping the jobs out; all the necessary functions are
    in the class JobsMap.py in the main(). All that needs to be done is to comment and uncomment out the 
    functions marked with %% to test them.  
def main():
    conn, cursor = JobsDB.open_db("JobsDB.sqlite")
    Filters.reset_job_locations()
    JobsDB.setup_db(cursor)
%%   df = Filters.no_filter()
%%   # df = Filters.filter_by_technology("swift")
%%   # df = Filters.filter_by_company("Apple")
%%   # df = Filters.filter_by_age_of_post("25/02/2020")
%%   # df = Filters.filter_by_title("Senior") 
    map_jobs(df)
    JobsDB.close_db(conn)
The functions will cache the locations coordinates in a table and then use that table to create the map.
        
     
    
        
        
    