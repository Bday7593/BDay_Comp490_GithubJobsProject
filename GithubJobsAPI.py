# Brian Day
# Comp 490 - Development Seminar
import json
import requests


# going through each json page.
def data_retrieval(url):
    raw_datum = requests.get(url)  # requesting the URL and saving it as a data type
    return raw_datum


def store_data(data):
    data_counter = 0
    for item in data.json():  # going through each dictionary item on the json page.
        data_counter = data_counter + 1
        # Append the item from the dictionary onto the jobs_list
        jobs_list.append(item)


def page_is_full(items_on_the_page):
    if items_on_the_page == 50:
        print("PAGE NOT FULL = 0")
        return 1
    else:
        return 0


def github_jobs_search():
    page = 1  # the page the url search is on.
    is_page_full = 1
    while is_page_full == 1:
        url1 = 'https://jobs.github.com/positions.json?page=' + str(page)  # re-assign URL for Github Jobs.txt
        raw_data = data_retrieval(url1)
        print("PAGE = " + str(page))
        store_data(raw_data)
        if len(jobs_list) % 50 != 0:
            break
        else:
            page = page + 1


def write_jobs_to_file(basic_list):
    print("WITHIN write_jobs_to_file()")
    with open('Github Jobs.txt', 'w') as output:
        json.dump(basic_list, output)
        # for item in basic_list:
        # json.dump(item, output)
        # output.write(json.dump(item, output))
        # output.write(json.dumps(basic_list))
        print("WITHIN write_jobs_to_file() TRYING TO WRITE TO FILE")


jobs_list = []  # defining a list to store the items from the json dictionary.
github_jobs_search()
write_jobs_to_file(jobs_list)

counts = 0
for job in jobs_list:
    # print(job['company'])
    counts = counts + 1
print(str(counts))
