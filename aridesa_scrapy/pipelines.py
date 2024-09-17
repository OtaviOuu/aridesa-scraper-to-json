# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from collections import defaultdict


class AridesaScrapyPipeline:
    def open_spider(self, spider):
        self.courses = defaultdict(dict)

    def process_item(self, item, spider):
        # Adapta o item para JSON
        course_title = item.get("course")
        title = item.get("title")
        link = item.get("link")

        if course_title and title and link:
            self.courses[course_title][title] = link

        return item

    # TODO: Retornar os nomes das aulas em ordem alfabetica
    def close_spider(self, spider):
        with open("items.json", "w", encoding="utf-8") as file:
            json.dump(self.courses, file, indent=4, ensure_ascii=False, sort_keys=True)
