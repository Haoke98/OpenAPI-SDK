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
import os.path
import time
from pprint import pprint
import json

import requests


class OpenAPI(object):
    session_file = os.path.expanduser('~/openapi-session.json')
    session = None

    def __init__(self, appKey: str = None, appSecret: str = None, baseurl: str = None,
                 ssl_verify: bool = True):
        if appKey is None:
            self.username = os.getenv("RC-OPEN-API-KEY")
        else:
            self.username = appKey
        if appSecret is None:
            self.password = os.getenv("RC-OPEN-API-SECRET")
        else:
            self.password = appSecret
        env_baseurl = os.getenv("RC-OPEN-API-BASEURL")
        if baseurl is not None:
            self.baseurl = baseurl
        elif env_baseurl is not None:
            self.baseurl = env_baseurl
        else:
            self.baseurl = "https://open.0p.fit/data-center"
        self.ssl_verify = ssl_verify
        self.load_session()

    def load_session(self):
        print("session loaded from %s" % self.session_file)
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r', encoding='utf-8') as f:
                self.session = json.load(f)
        if self.session is None:
            self.session = {
                "key": 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJTTFJDLUNvbXBhbnktc2FkYW0iLCJzdWIiOiJhZjZlNTU1Mi0zMTBlLTQzMjAtYjk4OC1iZWQyYjk0ODMzY2EiLCJuYW1lIjoidGVzdC11c2VyLTAwMDIzIiwiZXhwIjoxNzEzOTU2NTQ5fQ.tf0R9zRg15E73sWezvt6I_oAp5w58fQb75slJ3dXfa4',
                "expire": 3600,
                "status": 0
            }

    def save_session(self):
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session, f, ensure_ascii=False)

    def __get_headers__(self):
        return {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT',
                'Authorization': self.session['key']}

    def authorize(self):
        url = self.baseurl + '/rest/auth/key'
        jsonForm = {
            "name": self.username,
            "pwd": self.password
        }
        resp = self.__post__(url, jsonForm)
        # FIXME: 这里返回的Reps永远是None
        self.session = resp
        self.save_session()

    def __post__(self, url, jsonForm: dict):
        jsonForm["requestId"] = datetime.datetime.now().strftime("%Y%m%d%H%M")
        jsonForm["timestamp"] = time.time()
        jsonForm['sign'] = 'd15e5a64302e9dc9b54efb04500c13c6'
        print(url, self.__get_headers__())
        resp = requests.post(url, json=jsonForm, headers=self.__get_headers__(), verify=self.ssl_verify)
        if resp.status_code == 200:
            resp_dict = resp.json()
            pprint(resp_dict, indent=4)
            if resp_dict['code'] == 401:
                self.authorize()
                self.__post__(url, jsonForm)
            elif resp_dict['code'] == 9999:
                raise Exception("用户名和密码错误")
            elif resp_dict['code'] == 0:
                return resp_dict['data']
            else:
                logging.error(f"请求异常:{resp_dict}")
        else:
            logging.error(f"[{resp}, {resp.text}]")

    def ms_ent_verify_tri_factor(self, jsonForm: dict):
        """
        市场主体三要素验证接口
        :param jsonForm:
        :return:
        """
        url = self.baseurl + '/rest/ent/verification/tri-factor'
        self.__post__(url, jsonForm)

    def ent_verify_quad_factor(self, jsonForm: dict):
        url = self.baseurl + '/rest/ent/verification/quad-factor'
        self.__post__(url, jsonForm)

    def ent_verify_tri_factor_shareholder(self, jsonForm: dict):
        url = self.baseurl + '/rest/ent/verification/tri-factor-shareholder'
        self.__post__(url, jsonForm)

    def ent_verify_quad_factor_shareholder(self, jsonForm: dict):
        url = self.baseurl + '/rest/ent/verification/quad-factor-shareholder'
        self.__post__(url, jsonForm)

    def ent_verify_person_role_match_quad_factor(self, jsonForm: dict):
        """
        市场主体与自然人身份关系四要素验证接口
        :param jsonForm:
        :return:
        """
        url = self.baseurl + '/rest/ent/verification/person-role-match/quad-factor'
        self.__post__(url, jsonForm)

    def ent_verify_person_role_match_tri_factor(self, jsonForm: dict):
        """
        市场主体与自然人身份关系三要素验证接口
        :param jsonForm:
        :return:
        """
        url = self.baseurl + '/rest/ent/verification/person-role-match/tri-factor'
        return self.__post__(url, jsonForm)

    def ent_details_by_uscc(self, jsonForm):
        url = self.baseurl + '/rest/ent/details/uscc'
        return self.__post__(url, jsonForm)

    def bypass_domains(self):
        url = self.baseurl + '/rest/net/bypass_domains'
        self.__post__(url, {})

    def direct_dsl(self, dsl_body: dict):
        jsonForm = {"dsl_body": json.dumps(dsl_body)}
        url = self.baseurl + '/rest/dsl-direct/query'
        return self.__post__(url, jsonForm)

    def investment_promotion_regional(self, area_code: str, node_code: str):
        """
        区域性招商
        :param area_code:
        :param node_code:
        :return:
        """
        url = self.baseurl + '/rest/investment-promotion/regional'
        jsonForm = {"areaCode": area_code, "nodeCode": node_code}
        return self.__post__(url, jsonForm)

    def investment_promotion_ranking(self, area_code: str, node_code: str):
        """
        榜单招商
        :param area_code:
        :param node_code:
        :return:
        """
        url = self.baseurl + '/rest/investment-promotion/ranking'
        jsonForm = {"areaCode": area_code, "nodeCode": node_code}
        return self.__post__(url, jsonForm)
