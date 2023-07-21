import os
import pandas as pd
import re

import init


class KEGGStatistics:
    def __init__(self, ec, ko, m):
        self.ec = ec
        self.ko = ko
        self.map = m

    def ko_ec(self, ko_num):
        """根据ko号获取ec号和ec的名字以及相关的代谢通路名称
        对于类似"2.6.1.-"有"-"的ec不予处理
        一个ec对于的代谢通路有好多，这里只取第一个代谢通路
        """
        ec_res = []
        ec_name_res = []
        map_desc_res = []
        try:
            es_str = self.ko.loc[ko_num, "ec"]
            if pd.isna(es_str):
                ec_list = []
            else:
                ec_list = es_str.split(" ")
        except Exception as e:
            print(e)
            ec_list = []
        for ec in ec_list:
            an = re.search('\d+\.\d+\.\d+\.\d+', ec)
            if an:
                try:
                    ec_desc = self.ec.loc["ec:" + ec, "desc"]
                    with open(os.path.join(init.base_path, f"data/KEGG/ec-map/{ec}.txt")) as f:
                        f = f.readlines()
                        if f:
                            m = f[0][:-1]
                            map_desc = self.map.loc["path:" + m, "desc"]
                        else:
                            map_desc = ""
                        map_desc_res.append(map_desc)
                    ec_name = ec_desc.split(";")[0]
                    ec_res.append(ec)
                    ec_name_res.append(ec_name)
                except Exception as e:
                    print(e)
            else:
                print(ec)
        return ";".join(ec_res), ";".join(ec_name_res), ";".join(map_desc_res)
