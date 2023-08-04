from analyse.plot.corr import CorrNetworkGraph
from analyse.statistics.amplicon import AmpliconStatistics
from analyse.statistics.characteristics import NumCharacteristics
from analyse.statistics.plsda import FlavorVIP
from analyse.statistics.transcriptome import TransStatistics
from analyse.utils.sheet import SheetOperator
from analyse.utils.taxonomy import Taxonomy


def amp():
    amplicon_bac = AmpliconStatistics("./data/amplicon/bacteria.csv", tax_col_name="taxonomy")
    amplicon_fungi = AmpliconStatistics("./data/amplicon/fungi.csv", tax_col_name="taxonomy")

    nc_bac = NumCharacteristics(amplicon_bac.get_top(20)).get_mean(save_type="int")
    nc_fungi = NumCharacteristics(amplicon_fungi.get_top(20)).get_mean(save_type="int")

    sop = SheetOperator()
    bac_fungi = sop.merge(sop.get_group(nc_bac, "N").iloc[:, :-1], sop.get_group(nc_fungi, "E").iloc[:, :-1])
    return bac_fungi


def trans():
    trs = TransStatistics("./data/transcriptome/宏转录组S_2022.csv", tax_col_name="Taxon", taxonomy_type=Taxonomy.S.value)
    trs = NumCharacteristics(trs.get_top(10)).get_mean(save_type="int")

    sop = SheetOperator()
    trs = sop.get_group(trs, "N").iloc[:, :-1]
    trs = sop.clean_zero(trs)
    return trs


def flavor():
    fv = FlavorVIP("./data/flavor/jiupei.csv")
    vips = fv.get_top_vips(-1)
    sop = SheetOperator()
    vips = sop.sub_samples(vips, ["H07N", "P07N", "P30N"])
    vips = sop.clean_zero(vips)
    return vips


def main():
    trs = trans()
    vips = flavor()
    print(trs)
    print(vips)
    corr = CorrNetworkGraph(trs, vips)
    sop = SheetOperator()
    sop.save_csv(corr.node(), "./data/temp/node.csv", index=False)
    sop.save_csv(corr.edge(), "./data/temp/edge.csv", index=False)


if __name__ == '__main__':
    main()
