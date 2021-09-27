import json
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from config import BASE_LINK
from parser import AdvertisementPageParser


class CrawlerBase(ABC):

    @abstractmethod
    def start(self, store=False):
        pass

    @abstractmethod
    def store(self, data, filename=None):
        pass

    @staticmethod
    def get(link):
        try:
            response = requests.get(link)
        except requests.HTTPError:
            return None
        return response


class LinkCrawler(CrawlerBase):

    def __init__(self, cities, link=BASE_LINK):
        self.cities = cities
        self.link = link

    @staticmethod
    def get_site_data(html_doc):
        return BeautifulSoup(html_doc, "html.parser")

    def total_num_adv(self, url):
        res = self.get(url + str(0))
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
            res = self.get(url + str(start))
            soup = self.get_site_data(res.text)
            new_links = self.find_links(soup)
            adv_links.extend(new_links)
            start += 120
            crawl = bool(len(new_links))
        adv_links = adv_links[:adv_num]
        return adv_links

    def start(self, store=False):
        adv_links = list()
        for city in self.cities:
            links = self.start_crawl_city(self.link.format(city))
            print(f'Total {city.capitalize()} adv:', len(links))
            adv_links.extend(links)
        if store:
            self.store([li.get('href') for li in adv_links])
        return adv_links

    def store(self, data):
        with open('fixture/data.json', 'w') as f:
            f.write(json.dumps(data))


class DataCrawler(CrawlerBase):
    def __init__(self):
        self.links = self.__load_links()
        self.parser = AdvertisementPageParser()

    @staticmethod
    def __load_links():
        with open('fixture/data.json', 'r') as f:
            links = json.loads(f.read())
        return links

    def start(self, store=False):
        for link in self.links:
            res = self.get(link)
            data = self.parser.parser(res.text)
            if store:
                self.store(data, data.get('post_id', 'sample'))

    def store(self, data, filename):
        with open(f'fixture/adv/{filename}', 'w') as f:
            f.write(json.dumps(data))
        print(f'fixture/adv/{filename}.json')
