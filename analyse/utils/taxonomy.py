from enum import Enum


class Taxonomy(Enum):
    """ 物种分类学的不同等级
    K-S:界门纲目科属种
    """
    K = 0
    P = 1
    C = 2
    O = 3
    F = 4
    G = 5
    S = 6
