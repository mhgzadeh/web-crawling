import json

import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup

from config import BASE_LINK


class CrawlerBase(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass


class LinkCrawler(CrawlerBase):

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link

    def get_page(self, url, start=0):
        try:
            response = requests.get(url + str(start))
        except:
            return None
        return response

    @staticmethod
    def get_site_data(html_doc):
        return BeautifulSoup(html_doc, "html.parser")

    def total_num_adv(self, url):
        res = self.get_page(url, 0)
        soup = self.get_site_data(res.text)
        return int(soup.find('span', attrs={'class': 'totalcount'}).get_text())

    @staticmethod
    def find_links(soup):
        return soup.find_all('a', attrs={'class': 'hdrlnk'})

    def start_crawl_city(self, url):
        start = 0
        crawl = True
        adv_links = list()
        adv_num = self.total_num_adv(url)
        while crawl:
            res = self.get_page(url, start)
            soup = self.get_site_data(res.text)
            new_links = self.find_links(soup)
            adv_links.extend(new_links)
            start += 120
            crawl = bool(len(new_links))
        adv_links = adv_links[:adv_num]
        return adv_links

    def start(self):
        adv_links = list()
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            print(f'Total {city.capitalize()} adv:', len(links))
            adv_links.extend(links)
        self.store([li.get('href') for li in adv_links])

    def store(self, data):
        with open('fixture/data.json', 'w') as f:
            f.write(json.dumps(data))


class DataCrawler(CrawlerBase):
    def start(self):
        print('Not Implemented Function')

    def store(self, data):
        print('Not create store function.')
