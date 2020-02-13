# Brian Day
# Comp 490 - Development Seminar
import feedparser

# from email import feedparser


def store_data(data, my_list):
    for item in data:  # going through each dictionary item on the json page.
        print("The feed link in stack_overflow_jobs_list = " + item['feed']['title'])
        my_list.append(item)


def stack_overflow_jobs_search(my_list):
    # Create the feed.Put in the RSS feed that you want.
    stack_overflow_jobs_data = feedparser.parse('https://stackoverflow.com/jobs/feed')
    print(stack_overflow_jobs_data['feed']['title'])
    print(stack_overflow_jobs_data.feed.subtitle)
    print("The Stack Overflow URL is: " + stack_overflow_jobs_data['feed']['link'])
    print(len(stack_overflow_jobs_data['entries']))
    # print(stack_overflow_jobs_data.entries[0]['link'])
    for post in stack_overflow_jobs_data.entries:
        print(post.title + ": " + post.description + " " + post.guid + " " + post.link + " ")
    # store_data(stack_overflow_jobs_data, my_list)


def main():
    stack_overflow_jobs_list = []
    stack_overflow_jobs_search(stack_overflow_jobs_list)
    # print("The amount of entries in stack_overflow_jobs_list = " + str(stack_overflow_jobs_list['feed'][0]['link']))


if __name__ == '__main__':
    main()
