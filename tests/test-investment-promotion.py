# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/12/26
@Software: PyCharm
@disc:
======================================="""
from rc_openapi_sdk import OpenAPI

if __name__ == '__main__':
    rc_api = OpenAPI(ssl_verify=False)
    # data = rc_api.investment_promotion_regional("650000", "mcxfhy38160")
    data = rc_api.investment_promotion_ranking("440000", "mccy778")
    print(data)
