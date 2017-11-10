from collections import Counter
from math import log
from functools import reduce
from MDLChunker import initialisation


def countCiCjOccurences(s_c, Ci, Cj):
    """
        Nombre de fois ou s = CiCj apparait dans s_c
    """
    somme = 0
    s = [Ci, Cj]
    for mot in s_c:
        somme += sum(mot[i:i + len(s)] == s for i in range(len(mot)))
    return somme


def count(s_c):
    """
        Renvoi un dictionnaire contenant le decompte de chaque motif
        {"motif1": 25, "motif2": 30}
    """
    return reduce(lambda x, y: x + y, map(Counter, s_c))


def descriptionLengthIncrease(s_c, Ci, Cj):
    decomptes = count(s_c)
    # Nombre total d'occurence
    N = sum(decomptes.values())
    N_Ci = decomptes[Ci]
    N_Cj = decomptes[Cj]
    N_CiCj = countCiCjOccurences(s_c,  Ci,  Cj)
    N_bCiCj = N_Ci - N_CiCj
    N_CibCj = N_Cj - N_CiCj

    # Ci ou Cj ne sont pas des chunks - operation invalide
    if N_Ci * N_Cj * N_CiCj == 0:
        return 1000000

    L1 = N_CiCj * (log((N + 3 - N_CiCj)/(N_CiCj + 1))
                   - log(N/N_Ci) - log(N/N_Cj))
    L2 = N_CibCj * (log((N + 3 + N_CiCj)/(N_CibCj + 1)) - log(N/N_Ci))
    L2 += N_bCiCj * (log((N + 3 - N_CiCj)/(N_bCiCj + 1)) - log(N/N_Cj))
    L3 = 3 * log(N + 3 - N_CiCj) - log((N_CiCj + 1) * (N_bCiCj + 1
                                                       ) * (N_CibCj + 1))
    L4 = (N - N_Ci - N_Cj) * log((N + 3 + N_CiCj)/N)
    return L1 + L2 + L3 + L4


def lexi(s_c):
    return list(set(reduce(lambda x, y: x + y, s_c)))


def replace_s_c(s_c, chunk1, chunk2):
    sc_2 = []
    for mot in s_c:
        for i in range(len(mot)-2):
            if mot[i] == chunk1 and mot[i+1] == chunk2:
                del mot[i+1]
                mot[i] = chunk1 + chunk2
        sc_2 += [mot]
    return sc_2


class Optimizer:

    def __init__(self):
        self.scored_lexi = {}
        self.toDo = []

    def optimize(self, s_c):
        self.toDo += [(0, s_c, set())]

        while self.toDo:
            self.measure()

        score_min = min(self.scored_lexi.keys())
        return (score_min, self.scored_lexi[score_min])

    def measure(self):

        score, s_c, black_list = self.toDo.pop()
        lex = lexi(s_c)
        new_node = False

        for chunk1 in lex:
            for chunk2 in lex:
                if (chunk1, chunk2) not in black_list:
                    black_list.add((chunk1, chunk2))
                    interm_score = descriptionLengthIncrease(s_c,
                                                             chunk1, chunk2)
                    if interm_score <= 100:
                        new_node = True
                        new_score = score + interm_score
                        new_s_c = replace_s_c(s_c, chunk1, chunk2)
                        self.toDo += [(new_score, new_s_c, black_list)]

        # Sans nouveaux noeud, on enregistre le lexique et son score
        if not new_node:
            self.scored_lexi[score] = lex


print("initialise Optimizer")
opt = Optimizer()

s = ["aab aaab abba baab"]
s_c = [["a", "a", "b"], ["a", "a", "a", "b"], ["a", "b", "b", "a"
                                               ], ["b", "a", "a", "b"]]
print(opt.optimize(s_c))
s = "45678 567 147 128 182 118 1132 321 21 2111 2112"
s_c = initialisation(s, ["1", "2", "3", "4", "5", "6", "7", "8"])
