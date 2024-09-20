from typing import Iterable
from scrapy import Spider
from scrapy.http import Request, Response, FormRequest
import re
import sys
import os

from ..items import AridesaAulas


class aridesaSpider(Spider):
    item = AridesaAulas()
    name = "aridesa"
    base_url = "https://aridesa.instructure.com"

    def start_requests(self) -> Iterable[Request]:
        yield Request(
            url=f"{self.base_url}/login/canvas",
            callback=self.login,
        )

    def login(self, response: Response):
        os.system("clear")

        login = input("login: ")
        senha = input("senha: ")

        formToken = response.css(
            'form[action="/login/canvas"] input[name="authenticity_token"]::attr(value)'
        ).get()

        formCssSelector = 'form[action="/login/canvas"]'

        # TODO: Tratar erro de login
        yield FormRequest.from_response(
            response=response,
            formcss=formCssSelector,
            formdata={
                "pseudonym_session[unique_id]": login,
                "pseudonym_session[password]": senha,
                "authenticity_token": formToken,
            },
            callback=self.after_login,
        )

    def after_login(self, response: Response):
        # Logado:
        yield Request(
            url=f"{self.base_url}/courses",
            callback=self.courses_2024_parse,
        )

    def courses_2024_parse(self, response: Response):

        courses_hrefs = [
            f"{self.base_url}{href}"
            for href in response.css("td a::attr(href)").getall()
        ]

        (courses_hrefs)
        yield from response.follow_all(urls=courses_hrefs, callback=self.subjects_2024)

    def subjects_2024(self, response: Response):
        classes_hrefs = response.css(
            ".module-item-title .ig-title.title.item_link::attr(href)"
        ).getall()

        yield from response.follow_all(urls=classes_hrefs, callback=self.videos_2024)

    def videos_2024(self, response: Response):
        embed_video_pattern = r"https://www\.youtube\.com/embed/([a-zA-Z0-9_-]+)"
        match = re.search(embed_video_pattern, response.text)

        self.item["title"] = response.css("title::text").get()
        self.item["course"] = response.css("a[href*='/courses/'] span::text").get()

        if match:
            yt_video_link = match.group(0)
            self.item["link"] = yt_video_link

        yield self.item
