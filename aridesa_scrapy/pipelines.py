import json
from collections import defaultdict


class AridesaScrapyPipeline:
    courses = defaultdict(dict)

    def process_item(self, item, spider):
        # Adapta o item para JSON
        course_title = item.get("course")
        title = item.get("title")
        link = item.get("link")

        if course_title and title and link:
            self.courses[course_title][title] = link
            with open("items.json", "w", encoding="utf-8") as file:
                json.dump(
                    self.courses, file, indent=4, ensure_ascii=False, sort_keys=True
                )

        return item
