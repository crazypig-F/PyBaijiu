import pandas as pd

from analyse.base.statistics import BaseStatistics
from analyse.utils.taxonomy import Taxonomy


class TransStatistics(BaseStatistics):
    """宏转录组的丰度表统计
        输入的丰度表的格式：
        第一行为列名，包含n个样品的样品名称和一个分类列的列名
        第一列即是数据列，没有index_col
    """
    def __init__(self, csv_path, tax_col_name, separator=";", taxonomy_type=Taxonomy.G.value):
        super().__init__(csv_path, tax_col_name, separator, taxonomy_type)
        self.__clean()

    def __clean(self):
        """去除包含未知微生物的行
        :return: None
        """
        self.sheet.index = pd.Index([i[3:] for i in self.sheet.index])
        index_str = self.sheet.index.str
        self.sheet = self.sheet.loc[
                     ~
                     (index_str.startswith("uncultured") |
                      index_str.startswith("uc") |
                      index_str.startswith("er") |
                      index_str.startswith("unknown")), :]
