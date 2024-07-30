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
    ms_entities_ucc = []
    ms_entities_name = ["富络工业（上海）有限公司", "富默乐国际贸易（上海）有限公司", "湖南安与信信息科技有限公司"]
    persons_name = []
    with open('test.csv', 'r', encoding='utf-8') as fr:
        reader = csv.reader(fr)
        header = next(reader)
        for row in reader:
            i, ucc, realName = row[0:3]
            print(i, ucc, realName)
            ms_entities_ucc.append(ucc)
            persons_name.append(realName)

    print("=" * 50, "正在开始测试", "=" * 50)
    with open("result-2.csv", 'w', encoding='utf-8') as fw:
        writer = csv.writer(fw)
        total_time_dlt = 0
        n = 0
        for i in range(0, 5):
            for ucc in ms_entities_ucc:
                for ms_ent_name in ms_entities_name:
                    for realName in persons_name:
                        startedAt = time.time()
                        # print(rc_api)
                        rc_api.ent_verify_person_role_match_tri_factor({
                            "creditCode": ucc,
                            "entName": ms_ent_name,
                            'realName': realName,
                            "entStatus": "true",
                        })
                        timeDlt = time.time() - startedAt
                        total_time_dlt += timeDlt
                        n += 1
                        avg_time_dlt = total_time_dlt / n
                        print("timeDlt: {} s, avg_time_dlt: {} s".format(timeDlt, avg_time_dlt))
                        writer.writerow([i, ucc, ms_ent_name, realName, i, timeDlt, ])
