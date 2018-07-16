from urllib.request import urlopen
from link_finder import LinkFinder
from general import create_data_files, create_project_dir, file_to_set, set_to_file
from domain import get_domain_name


class Spider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spider.project_name = project_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = Spider.project_name + '/queue.txt'
        Spider.crawled_file = Spider.project_name + '/crawled.txt'

        self.boot()
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.project_name, Spider.base_url)
        Spider.queue = file_to_set(Spider.queue_file)
        Spider.crawled = file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(threadName, url):
        if url not in Spider.crawled:
            print(threadName + ' crawling ' + url)
            print('Queue:' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(url))
            Spider.queue.remove(url)
            Spider.crawled.add(url)
            Spider.update_files()

    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)

    @staticmethod
    def gather_links(url):
        html_string = ''
        try:
            response = urlopen(url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, url)
            finder.feed(html_string)
        except Exception:
            print('Error: can not crawl page: ' + url)
            return set()

        return finder.page_links()

    @staticmethod
    def update_files():
        set_to_file(Spider.queue, Spider.queue_file)
        set_to_file(Spider.crawled, Spider.crawled_file)