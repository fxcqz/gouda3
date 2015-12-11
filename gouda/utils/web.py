import requests
from bs4 import BeautifulSoup


def get_page_contents(url):
    request = requests.get(url)
    return request.text
