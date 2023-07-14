import pandas as pd


class NumCharacteristics:
    """计算均值和标准差
       输入表格格式：
            第一行是各个属性名称
            第一列是样品名称，平行样的样品名称最后一个字符用于区分平行样
    """
    def __init__(self, csv_path):
        self.sheet = pd.read_csv(csv_path, index_col=0)

    def get_mean(self):
        """
        :return:均值
        """
        sheet = self.sheet
        sheet["name"] = [i[:-1] for i in sheet.index]
        return sheet.groupby(by="name").mean()

    def get_std(self):
        """
        :return: 标准差
        """
        sheet = self.sheet
        sheet["name"] = [i[:-1] for i in sheet.index]
        return sheet.groupby(by="name").std()
