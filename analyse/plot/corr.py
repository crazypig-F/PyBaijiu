import pandas as pd
import scipy.stats


class CorrNetworkGraph:
    """整理用于相关性网络图的数据，包括边的数据整理和顶点的数据整理
    输入两张表格：第一张是微生物的丰度表格，第二张是风味化合物的GC-MS数据表格
        第一张表格数据格式：第一行为微生物名称，第一列为样品名称，是index_col
        第一张表格数据格式：第一行为风味化合物名称，第一列为样品名称，是index_col
    注意1：两张表格的样品数量必须一致，而且必须每一行都对应同一个样品
    注意2：此处以微生物和风味数据为例，如果要计算其他类型数据的相关性关系可以适当改动
    """
    def __init__(self, sheet1, sheet2, method="pearson"):
        self.sheet1 = sheet1
        self.sheet2 = sheet2
        self.r, self.p = self.__tow_mat(method)

    def __tow_mat(self, method):
        """
        :param method: 计算相关性的方法
        :return: 相关性系数和相关性显著性
        """
        res_r = pd.DataFrame(index=self.sheet1.columns, columns=self.sheet2.columns)
        res_p = pd.DataFrame(index=self.sheet1.columns, columns=self.sheet2.columns)
        for name1 in self.sheet1.columns:
            for name2 in self.sheet2.columns:
                row1 = self.sheet1[name1]
                row2 = self.sheet2[name2]
                if method == "pearson":
                    r = scipy.stats.pearsonr(row1, row2)[0]
                    p = scipy.stats.pearsonr(row1, row2)[1]
                elif method == "spearman":
                    r = scipy.stats.spearmanr(row1, row2)[0]
                    p = scipy.stats.spearmanr(row1, row2)[1]
                else:
                    raise Exception
                if (r > 0.6 or r < -0.6) and p < 0.05:
                    res_r.loc[name1, name2] = r
                    res_p.loc[name1, name2] = p
        return res_r, res_p

    def edge(self):
        """
        :return: 相关性网络图边的信息
        """
        source_list = []
        dest_list = []
        r_list = []
        p_list = []
        weight_list = []
        color_list = []
        for i, index in enumerate(self.r.index):
            for j, col in enumerate(self.r.columns):
                r = self.r.loc[index, col]
                p = self.p.loc[index, col]
                if not pd.isna(r):
                    source_list.append(index)
                    dest_list.append(col)
                    r_list.append(r)
                    p_list.append(p)
                    weight_list.append(abs(r))
                    if r >= 0:
                        color_list.append("red")
                    else:
                        color_list.append("blue")
        result = {
            "Id": list(range(len(source_list))),
            "Source": source_list,
            "Target": dest_list,
            "Weight": weight_list,
            "Relevance": r_list,
            "Significance": p_list,
            "Color": color_list
        }
        return pd.DataFrame(result)

    def node(self):
        """
        :return: 相关性网络图顶点的信息
        """
        sheet_e = self.edge()
        source_list = sheet_e["Source"].to_list()
        target_list = sheet_e["Target"].to_list()
        label_list = [i for i in self.sheet1.columns if i in source_list or i in target_list] + \
                  [i for i in self.sheet2.columns if i in source_list or i in target_list]
        color_list = ["node1" for i in self.sheet1.columns if i in source_list or i in target_list] + \
                     ["node2" for i in self.sheet2.columns if i in source_list or i in target_list]
        result = {
            "Id": label_list,
            "Label": label_list,
            "Color": color_list
        }
        return pd.DataFrame(result)
