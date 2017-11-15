from collections import Counter
from math import log2
from functools import reduce


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


def descriptionLengthIncrease(s_c, c, Ci, Cj):
    ensembleChunk = list(s_c)
    for chunk_def in c:
        if len(chunk_def["detail"]) > 1:  # ajout de la decomposition si existe
            ensembleChunk += [chunk_def["detail"][1:]]
        ensembleChunk += [[chunk_def["detail"][0]]]  # ajout de la def
    decomptes = count(ensembleChunk)

    # Nombre total d'occurence
    N = sum(decomptes.values())
    N_Ci = decomptes[Ci]
    N_Cj = decomptes[Cj]
    N_CiCj = countCiCjOccurences(ensembleChunk,  Ci,  Cj)
    N_bCiCj = N_Ci - N_CiCj
    N_CibCj = N_Cj - N_CiCj

    # Ci ou Cj ne sont pas des chunks - operation invalide
    if N_Ci * N_Cj * N_CiCj == 0:
        return 1000000

    L1 = N_CiCj * (log2((N + 3 - N_CiCj)/(N_CiCj + 1))
                   - log2(N/N_Ci) - log2(N/N_Cj))
    L2 = N_CibCj * (log2((N + 3 + N_CiCj)/(N_CibCj + 1)) - log2(N/N_Ci))
    L2 += N_bCiCj * (log2((N + 3 - N_CiCj)/(N_bCiCj + 1)) - log2(N/N_Cj))
    L3 = 3 * log2(N + 3 - N_CiCj) - log2((N_CiCj + 1) * (N_bCiCj + 1
                                                         ) * (N_CibCj + 1))
    L4 = (N - N_Ci - N_Cj) * log2((N + 3 - N_CiCj)/N)

    return L1 + L2 + L3 + L4


def lexi(s_c):
    return list(set(reduce(lambda x, y: x + y, s_c)))


def replace_s_c(s_c, chunk1, chunk2):
    sc_2 = list()
    for mot in s_c:
        mot2 = list()
        skip = False
        for i in range(len(mot)):
            if skip:
                skip = False
                continue
            if i < len(mot) - 1 and mot[i] == chunk1 and mot[i+1] == chunk2:
                mot2 += [chunk1 + chunk2]
                skip = True
            else:
                mot2 += [mot[i]]
        sc_2 += [mot2]
    return sc_2


class Optimizer:

    def __init__(self):
        self.scores = {}
        self.toDo = []

    def optimize(self, s_c, c):
        self.scores = {}
        self.toDo = []

        self.toDo += [(0, s_c, set(), c)]
        while self.toDo:
            self.measure()

        score_min = min(self.scores.keys())
        return self.scores[score_min]

    def measure(self):

        score, s_c, black_list, c = self.toDo.pop()
        lex = lexi(s_c)
        self.scores[score] = (s_c, c)
        for chunk1 in lex:
            for chunk2 in lex:
                if (chunk1, chunk2) not in black_list:
                    c2 = c[:]
                    new_chunk = chunk1 + chunk2
                    c2 += [{'word': new_chunk,
                            'detail': [new_chunk, chunk1, chunk2]}]
                    interm_score = descriptionLengthIncrease(s_c, c2,
                                                             chunk1, chunk2)
                    if interm_score < 0:
                        black_list2 = set(black_list)
                        black_list2.add((chunk1, chunk2))
                        new_score = score + interm_score
                        new_s_c = replace_s_c(s_c, chunk1, chunk2)
                        self.toDo += [(new_score, new_s_c, black_list2, c2)]
