import requests
from bs4 import BeautifulSoup


def get_page(url, start=0):
    try:
        response = requests.get(url.format(str(start)))
    except:
        return None
    print(response.status_code, response.url)
    return response


def get_site_data(html_doc):
    return BeautifulSoup(html_doc)


def total_num_adv(link):
    res = get_page(link, 0)
    soup = get_site_data(res.text)
    return int(soup.find('span', attrs={'class': 'totalcount'}).get_text())


def find_links(soup):
    return soup.find_all('a', attrs={'class': 'hdrlnk'})


def start_crawl(link):
    start = 0
    crawl = True
    adv_links = list()
    adv_num = total_num_adv(link)
    while crawl:
        res = get_page(link, start)
        soup = get_site_data(res.text)
        new_links = find_links(soup)
        adv_links.extend(new_links)
        start += 120
        crawl = bool(len(new_links))
    adv_links = adv_links[:adv_num-1]
    return adv_links


if __name__ == "__main__":
    link = "https://paris.craigslist.org/d/housing/search/hhh?lang=en&cc=gb&s={}"
    links = start_crawl(link)
    print('total:',  len(links))
