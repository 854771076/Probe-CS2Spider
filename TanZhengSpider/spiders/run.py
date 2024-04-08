# -*- coding: utf-8 -*-

from scrapy import cmdline


if __name__ == '__main__':
    cmdline.execute(("scrapy crawl steam_csgo").split())
    # cmdline.execute(("scrapy crawl uuyp_csgo").split())
    # cmdline.execute(("scrapy crawl c5_csgo").split())
    # cmdline.execute(("scrapy crawl igxe_csgo").split())
    # cmdline.execute(("scrapy crawl buff_csgo").split())
    # cmdline.execute(("scrapy crawl archive_csgo").split())