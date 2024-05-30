# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/5/30
@Software: PyCharm
@disc: 接口延迟测试
======================================="""
import csv
import time

from sdk import OpenAPI

if __name__ == '__main__':
    rc_api = OpenAPI(ssl_verify=False)
    with open('test.csv', 'r', encoding='utf-8') as fr, open("result.csv", 'w', encoding='utf-8') as fw:
        reader = csv.reader(fr)
        writer = csv.writer(fw)
        header = next(reader)
        total_time_dlt = 0
        n = 0
        for row in reader:
            if len(row) == 6:
                i, ucc, realName, IDCarNoMD5, result, first = row
            elif len(row) == 5:
                i, ucc, realName, IDCarNoMD5, result = row
                first = None
            else:
                raise ValueError("ot enough values to unpack,row:{}".format(row))
            print(i, ucc, realName, IDCarNoMD5)
            startedAt = time.time()
            # print(rc_api)
            rc_api.ent_verify_person_role_match_tri_factor({
                "creditCode": ucc,
                "entName": "富络工业（上海）有限公司",
                'realName': realName,
                "entStatus": "true",
            })
            timeDlt = time.time() - startedAt
            total_time_dlt += timeDlt
            n += 1
            avg_time_dlt = total_time_dlt / n
            print("timeDlt: {} s, avg_time_dlt: {} s".format(timeDlt, avg_time_dlt))
            writer.writerow([i, ucc, realName, IDCarNoMD5, timeDlt, first, timeDlt])
