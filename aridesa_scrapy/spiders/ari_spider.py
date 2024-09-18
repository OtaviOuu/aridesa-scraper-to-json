from typing import Any, Iterable
from scrapy import Spider
from scrapy.http import Request, Response, JsonRequest, FormRequest
import re

import scrapy.logformatter
from ..items import AridesaAulas
from collections import defaultdict

# TODO: Receber senha por flags
# 23423135:Tc4hz8qe2d@@

# TODO: Carregar cookies direto dos navegadores do sistema
cookies = [
    {
        "name": "_legacy_normandy_session",
        "value": "QFjO6vnxIQbcrd9AAwp6RA+N2kVgIcFAztFWbTqBP3PGOuDM3zdsVGBY-f_s9SztNjGbnf8rOIhY--XP8GVr4MwQ8vZg-09XWl77uK8YDjELh-DkampLgOG3wtzBsdPx6g-oEqeBCSyyPZja9LSwGktVIXqndYL0gxJHgTljKZxcv0wvPKy176FIr1HHAufKWz8N_tuGEiS2WVmIjyFlZe098hWNCzvH7cHPnNfRdYeuuyRTDscr2_5KioIKX8MMguVSCjdKk9UiCRabne50wB2OVLIdW28UDI_v5QLMPwQt1QOVnJ5hgX7gIezMXXHByP9fgJHVIW4IfGIl_vLqf-zFW57k3xWqykkhcz2Vdkf-mWN8lS1aWH7XJ11vKyCT6YvogFwkwSYgFliOR3FKdfTB3mUX43HWObF3qe3ZE4i_A.9U2NxHdho3CwA1D1HNzvvHGi0I4.ZujdCA",
        "domain": "aridesa.instructure.com",
        "hostOnly": True,
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "no_restriction",
        "session": True,
        "firstPartyDomain": "",
        "partitionKey": None,
        "storeId": None,
    },
    {
        "name": "log_session_id",
        "value": "82ca7f4344e42735bcf5e5b62f706f0f",
        "domain": "aridesa.instructure.com",
        "hostOnly": True,
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "no_restriction",
        "session": True,
        "firstPartyDomain": "",
        "partitionKey": None,
        "storeId": None,
    },
    {
        "name": "_ga",
        "value": "GA1.2.721992705.1725994374",
        "domain": ".instructure.com",
        "hostOnly": False,
        "path": "/",
        "secure": False,
        "httpOnly": False,
        "sameSite": "no_restriction",
        "session": False,
        "firstPartyDomain": "",
        "partitionKey": None,
        "expirationDate": 1789066515,
        "storeId": None,
    },
    {
        "name": "_csrf_token",
        "value": "AoSLAnzqHT2axu3cLWFH113GhkjsqTs%2BlcHCz7cMzt5F9eBnU5hqTtfyqKhHLBG0EO3ze9zLdE3H6rOs9nut7A%3D%3D",
        "domain": "aridesa.instructure.com",
        "hostOnly": True,
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "no_restriction",
        "session": True,
        "firstPartyDomain": "",
        "partitionKey": None,
        "storeId": None,
    },
    {
        "name": "_hp2_id.3001039959",
        "value": "%7B%22userId%22%3A%225686342285698394%22%2C%22pageviewId%22%3A%226128167986342756%22%2C%22sessionId%22%3A%221691066822117514%22%2C%22identity%22%3A%22uu-2-2e0c34053ed290703e04245be12c30b73154333ab2ebd1a9f0e85744a98031ea-inYDFpFeroMfE7Mp7PcAJPcTWBjrkgDBHe6XKVlw%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3ANone%2C%22isIdentified%22%3A1%7D",
        "domain": ".instructure.com",
        "hostOnly": False,
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "no_restriction",
        "session": False,
        "firstPartyDomain": "",
        "partitionKey": None,
        "expirationDate": 1760072115,
        "storeId": None,
    },
    {
        "name": "_hp2_props.3001039959",
        "value": "%7B%22Base.appName%22%3A%22Canvas%22%7D",
        "domain": ".instructure.com",
        "hostOnly": False,
        "path": "/",
        "secure": True,
        "httpOnly": False,
        "sameSite": "no_restriction",
        "session": False,
        "firstPartyDomain": "",
        "partitionKey": None,
        "expirationDate": 1760072115,
        "storeId": None,
    },
    {
        "name": "canvas_session",
        "value": "QFjO6vnxIQbcrd9AAwp6RA+N2kVgIcFAztFWbTqBP3PGOuDM3zdsVGBY-f_s9SztNjGbnf8rOIhY--XP8GVr4MwQ8vZg-09XWl77uK8YDjELh-DkampLgOG3wtzBsdPx6g-oEqeBCSyyPZja9LSwGktVIXqndYL0gxJHgTljKZxcv0wvPKy176FIr1HHAufKWz8N_tuGEiS2WVmIjyFlZe098hWNCzvH7cHPnNfRdYeuuyRTDscr2_5KioIKX8MMguVSCjdKk9UiCRabne50wB2OVLIdW28UDI_v5QLMPwQt1QOVnJ5hgX7gIezMXXHByP9fgJHVIW4IfGIl_vLqf-zFW57k3xWqykkhcz2Vdkf-mWN8lS1aWH7XJ11vKyCT6YvogFwkwSYgFliOR3FKdfTB3mUX43HWObF3qe3ZE4i_A.9U2NxHdho3CwA1D1HNzvvHGi0I4.ZujdCA",
        "domain": "aridesa.instructure.com",
        "hostOnly": True,
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "no_restriction",
        "session": True,
        "firstPartyDomain": "",
        "partitionKey": None,
        "storeId": None,
    },
]

final_data = {}


class aridesaSpider(Spider):
    item = AridesaAulas()

    name = "aridesa"
    base_url = "https://aridesa.instructure.com"
    base_api = f"{base_url}/api/v1/dashboard/dashboard_cards"

    api_courses_2023 = "https://aridesa.instructure.com/api/v1/courses/"

    def start_requests(self) -> Iterable[Request]:

        yield Request(
            url=self.base_api,
            cookies=cookies,
            callback=self.courses_parse,
        )

    def courses_parse(self, response: Response) -> Any:
        for course_card in response.json():

            yield response.follow(
                course_card["pagesUrl"],
                callback=self.classes_parse,
            )

    def classes_parse(self, response: Response):

        classes_hrefs = response.css(
            ".module-item-title .ig-title.title.item_link::attr(href)"
        ).getall()

        for href in classes_hrefs:

            yield response.follow(
                url=f"{self.base_url}{href}",
                callback=self.video_parse,
            )

    def video_parse(self, response: Response):

        self.item["title"] = response.css("title::text").get()
        self.item["course"] = response.css("a[href*='/courses/'] span::text").get()

        embed_video_pattern = r"https://www\.youtube\.com/embed/([a-zA-Z0-9_-]+)"
        match = re.search(embed_video_pattern, response.text)

        if match:
            yt_video_link = match.group(0)
            self.item["link"] = yt_video_link

            yield self.item
