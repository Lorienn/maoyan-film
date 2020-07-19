# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 09:48:06 2020

@author: 小花
"""

from spiderEdited import MultiThreadedSpider
import pandas as pd
import re


class maoyanSpider(MultiThreadedSpider):
#    start_urls = ["https://maoyan.com/films?showType=3"]
    start_urls = ["https://maoyan.com/films?showType=3&sortId=3"]

    def on_start(self):
        self.data = []

    def process(self, response):
        page_num = response.doc("#app > div > div.movies-panel > div.movies-pager > ul > li.active > a").text()
        for a in response.doc("div.channel-detail.movie-item-title > a").items():
            self.crawl({
                "url": a.attr("href"),
                "page_num": page_num
            }, self.process_detail)
        for a in response.doc("div.movies-pager > ul > li.active + li > a").items():
            link = "https://maoyan.com/films?" + re.split(r"\?", a.attr("href"))[1]
            self.crawl({"url": link})

    def process_detail(self, response):
        title = ""
        etitle = ""
        rating = ""
        rating_people = ""
        box_office = ""
        times = ""
        year = ""
        area = ""
        location = ""
        length = ""
        synopsis = ""
        director = ""
        actors = ""
        m_type = ""
        company = ""

        title = response.doc("h1").text()
        etitle = response.doc(".ename").text()
        rating = response.doc("div.movie-stats-container > div:nth-child(1) > div > span > span").text()

        rating_people = response.doc("div.movie-stats-container > div:nth-child(1) > div > div > span > span").text()
        box_office = response.doc(
            "div.movie-stats-container > div:nth-child(2) > div > span.stonefont").text() + response.doc(
            "div.movie-stats-container > div:nth-child(2) > div > span.unit").text()

        times = response.doc(
            "div.tab-desc.tab-content.active > div:nth-child(7) > div.mod-content > div > div:nth-child(1) > div:nth-child(1)").text()
        if times:
            times = re.findall(r"\d+", times)[0]

        y = response.doc("div.movie-brief-container > ul > li:nth-child(3)").text()
        if y:
            year = re.findall(r"\d+", y)[0]

        a = response.doc("div.movie-brief-container > ul > li:nth-child(3)").text()
        A = re.findall(r"[^\d\-^]", y)
        area = ""
        for a in A[:len(A) - 2]:
            area += a

        loca_length = response.doc("div.movie-brief-container > ul > li:nth-child(2)").text()
        location = re.split(r"/", loca_length)[0]
        if len(re.split(r"/", loca_length)) == 2:
            l = re.split(r"/", loca_length)[1]
            length = re.findall(r"\d+", l)[0]
        else:
            length = None

        synopsis = response.doc("div.tab-desc.tab-content.active > div:nth-child(1) > div.mod-content > span").text()
        director = response.doc("div.mod-content > div > div:nth-child(1) > ul > li > div > a").text()

        for a in response.doc("div.movie-brief-container > ul > li:nth-child(1)>a").items():
            m_type = m_type + a.text() + " "
        for a in response.doc("div.mod-content > div > div:nth-child(2) > ul a.name").items():
            actors = actors + a.text() + " "

        producer = response.doc(
            "#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(6) > div.mod-content > div > div:nth-child(2) > div.attribute-item-top > span").text()
        if producer == "出品发行":
            company = response.doc(
                "#app > div > div.main-content > div > div.tab-content-container > div.tab-desc.tab-content.active > div:nth-child(6) > div.mod-content > div > div:nth-child(2) > div.attribute-item-content.ellipsis").text()

        self.data.append({
            "名字": title,
            "外语名字": etitle,
            "评分": rating,
            "评分人数": rating_people,
            "票房": box_office,
            "获奖次数": times,
            "上映年份": year,
            "上映地区": area,
            "类型": m_type,
            "制片国家、地区": location,
            "片长": length,
            "出品公司": company,
            "导演": director,
            "演员": actors,
            "页码": response.data["page_num"],
            "剧情": synopsis,
        })

    def on_end(self):
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("maoyanMovies.xlsx")
        print(self.data)


if __name__ == '__main__':
    maoyanSpider().start()
