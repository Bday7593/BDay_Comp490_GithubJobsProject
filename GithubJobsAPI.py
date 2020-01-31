# Brian Day
# Comp 490 - Development Seminar

import json
import requests
from urllib.request import urlopen

#from pip._vendor import requests


page = 1    #the page the url search is on.
jobs_list = []        #defining a list to store the items from the json dictionary.
url1 = 'https://jobs.github.com/positions.json?page=' + str(page)   #the URL for Github Jobs


raw_data = requests.get(url1)   #requesting the URL and saving it as a data type
raw_data.json()     #changing the URL data type to the json data.

count = 0   #this is the count of items on in the dictionary
items_on_page = 50  #this is how many items should be in each dictionary. decrement by 1.
full_page = 1

#going through each json page.
while(full_page == 1):
    #going through each dictionary item on the json page.
    for item in raw_data.json():
        #print(item['company'])
       # print(item['title'])
       # print()
        count = count + 1
        print("THE COUNT IS: " + str(count))
        items_on_page = items_on_page - 1

        #Append the item from the dictionary onto the jobs_list
        jobs_list.append(item)
    #print("ITEMS_ON_PAGE = " + str(items_on_page))
    if(items_on_page == 0):
        items_on_page = 50;
        page = page + 1
        url1 = 'https://jobs.github.com/positions.json?page=' + str(page)  # the URL for Github Jobs
        #print("PAGE = " + str(page))
        #print("URL = " + url1)
        #reaccess the url with the new page.
        raw_data = requests.get(url1)  # requesting the URL and saving it as a data type
        raw_data.json()  # changing the URL data type to the json data.
    else:
        full_page = 0
        print("FULL_PAGE = 0")

counter = 0
for job in jobs_list:
    print(job['company'])
    counter = counter + 1
print(str(counter))
#if __name__ == '__main__':
    # main()
