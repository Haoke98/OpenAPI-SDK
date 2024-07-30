# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/7/30
@Software: PyCharm
@disc:
======================================="""
from sdk import OpenAPI

if __name__ == '__main__':
    rc_api = OpenAPI(ssl_verify=False)
    rc_api.ent_details_by_uscc({
        "uscc": "91430104MACL90613W"
    })
