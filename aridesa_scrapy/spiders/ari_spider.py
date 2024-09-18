from typing import Iterable
from scrapy import Spider
from scrapy.http import Request, Response
import re

from ..items import AridesaAulas

# TODO: Receber senha por flags
# 23423135:Tc4hz8qe2d@@

# TODO: Carregar cookies direto dos navegadores do sistema
cookies = [
    {
        "name": "_legacy_normandy_session",
        "value": "LlhlZxfm3QYt0YU_nizytw+xZxlTC4g3HxhiW3vbcbuPzTS38gzMBMEt53NeEaZw3TcOhBfIum21cWE5roRCiLFlI0Htf_rlQwInWXufSomF_HXkVY6PJDA7il02I9-zWmP6W3FRPbT8FyyOKjOF4KLrUgSJdp9S1fUsFxq9XNW8Oh4jRMvBXPE1uiuTSwFjNYZqE1rGh8vYX84eyr4atMzntRMIMQQk4Aviep5nzPnyvAuNDVR6z7eb5oB3UjiSw0JPl-zA2HuMgoTLYsbEUrZpRmrn_PsUlh4EWSvZvLyw6uUNbJVxSpwwtoxBJhuSXZPBya6njSq_2KphjVl8Wi0ZeKKlhKT1nuQgMX9caJAwHD36d7cZZayqpDT3TmEoYO4WjUYiG-IGo16sdxnk5nR.iPu21to-oGMixRUE3747gZYaO-w.Zuo8Uw",
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
        "value": "e14c6555488521ebe79cdb5d5164d047",
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
        "name": "pseudonym_credentials",
        "value": "104579%3A%3A799cb5d985e68cc95beee240239ade5b205f2c148af58660222d46fe4377820bb48a62169772a556d4927109d3f37ae5ce1012757bf738aa50fb3c561f4242ed%3A%3A47faeaf8b03511478e14a1d44a8d6b907141c977665c628bb838276dfc6ecdb3",
        "domain": "aridesa.instructure.com",
        "hostOnly": True,
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "no_restriction",
        "session": False,
        "firstPartyDomain": "",
        "partitionKey": None,
        "expirationDate": 1727829545,
        "storeId": None,
    },
    {
        "name": "_csrf_token",
        "value": "uHNqjRTrK3VHqmhDn98kCZmmcyuOLiixQf5joS1chV3zSwjXe6pGDCLgABDbnnBE69IaGM9BbIkbuAzCYhTxJw%3D%3D",
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
        "value": "LlhlZxfm3QYt0YU_nizytw+xZxlTC4g3HxhiW3vbcbuPzTS38gzMBMEt53NeEaZw3TcOhBfIum21cWE5roRCiLFlI0Htf_rlQwInWXufSomF_HXkVY6PJDA7il02I9-zWmP6W3FRPbT8FyyOKjOF4KLrUgSJdp9S1fUsFxq9XNW8Oh4jRMvBXPE1uiuTSwFjNYZqE1rGh8vYX84eyr4atMzntRMIMQQk4Aviep5nzPnyvAuNDVR6z7eb5oB3UjiSw0JPl-zA2HuMgoTLYsbEUrZpRmrn_PsUlh4EWSvZvLyw6uUNbJVxSpwwtoxBJhuSXZPBya6njSq_2KphjVl8Wi0ZeKKlhKT1nuQgMX9caJAwHD36d7cZZayqpDT3TmEoYO4WjUYiG-IGo16sdxnk5nR.iPu21to-oGMixRUE3747gZYaO-w.Zuo8Uw",
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


class aridesaSpider(Spider):
    item = AridesaAulas()

    name = "aridesa"
    base_url = "https://aridesa.instructure.com"

    def start_requests(self) -> Iterable[Request]:
        yield Request(
            url="https://aridesa.instructure.com/courses",
            cookies=cookies,
            callback=self.courses_2024_parse,
        )

    def courses_2024_parse(self, response: Response):

        courses_hrefs = [
            f"{self.base_url}{href}"
            for href in response.css("td a::attr(href)").getall()
        ]

        print(courses_hrefs)
        yield from response.follow_all(
            urls=courses_hrefs, callback=self.subjects_2024, cookies=cookies
        )

    def subjects_2024(self, response: Response):
        classes_hrefs = response.css(
            ".module-item-title .ig-title.title.item_link::attr(href)"
        ).getall()

        yield from response.follow_all(
            urls=classes_hrefs, callback=self.videos_2024, cookies=cookies
        )

    def videos_2024(self, response: Response):
        embed_video_pattern = r"https://www\.youtube\.com/embed/([a-zA-Z0-9_-]+)"
        match = re.search(embed_video_pattern, response.text)

        self.item["title"] = response.css("title::text").get()
        self.item["course"] = response.css("a[href*='/courses/'] span::text").get()

        if match:
            yt_video_link = match.group(0)
            self.item["link"] = yt_video_link

        yield self.item
