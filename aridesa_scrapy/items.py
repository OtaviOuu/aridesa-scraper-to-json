from scrapy import Item, Field


class AridesaAulas(Item):
    title = Field()
    link = Field()
    course = Field()
