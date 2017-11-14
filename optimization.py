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
        ensembleChunk += [chunk_def["detail"]]
    decomptes = count(ensembleChunk)

    # Nombre total d'occurence
    N = sum(decomptes.values())
    N_Ci = decomptes[Ci]
    N_Cj = decomptes[Cj]
    N_CiCj = countCiCjOccurences(s_c,  Ci,  Cj)
    N_bCiCj = N_Ci - N_CiCj
    N_CibCj = N_Cj - N_CiCj

    # Ci ou Cj ne sont pas des chunks - operation invalide

    # formules differentes si Ci==Cj

    if N_Ci * N_Cj * N_CiCj == 0:
        return 1000000


    
    L1 = N_CiCj * (log2((N + 3 - N_CiCj)/(N_CiCj + 1))
                   - log2(N/N_Ci) - log2(N/N_Cj))
    L2 = N_CibCj * (log2((N + 3 - N_CiCj)/(N_CibCj + 1)) - log2(N/N_Ci))
    if Ci!=Cj:
        L2 += N_bCiCj * (log2((N + 3 - N_CiCj)/(N_bCiCj + 1)) - log2(N/N_Cj))

    L3 = 3 * log2(N + 3 - N_CiCj) - log2((N_CiCj + 1) * (N_bCiCj + 1
                                                         ) * (N_CibCj + 1))
    if Ci==Cj:
        L4 = (N - N_Ci) * log2((N + 3 - N_CiCj)/N)
    else:
        L4 = (N - N_Ci - N_Cj) * log2((N + 3 - N_CiCj)/N)
    


    """
    L1 = N_CiCj * (log2((N + 3 - N_CiCj)/(N_CiCj + 1))
                   - log2(N/N_Ci) - log2(N/N_Cj))
    L2 = N_CibCj * (log2((N + 3 - N_CiCj)/(N_CibCj + 1)) - log2(N/N_Ci))
    L2 += N_bCiCj * (log2((N + 3 - N_CiCj)/(N_bCiCj + 1)) - log2(N/N_Cj))

    L3 = 3 * log2(N + 3 - N_CiCj) - log2((N_CiCj + 1) * (N_bCiCj + 1
                                                         ) * (N_CibCj + 1))
    L4 = (N - N_Ci - N_Cj) * log2((N + 3 - N_CiCj)/N)
    """


    """
    print("L1 = ", L1)
    print("L2 = ", L2)
    print("L3 = ", L3)
    print("L4 = ", L4)
    """
    return L1 + L2 + L3 + L4


def lexi(s_c):
    return list(set(reduce(lambda x, y: x + y, s_c)))


def replace_s_c(s_c, chunk1, chunk2):
    sc_2 = list()
    for mot in s_c:
        mot2 = list(mot)
        for i in range(len(mot2)-1):
            if mot2[i] == chunk1 and mot2[i+1] == chunk2:
                del mot2[i+1]
                mot2[i] = chunk1 + chunk2
        sc_2 += [mot2]
    return sc_2


class Optimizer:

    def __init__(self):
        self.toDo = []
        self.black_list = set()
        self.minS_C = []
        self.min_C = []
        self.minS_C_score = 10

    def optimize(self, s_c, c):
        self.scores = {}
        self.toDo = []
        self.toDo += [(0, s_c, self.black_list, c)]

        """
        self.measure()
        for i in range(len(self.toDo)):
            self.measure()
        """
        i = 0
        while self.toDo and i < 5000000:
            i += 1
            #print(len(self.toDo))
            self.measure()
        print("***************", i)
        return self.minS_C, self.min_C

    def measure(self):

        score, s_c, black_list, c = self.toDo.pop()
        lex = lexi(s_c)
        if score < self.minS_C_score:
            self.black_list = black_list
            self.minS_C = s_c
            self.min_C = c

        for chunk1 in lex:
            for chunk2 in lex:
                if (chunk1, chunk2) not in black_list:
                    interm_score = descriptionLengthIncrease(s_c, c,
                                                             chunk1, chunk2)
                    #print("***** interm_score(", chunk1, ",", chunk2, ") = ", interm_score)
                    if interm_score < 0:
                        c2 = c[:]
                        new_chunk = chunk1 + chunk2
                        c2 += [{'word': new_chunk,
                            'detail': [new_chunk, chunk1, chunk2]}]
                        black_list2 = set(black_list)
                        black_list2.add((chunk1, chunk2))
                        new_score = score + interm_score
                        new_s_c = replace_s_c(s_c, chunk1, chunk2)
                        self.toDo += [(new_score, new_s_c, black_list2, c2)]


print("initialise Optimizer")
opt = Optimizer()

s = ["aab aaab abba baab"]
s_c = [["c", "a", "b"], ["a", "c", "a", "b"], ["a", "b", "c", "c"],
       ["b", "c", "a", "b"], ['a', 'b'], ['a', 'b']]
c = [{"word": "a", "detail": ["a"]}, {"word": "b", "detail": ["b"]},
     {"word": "c", "detail": ["c"]}]
print(opt.optimize(s_c, c))
