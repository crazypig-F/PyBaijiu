import pandas as pd
import os
base_path = r"D:\code\python_code\BaijiuAnalyse"
kegg_ec = pd.read_csv(os.path.join(base_path, "data\KEGG\ec.csv"), index_col=0)
kegg_ko = pd.read_csv(os.path.join(base_path, "data\KEGG\ko.csv"), index_col=0)
kegg_map = pd.read_csv(os.path.join(base_path, "data\KEGG\map.csv"), index_col=0)
