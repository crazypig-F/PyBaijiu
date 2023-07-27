import pandas as pd


class NumCharacteristics:
    """计算均值和标准差
       输入表格格式：
            第一行是各个属性名称
            第一列是样品名称，平行样的样品名称最后一个字符用于区分平行样
    """
    def __init__(self, csv_path="", sheet=None):
        if sheet:
            self.sheet = sheet
        else:
            self.sheet = pd.read_csv(csv_path, index_col=0)

    def get_mean(self, save_type="float"):
        """对有平行样的数据取平均值，样品的命名必须前n个字符相同，最后一个字符用于区分平行样
            例如SampleA，SampleB，SampleC
        :return: 取平均值之后的数据组成的数据表
        """
        sheet_mean = self.sheet.T
        sheet_mean["name"] = [i[:-1] for i in sheet_mean.index]
        return sheet_mean.groupby(by="name").mean().astype(save_type)

    def get_std(self):
        """
        :return: 标准差
        """
        sheet = self.sheet
        sheet["name"] = [i[:-1] for i in sheet.index]
        return sheet.groupby(by="name").std()
