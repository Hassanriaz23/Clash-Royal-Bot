# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WinrateItem(scrapy.Item):
    # define the fields for your item here like:
    victory = scrapy.Field()
    defeat = scrapy.Field()
    total_players_no = scrapy.Field()

