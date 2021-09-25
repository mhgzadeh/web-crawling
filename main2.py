import sys
from crawl import LinkCrawler, DataCrawler

if __name__ == "__main__":
    switch = sys.argv[1]
    if switch == "find_links":
        link_crawler = LinkCrawler(cities=['paris', 'berlin', 'amsterdam', 'munich'])
        link_crawler.start()
    elif switch == "extract_pages":
        data_crawler = DataCrawler()
        data_crawler.start()
