from winrate.spiders.trial import WinSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    # with open("clan_tag.txt", "r") as f:
    #     clan_tag = f.read().strip().replace('#','')
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(WinSpider)
    # process.crawl(WinSpider, input='inputargument', clan_tag=clan_tag)
    process.start()
