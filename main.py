import requests
from bs4 import BeautifulSoup
# import sys


# def get_page(url, start=0):
#     try:
#         response = requests.get(url + str(start))
#     except:
#         return None
#     # print(response.status_code, response.url)
#     return response
#
#
# def get_site_data(html_doc):
#     return BeautifulSoup(html_doc, "html.parser")
#
#
# def total_num_adv(link):
#     res = get_page(link, 0)
#     soup = get_site_data(res.text)
#     return int(soup.find('span', attrs={'class': 'totalcount'}).get_text())
#
#
# def find_links(soup):
#     return soup.find_all('a', attrs={'class': 'hdrlnk'})
#
#
# def start_crawl_city(link):
#     start = 0
#     crawl = True
#     adv_links = list()
#     adv_num = total_num_adv(link)
#     while crawl:
#         res = get_page(link, start)
#         soup = get_site_data(res.text)
#         new_links = find_links(soup)
#         adv_links.extend(new_links)
#         start += 120
#         crawl = bool(len(new_links))
#     adv_links = adv_links[:adv_num]
#     return adv_links


# def start_crawl():
#     cities = ['paris', 'berlin', 'amsterdam', 'munich']
#     link = "https://{}.craigslist.org/d/housing/search/hhh?lang=en&cc=gb&s="
#     for city in cities:
#         links = start_crawl_city(link.format(city))
#         print(f'Total {city.capitalize()} adv:', len(links))


# def get_pages_data():
#     print('Not Implemented Function')
#
#
# if __name__ == "__main__":
#     switch = sys.argv[1]
#     if switch == "find_links":
#         start_crawl()
#     elif switch == "extract_pages":
#         get_pages_data()
