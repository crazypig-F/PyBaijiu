from analyse.statistics.transcriptome import TransStatistics
from analyse.statistics.plsda import FlavorVIP
from analyse.utils.sheet import SheetOperator
from analyse.plot.corr import CorrNetworkGraph
from analyse.statistics.characteristics import NumCharacteristics

if __name__ == '__main__':
    # t = TransStatistics("../data/transcriptome/宏转录组S_2022.csv", tax_col_name="Taxon")
    # f = FlavorVIP("../data/flavor/jiupei_part.csv")
    # vip = f.get_top_vips(10)
    # mean_top = t.get_mean().loc[:, t.get_top(top_k=10).columns[:-1]]
    #
    # vip = SheetOperator.get_group(vip, "E")
    # vip = SheetOperator.clean_zero(vip)
    #
    # mean_top = SheetOperator.get_group(mean_top, "E")
    # mean_top = SheetOperator.clean_zero(mean_top)
    #
    # corr = CorrNetworkGraph(mean_top, vip, method="spearman")
    # print(corr.edge())
    # print(corr.node())

    num_character = NumCharacteristics("../data/physicochemical/physicochemical.csv")
    print(num_character.get_mean())
