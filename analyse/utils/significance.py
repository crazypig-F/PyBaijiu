from scipy.stats import stats


class Significance:
    def __init__(self):
        pass

    @classmethod
    def t_test(cls, data1, data2):
        """
        成对样本t检验
        """
        t, p = stats.ttest_rel(data1, data2)
        return t, p
