from typing import Any, Iterable
from scrapy import Spider
from scrapy.http import Request, Response, JsonRequest, FormRequest
import browser_cookie3
import re
import os
from pathlib import Path

# 23423135:Tc4hz8qe2d@@

cj = browser_cookie3.firefox(domain_name="aridesa.instructure.com")
cookis = {c.name: c.value for c in cj}

cookies = [
    {
        "name": "_legacy_normandy_session",
        "value": "CzgzwUs-vo9h88KgWqjzRA+ZJ2H72Tk3kC6XxlnYvg8OVyJK7DMVCX4btXdXXH7zcRtFZucTAUaCrAcuSBsuS6IeiGZvTK2DGhc1qWFMkp4nfeNjJ1jvOEnZVMKiW3VmlZDNL_I280sYZi3brFeoz3T8IL8WwPjnU8okfrKyKqbRljVXi-pDzZNKNoeXCsQtvXtCo5Oqg4_7u9chfnGyh_W9ZKdmeNp0bHv92IILNc2DgMNDuU4x--LxUUlzmo3cMIK9BlJrw9Opiice7sdlLWLbQUB-Ays83hpEYLl9500ZerFCB1cc1677IMBmaFCI44yzOEVCYtd5SYoFM7lcux7q7UepRoQLnOYahSUrUYlsjOGs179MUKKIXZI4LNxI-7-cfQe61yiT9HHWtka1gdol6sXv_aXXuD5MXdmiICqsA.T0U42FEKmJwnlOii5YPIDi7KZOs.ZueJfA",
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
        "value": "4a95e7664a9141321e055771032f5856",
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
        "value": "104432%3A%3A799cb5d985e68cc95beee240239ade5b205f2c148af58660222d46fe4377820bb48a62169772a556d4927109d3f37ae5ce1012757bf738aa50fb3c561f4242ed%3A%3A182a5fcf83e42a3b61cf8491eccc92faf46b5016785d90a135b1b25ce1e63031",
        "domain": "aridesa.instructure.com",
        "hostOnly": True,
        "path": "/",
        "secure": True,
        "httpOnly": True,
        "sameSite": "no_restriction",
        "session": False,
        "firstPartyDomain": "",
        "partitionKey": None,
        "expirationDate": 1727659608,
        "storeId": None,
    },
    {
        "name": "_csrf_token",
        "value": "YjbXz%2BoHt%2Bg3gUbv1Wg7hv0csuaA8O7ozqEYaIQqHiJSbrOkjVbP0HzkKpexG1H2hW%2F2qMm0t6yv7EsRyWRnSA%3D%3D",
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
        "value": "%7B%22userId%22%3A%225686342285698394%22%2C%22pageviewId%22%3A%226128167986342756%22%2C%22sessionId%22%3A%221691066822117514%22%2C%22identity%22%3A%22uu-2-2e0c34053ed290703e04245be12c30b73154333ab2ebd1a9f0e85744a98031ea-inYDFpFeroMfE7Mp7PcAJPcTWBjrkgDBHe6XKVlw%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%None%2C%22isIdentified%22%3A1%7D",
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
        "value": "CzgzwUs-vo9h88KgWqjzRA+ZJ2H72Tk3kC6XxlnYvg8OVyJK7DMVCX4btXdXXH7zcRtFZucTAUaCrAcuSBsuS6IeiGZvTK2DGhc1qWFMkp4nfeNjJ1jvOEnZVMKiW3VmlZDNL_I280sYZi3brFeoz3T8IL8WwPjnU8okfrKyKqbRljVXi-pDzZNKNoeXCsQtvXtCo5Oqg4_7u9chfnGyh_W9ZKdmeNp0bHv92IILNc2DgMNDuU4x--LxUUlzmo3cMIK9BlJrw9Opiice7sdlLWLbQUB-Ays83hpEYLl9500ZerFCB1cc1677IMBmaFCI44yzOEVCYtd5SYoFM7lcux7q7UepRoQLnOYahSUrUYlsjOGs179MUKKIXZI4LNxI-7-cfQe61yiT9HHWtka1gdol6sXv_aXXuD5MXdmiICqsA.T0U42FEKmJwnlOii5YPIDi7KZOs.ZueJfA",
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
    name = "aridesa"
    base_url = "https://aridesa.instructure.com"
    base_api = f"{base_url}/api/v1/dashboard/dashboard_cards"

    base_path = f"{os.getcwd}/Ari_de_Sa"

    def start_requests(self) -> Iterable[Request]:

        # Cria pasta do Ari de Sá
        self.base_path.mkdir(self.base_path)

        yield Request(
            url=self.base_api,
            cookies=cookies,
            callback=self.courses_parse,
        )

    def courses_parse(self, response: Response) -> Any:
        for course_card in response.json():
            course_context = {
                "course_title": course_card["originalName"],
                "course_href": course_card["pagesUrl"],
                "video_title": None,
            }

            yield response.follow(
                course_card["pagesUrl"],
                callback=self.classes_parse,
                cb_kwargs={"course_context": course_context},
            )

    def classes_parse(self, response: Response, course_context):

        classes_hrefs = response.css(
            ".module-item-title .ig-title.title.item_link::attr(href)"
        ).getall()
        classes_titles = response.css(
            ".module-item-title .ig-title.title.item_link::text"
        ).getall()

        for href, title in zip(classes_hrefs, classes_titles):

            course_context["video_title"] = title.strip()

            yield response.follow(
                url=f"{self.base_url}{href}",
                callback=self.video_parse,
                cb_kwargs={"course_context": course_context},
            )

    def video_parse(self, response: Response, course_context):

        embed_video_pattern = r"https://www\.youtube\.com/embed/([a-zA-Z0-9_-]+)"
        match = re.search(embed_video_pattern, response.text)

        if match:
            course_context["yt_video_link"] = match.group(0)

            yield {course_context["course_title"]: course_context["yt_video_link"]}

        yield {"video_title": "Página sem vídeo"}
