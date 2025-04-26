# NOT DEFAULT
# Define your spiders here
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spiders.html

import re

from scrapy import spiders, http, signals
from tqdm import tqdm


# NOTE: Substance matching is to complex and will not be used
class ATC_Spider(spiders.Spider):
    '''
    This ATC Spider extracts atc data from the WHO.
    '''

    # Overriden Spider Settings
    # name is used to start a spider with the scrapy crawl command
    name = 'atc'
    # custom_settings contains own settings, but can also override the values in settings.py
    custom_settings = {
        'PROGRESS_LOGGING': False,
        'DEPTH_LIMIT': 4  # NOTE: Can be used to only extract atc codes up to a certain length
    }
    # These are the allowed domains. This spider should only follow urls in these domains
    allowed_domains = ['www.whocc.no']

    # URLS and headers
    base_url = 'https://www.whocc.no/atc_ddd_index/'
    query_url = 'https://www.whocc.no/atc_ddd_index/?code={}&showdescription=no'
    # This regex will extract the atc_code from the url
    atc_regex = re.compile(r'code=(\S+)&')

    def __init__(self, progress_logging=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_settings.update({
            'PROGRESS_LOGGING': progress_logging
        })
        if self.custom_settings.get('PROGRESS_LOGGING'):
            self.pbar = tqdm(
                total=float('inf'),
                leave=False,
                desc='Scraping Progress',
                unit='ATC codes',
                colour='green',
            )

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.idle, signals.spider_idle)

        if "level" in kwargs and kwargs["level"].isdigit():
            # Clamp between 1 and 4
            level = min(max(int(kwargs["level"]), 1), 4)
            spider.settings.update(
                {
                    'DEPTH_LIMIT': level
                },
                priority="spider"
            )

        return spider

    def start_requests(self):
        '''
        Starts the Spider with a single request to the ATC Index home page.
        The first site has a different structure and will be parsed different from the rest.
        '''
        return [http.Request(self.base_url, cb_kwargs={'base_url_page': True})]

    def parse(self, response: http.Response, base_url_page=False):
        '''
        Parses all responses and extracts atc_code and atc_value from the <a> Element.
        It will follow the links to the deepest level allowed by the DEPTH_LIMIT.
        '''
        if self.custom_settings.get('PROGRESS_LOGGING') and isinstance(self.pbar, tqdm):
            self.pbar.update()

        main = response.xpath('//*[@id="content"]')
        if base_url_page:
            main = main.xpath('./div/div')

        # This list is empty in the last level
        atc_links = main.xpath('./p/b//a')
        follow_links = bool(atc_links)
        if not atc_links:
            atc_links = main.xpath('.//table//a')

        atc_codes = [
            self.atc_regex.search(link).group(1) for link in atc_links.xpath('./@href').getall()
        ]

        atc_values = [
            ''.join(link.xpath('.//text()').getall()) for link in atc_links
        ]

        # This assertion will probably fail if the code breaks (i.e. after website changes)
        # NOTE: It's possible to check for a regex match in the atc_codes with:
        #       r"^[A-DGHJLMNPRSV](?:[0-2]\d(?:[A-NRXZ](?:[A-NPRSTVXYZ](?:[0-8]\d)?)?)?)?$"" or less strict
        #       r"^[A-DGHJLMNPRSV](?:\d{2}(?:[A-NRXZ](?:[A-NPRSTVXYZ](?:\d{2})?)?)?)?$" or less strict
        #       r"^[A-Z](?:\d{2}(?:[A-Z](?:[A-Z](?:\d{2})?)?)?)?$"
        assert len(atc_codes) == len(atc_values)

        for atc, value in zip(atc_codes, atc_values):
            yield {
                'atc_code': atc,
                'atc_value': value
            }

        if follow_links:
            next_requests = [
                http.Request(f'{self.base_url}{links[2:]}', dont_filter=True) for links in atc_links.xpath('./@href').getall()
            ]
            for request in next_requests:
                yield request

    def idle(self):
        if self.custom_settings.get('PROGRESS_LOGGING') and isinstance(self.pbar, tqdm):
            self.pbar.close()

    def closed(self, reason: str):
        if reason == 'finished':
            self.logger.info('Scraping finished successfully.')
        elif reason == 'shutdown':
            self.logger.info('Scraping was stopped by user.')
        else:
            self.logger.info(f'Scraping finished with reason: {reason}')
