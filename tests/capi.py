# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/5/31
@Software: PyCharm
@disc:
======================================="""
import csv
import os
import time
from urllib.parse import quote

import requests
from elasticsearch import Elasticsearch

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}


def search(query: str):
    _url = f"https://www.tianyancha.com/search?key={query}"
    print(_url)
    _url = quote(_url, safe='/:?=&')
    print(_url)
    reference = f"{_url}&sessionNo={time.time()}"
    resp = requests.get(f"https://www.tianyancha.com/search?key={query}",
                        headers={
                            **headers,
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                            "Cookie": f"HWWAFSESID=e679473c195e8ff1b7; HWWAFSESTIME={time.time()}; csrfToken=23YIhYgTphVGT6pTxUVcEoyE; TYCID=3ab75590061811efb1abffa7b18080a2; CUID=e305def67d6e203d3dcd203096bfb8d2; jsid=SEO-BAIDU-ALL-SY-000001; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22264214686%22%2C%22first_id%22%3A%2218f2986f3dea6d-0a87b0c6e6815e8-1b525637-3686400-18f2986f3df170d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMThmMjk4NmYzZGVhNmQtMGE4N2IwYzZlNjgxNWU4LTFiNTI1NjM3LTM2ODY0MDAtMThmMjk4NmYzZGYxNzBkIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMjY0MjE0Njg2In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%22264214686%22%7D%2C%22%24device_id%22%3A%2218f2986f3dea6d-0a87b0c6e6815e8-1b525637-3686400-18f2986f3df170d%22%7D; tyc-user-info=%7B%22state%22%3A%220%22%2C%22vipManager%22%3A%220%22%2C%22mobile%22%3A%2215899198230%22%2C%22userId%22%3A%22264214686%22%7D; tyc-user-info-save-time={time.time()}; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTg5OTE5ODIzMCIsImlhdCI6MTcxNjUzODkyMCwiZXhwIjoxNzE5MTMwOTIwfQ.Bwi8mferwtkZvzO-pD7TzXCoTgAc4wK8tcA3st0PkvK_pgTr4rI8NF1exSgi3iG4vimV9n7-hCZpA8DrBkoo_A; Hm_lvt_e92c8d65d92d534b0fc290df538b4758={time.time()}; bannerFlag=true; searchSessionId={time.time()}; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758={time.time()}",
                            "Reference": reference

                        })
    print(resp.status_code)
    if resp.status_code == 200:
        with open(f"./data/tianyancha-search-{query}.html", 'wb') as f:
            f.write(resp.content)


class CAPI:
    def __init__(self, aut_token):
        self.aut_token = aut_token
        self.headers = {
            **headers,
            "Content-Type": "application/json",
            "X-Auth-Token": self.aut_token,
            "X-Tycid": "3ab75590061811efb1abffa7b18080a2",
            "Referer": "https://www.tianyancha.com/",
            "Origin": "https://www.tianyancha.com",
            "Accept": "*/*",
            "Accept-Encoding": "gzip"
        }
        self.base_url = "https://capi.tianyancha.com"

    def __do__(self, url, method: str = "POST", params=None, data=None):
        if params is None:
            params = {}
        params["_"] = time.time()
        queries = []
        for key, value in params.items():
            queries.append(f"{key}={value}")
        _query = "&".join(queries)
        _url = f"{self.base_url}/{url}?{_query}"
        print(_url)
        if method == "GET":
            resp = requests.get(_url, headers={
                **self.headers,
            })
        else:
            resp = requests.post(
                _url,
                json=data, headers={
                    **self.headers,
                })

        if resp.status_code == 200:
            respJson = resp.json()
            if respJson["state"] == "ok":
                return respJson
            else:
                print(respJson)
                return respJson
        else:
            print(resp.status_code, resp.text)

    def __POST__(self, url, params=None, data=None):
        return self.__do__(url, method="POST", params=params, data=data)

    def __GET__(self, url, params=None):
        return self.__do__(url, method="GET", params=params)

    def get_shareholder_v2(self, _id: int, vShow: bool = False):
        resp = self.__POST__(f"cloud-company-background/companyV2/dim/holderV2", data={
            "gid": str(_id),
            "pageSize": 10, "pageNum": 1,
            "sortField": "", "sortType": "-100",
            "historyType": 1
        })
        data = resp['data']
        ent_name = data['companyName']
        result = data['result']
        if vShow:
            print(ent_name)
            for item in result:
                shareHolderName = item["shareHolderName"]
                percent = item["percent"]
                print("-" * 20, shareHolderName, ":", percent, item)
        return ent_name, result

    def staff(self, ent_id: int):
        resp = self.__GET__(f"cloud-company-background/company/dim/staff", params={
            "gid": ent_id, "pageSize": 20, "pageNum": 1
        })
        data = resp['data']
        result = data['result']
        for item in result:
            typeSore = item["typeSore"]
            typeJoin = item["typeJoin"]
            name = item["name"]
            print("-" * 20, str(name).center(20, " "), str(typeSore).center(20, " "), str(typeJoin).center(40, " "),
                  item)
        return result

    def suggest(self, keyword, vShow: bool = False):
        resp = self.__POST__(f"cloud-tempest/search/suggest/v3", data={
            "keyword": keyword
        })
        data = resp['data']
        if vShow:
            for item in data:
                print("-" * 20, item)
        return data
