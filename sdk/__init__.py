# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/4/18
@Software: PyCharm
@disc:
======================================="""
import datetime
import logging
import time
from pprint import pprint

import requests


class OpenAPI(object):

    def __init__(self, username: str, password: str, baseurl: str = "https://open.0p.fit/data-center"):
        self.username = username
        self.password = password
        self.baseurl = baseurl
        self.session = {
            "key": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJTTFJDLUNvbXBhbnktc2FkYW0iLCJzdWIiOiJhZjZlNTU1Mi0zMTBlLTQzMjAtYjk4OC1iZWQyYjk0ODMzY2EiLCJuYW1lIjoidGVzdC11c2VyLTAwMDIzIiwiZXhwIjoxNzEzOTU2NTQ5fQ.tf0R9zRg15E73sWezvt6I_oAp5w58fQb75slJ3dXfa4',
            "expire": 3600,
            "status": 0
        }

    def __get_headers__(self):
        return {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT',
                'Authorization': self.session['key']}

    def authorize(self):
        url = self.baseurl + '/rest/auth/key'
        print(url)
        jsonForm = {
            "name": self.username,
            "pwd": self.password
        }
        resp = self.__post__(url, jsonForm)
        self.session = resp['data']

    def __post__(self, url, jsonForm):
        resp = requests.post(url,
                             json=jsonForm,
                             headers=self.__get_headers__())
        if resp.status_code == 200:
            resp_dict = resp.json()
            pprint(resp_dict, indent=4)
            if resp_dict['code'] == 401:
                self.authorize()
                self.__post__(url, jsonForm)
            elif resp_dict['code'] == 0:
                return resp_dict
            else:
                logging.error(f"请求异常:{resp_dict}")
        else:
            logging.error(f"[{resp}, {resp.text}]")

    def check(self, jsonForm: dict):
        url = self.baseurl + '/rest/ent/check'
        print(url)
        jsonForm["requestId"] = datetime.datetime.now().strftime("%Y%m%d%H%M")
        jsonForm["timestamp"] = time.time()
        jsonForm['sign'] = 'd15e5a64302e9dc9b54efb04500c13c6'
        self.__post__(url, jsonForm)
