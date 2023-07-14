import pandas as pd
from analyse.utils.taxonomy import Taxonomy


class BaseStatistics:
    """微生物高通量测序丰度表统计
    输入的丰度表的格式：
        第一行为列名，包含n个样品的样品名称和一个分类列的列名
        第一列即是数据列，没有index_col
    处理完成的表的格式：
        输出的表格是输入表格的转置
        第一行为物种分类名称
        第一列是n个样品的样品名称，作为index_col
    """

    def __init__(self, csv_path, tax_col_name, separator, taxonomy_type=Taxonomy.G.value):
        """
        :param csv_path: csv文件路径
        :param tax_col_name: taxonomy的列名
        :param separator: taxonomy之间的分隔符
        :param taxonomy_type: 需要选取的taxonomy分类学水平,默认属水平
        """
        self.sheet = pd.read_csv(csv_path)
        self.tax_col_name = tax_col_name
        self.separator = separator
        self.taxonomy_type = taxonomy_type
        self.__set_taxonomy()

    def __set_taxonomy(self):
        """设置表格的taxonomy列
        :return: None
        """
        taxonomy = self.sheet[self.tax_col_name].apply(lambda x: x.split(self.separator))
        self.sheet = self.sheet.loc[taxonomy.apply(lambda x: len(x) >= self.taxonomy_type), :].copy()
        self.sheet[self.tax_col_name] = self.sheet[self.tax_col_name].apply(lambda x: x.split(";")).apply(
            lambda x: x[self.taxonomy_type].strip())
        self.sheet = self.sheet.groupby([self.tax_col_name]).sum()

    def get_top(self, top_k):
        """获取丰度排名前k个微生物的数据
        :param top_k: 选取丰度排名前k个微生物
        :return: 由丰度排名前k个微生物组成的丰度表
        """
        top = self.sheet.apply(sum, axis=1).sort_values(ascending=False)
        # 取前top_k
        sheet_top = self.sheet.loc[top[:top_k].index, :]
        sheet_top.loc["Others", :] = self.sheet.loc[top[top_k:].index, :].sum()
        return sheet_top.T

    def get_mean(self):
        """对有平行样的数据取平均值，样品的命名必须前n个字符相同，最后一个字符用于区分平行样
            例如SampleA，SampleB，SampleC
        :return: 取平均值之后的数据组成的数据表
        """
        sheet_mean = self.sheet.T
        sheet_mean["name"] = [i[:-1] for i in sheet_mean.index]
        sheet_mean = sheet_mean.groupby(by="name").mean().astype("int")
        return sheet_mean
