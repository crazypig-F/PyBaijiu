import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import accuracy_score


class FlavorVIP:
    """获取偏最小二乘判别分析的vip
    输入表格的格式：已经取了平均值之后的数据表
        第一行为化合物名称
        第一列为样品名称，是index_col
        用样品名称类别最后一个字符区分类别
        例如：XXXE，XXYE，XXZE，XXXN，XXYN，XXZN。这里有两类：E和N
    """

    def __init__(self, csv_path, n_components=3):
        self.model = PLSRegression(n_components=n_components)
        self.X = pd.read_csv(csv_path, index_col=0)
        self.Y = self.__get_y()
        self.__fit()
        self.vips = self.get_vips()

    def __get_y(self):
        """
        :return: 类别标签
        """
        Y = pd.get_dummies([0 if i[-1] == "E" else 1 for i in self.X.index])
        return Y

    def __fit(self):
        self.model.fit(self.X, self.Y)

    def predict(self, X, Y):
        """
        :param X: 真实数据
        :param Y: 真实标签
        :return: 预测标签和真实标签准确率
        """
        Y_hat = self.model.predict(X)
        Y_hat = np.array([np.argmax(i) for i in Y_hat])
        acc = accuracy_score(Y, Y_hat)
        return acc

    def get_vips(self):
        """
        :return: 特征的VIP值由高到低排列，VIP越大，表明特征越重要
        """
        t = self.model.x_scores_
        w = self.model.x_weights_
        q = self.model.y_loadings_
        m, p = self.X.shape
        _, h = t.shape
        vips = np.zeros((p,))
        s = np.diag(t.T @ t @ q.T @ q).reshape(h, -1)
        total_s = np.sum(s)
        for i in range(p):
            weight = np.array([(w[i, j] / np.linalg.norm(w[:, j])) ** 2 for j in range(h)])
            vips[i] = np.sqrt(p * (s.T @ weight) / total_s)

        vips = dict(zip(self.X.columns.to_list(), vips))
        vips = sorted(vips.items(), key=lambda x: x[1], reverse=True)
        vips_label = [i[0] for i in vips]
        vips_val = [i[1] for i in vips]
        return dict(zip(vips_label, vips_val))

    def get_top_vips(self, top_k):
        """
        :param top_k: 取前top_k的vip, 当top_k<=0时就取vip>=1
        :return: 选取的vip的组成的数据表
        """
        vips_label = list(self.vips.keys())
        vips_val = list(self.vips.values())
        if top_k > 0:
            index = [vip for vip in vips_label[:top_k]]
        else:
            index = [vips_label[i] for i in range(len(vips_label)) if vips_val[i] >= 1]
        return self.X.loc[:, index]
