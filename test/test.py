import pandas as pd

import init
from analyse.statistics.kegg import KEGGStatistics
from analyse.statistics.transcriptome import TransStatistics
from analyse.utils.sheet import SheetOperator


def test_trans():
    t = TransStatistics("../data/transcriptome/宏转录组S_2022.csv", tax_col_name="Taxon")
    mean_top = t.get_top(top_k=10).iloc[:, :-1]
    mean_top = SheetOperator.get_group(mean_top, "E")
    SheetOperator.save_csv(mean_top, "../data/temp/transcriptome.csv")

    num_character = pd.read_csv("../data/physicochemical/physicochemical.csv", index_col=0)
    physicochemical_sub_samples = SheetOperator.sub_samples(num_character, [i + str(j) for i in
                                                                            ["H07E", "P07E", "P30E", "H07N", "P07N",
                                                                             "P07N"] for j in range(1, 4)])
    physicochemical_sub_samples = SheetOperator.get_group(physicochemical_sub_samples, "E")
    SheetOperator.save_csv(physicochemical_sub_samples, "../data/temp/physicochemical.csv")


def test_kegg(name):
    kegg = KEGGStatistics(init.kegg_ec, init.kegg_ko, init.kegg_map)
    df = pd.read_excel(f"./{name}.xlsx")
    "EC	Name	Pathway"
    df["EC"] = df.loc[:, "KO"].apply(lambda x: kegg.ko_ec(x)[0])
    df["Name"] = df.loc[:, "KO"].apply(lambda x: kegg.ko_ec(x)[1])
    df["Pathway"] = df.loc[:, "KO"].apply(lambda x: kegg.ko_ec(x)[2])
    df.to_csv(f"{name}.csv", index=False)


if __name__ == '__main__':
    test_kegg("gene_ko_species")
