# Brian Day
# Comp 490 - Development Seminar
import feedparser


def store_data(data, my_list):
    for item in data:  # going through each dictionary item on the json page.
        print("The feed link in stack_overflow_jobs_list = " + item['feed']['title'])
        my_list.append(item)


def stack_overflow_jobs_search():
    # Create the feed.Put in the RSS feed that you want.
    stack_overflow_jobs_data = feedparser.parse('https://stackoverflow.com/jobs/feed')
    # print(stack_overflow_jobs_data['feed']['title'])
    # print(stack_overflow_jobs_data.feed.subtitle)
    # print("The Stack Overflow URL is: " + stack_overflow_jobs_data['feed']['link'])
    # print("Stack Overflow jobs available: ")
    # print(len(stack_overflow_jobs_data['entries']))
    # print(stack_overflow_jobs_data.entries[0]['link'])
    print()
    # for post in stack_overflow_jobs_data.entries:
    # print("post.author:     " + post.author)
    # print("post.category:     " + post.category)
    # print("post.title:      " + post.title)
    # print("post.guid:       " + post.guid)
    # print("post.description: " + post.description)
    # print("post.link:       " + post.link)
    # print("post.published:       " + post.published)
    # for entry in post:
    # print(post.created)
    # print()
    return stack_overflow_jobs_data.entries


def main():
    stack_overflow_jobs_search()


if __name__ == '__main__':
    main()
