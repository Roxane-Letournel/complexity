from collections import Counter
from math import log
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
    sc_2 = list()
    for mot in s_c:
        mot2 = list(mot)
        for i in range(len(mot2)-2):
            if mot2[i] == chunk1 and mot2[i+1] == chunk2:
                del mot2[i+1]
                mot2[i] = chunk1 + chunk2
        sc_2 += [mot2]
    return sc_2


class Optimizer:

    def __init__(self):
        self.scores = {}
        self.toDo = []

    def optimize(self, s_c):
        self.toDo += [(0, s_c, set(), lexi(s_c))]

        while self.toDo:
            self.measure()

        score_min = min(self.scores.keys())
        return (score_min, self.scores[score_min])

    def measure(self):

        score, s_c, black_list, history = self.toDo.pop()
        lex = lexi(s_c)
        self.scores[score] = (lex, history)

        for chunk1 in lex:
            for chunk2 in lex:
                if (chunk1, chunk2) not in black_list:
                    interm_score = descriptionLengthIncrease(s_c,
                                                             chunk1, chunk2)
                    if interm_score <= 5:
                        hist2 = list(history)
                        hist2 += [(chunk1 + chunk2, chunk1, chunk2)]
                        black_list2 = set(black_list)
                        black_list2.add((chunk1, chunk2))
                        new_score = score + interm_score
                        new_s_c = replace_s_c(s_c, chunk1, chunk2)
                        self.toDo += [(new_score, new_s_c, black_list2, hist2)]


print("initialise Optimizer")
opt = Optimizer()

s = ["aab aaab abba baab"]
s_c = [["a", "a", "b"], ["a", "a", "a", "b"], ["a", "b", "b", "a"
                                               ], ["b", "a", "a", "b"]]
print(opt.optimize(s_c))
s = "45678 567 147 128 182 118 1132 321 21 2111 2112"



class Factorizer:

	def __init__(self, chunks):
		self.chunks = sorted(chunks, key=lambda t: len(t['word'])) # largest strings first

	def changeChunks(self, newChunks):
		self.chunks = sorted(newChunks, key=lambda t: len(t['word'])) # largest strings first

	def factorize(self, stimulus):

		# first fast factorization to cut branches faster later
        bestCost = 0
        residual = stimulus
        while(len(residual)!=0):
            i = 0
            while (i < len(self.chunks)):
                if self.chunks[i]['word'] in residual:
                    bestCost += self.chunks[i]['codelength']
                    residual.replace(self.chunks[i]['word'], '')
                    break
                else
                    i+=1

        # exploring all factorizations possibles 
        













