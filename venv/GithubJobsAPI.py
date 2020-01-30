import json
from urllib.request import urlopen

from pip._vendor import requests


def main():
    url = 'https://jobs.github.com/positions.json?description=python&full_time=true&location=sf'

    raw_data = requests.get(url)
    raw_data.json()
    #json_obj = urlopen(url)

    #data = json.load(json_obj)

    print(raw_data.json())


if __name__ == '__main__':
    main()
