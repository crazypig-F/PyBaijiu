class SheetOperator:
    @classmethod
    def get_group(cls, sheet, group):
        """选取特定分组的样品
            例如H00N，H03N，H07N, H00E，H03E，H07E,此时指定group="N"或者group="E"
            注意：第一列必须为样品名
        :param sheet: 需要选择分组的数据表
        :param group: 样名称中该组的代号，必须在样品名称中唯一存在的
        :return: 选取分组之后的数据组成的数据表
        """
        return sheet.loc[sheet.index.str.contains(group), :]

    @classmethod
    def clean_zero(cls, sheet):
        """
        :param sheet: 输入的表格，一行为一个样本的数据
        :return: 清除全为0的一列，这里使用sum==0来判断，默认数据中没有负值
        """
        return sheet.loc[:, sheet.apply(sum, axis=0) != 0]

    @classmethod
    def save_csv(cls, sheet, save_path, index=True):
        """
        :param sheet: 输入的表格
        :param save_path: 保存的路径
        :param index: 是否保存index
        :return: None
        """
        sheet.to_csv(save_path, index=index)

    @classmethod
    def sub_samples(cls, sheet, name_list):
        """选取部分样品
        :param sheet: 输入的表格
        :param name_list: 需要的样品名称列表
        :return: 选取的表格
        """
        return sheet.loc[name_list, :]
