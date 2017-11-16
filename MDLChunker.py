# coding: utf-8

import numpy as np
import sys
import time
import functools

from optimization import countCiCjOccurences, replace_s_c
from fonctions_aux import initial_lexical, countStringOccurence
from factorizer import Factorizer
from distribution import addChunkCrit


def update_codelengths(S_C, C):
    TOTAL = 0  # Cout total du S_C et C
    ELTS = 0  # Nombre d'éléments dans S_C et C
    for word in S_C:
        ELTS += len(word)  # compte le nombre d'éléments dans S_C
    for word in C:
        ELTS += len(word['detail'])  # compte le nombre d'éléments dans
    # print('number of chunks in S|C and C = ',ELTS)

    DETAIL = [dic['detail'] for dic in C]
    WORDS = [dic['word'] for dic in C]

    i = -1
    for chunk in WORDS:
        i += 1
        comptSC = countStringOccurence(S_C, chunk)
        comptC = countStringOccurence(DETAIL, chunk)

        #print('Chunk',chunk,':',comptSC,'times in S|C',';',comptC,'times in C')

        C[i]['codelength'] = -comptC * np.log2((comptC + comptSC) / (ELTS))
        TOTAL += -(comptC + comptSC) * np.log2((comptC + comptSC) / (ELTS))
    # print('Updated Chunk =',C)
    # print(TOTAL)
    return C, TOTAL, S_C


def initialisation(stimuli, lexi):

    S_C = []

    # Initialisation Chunk
    C = lexi[:]
    for i in range(0, len(lexi)):
        C[i] = {}
        C[i]['word'] = lexi[i]
        C[i]['detail'] = [lexi[i]]
        C[i]['codelength'] = 1

    # Initialisation Stimuli|Chunk
    # print(C)
    fact = Factorizer(C)
    fact.factorize(stimuli)
    S_C.append(fact.getBestFact())

    C, TOTAL, S_C = update_codelengths(S_C, C)

    return S_C, C, TOTAL


'''MDL avec ajout de mots'''


def MDLChunker_search_factorized(all_stimuli):
    lexi0 = initial_lexical(all_stimuli)
    stimuli = all_stimuli[0]
    # fonction initialisation : modifier cutting avec
    S_C, C, TOTAL = initialisation(stimuli, lexi0)
    first_mdl = TOTAL

    for k in range(0, len(all_stimuli)):
        if k != 0:
            '''factorisation du dernier stimuli'''
            stimuli = all_stimuli[k]
            fact = Factorizer(C)
            fact.factorize(stimuli)
            S_C.append(fact.getBestFact())
            C, TOTAL, S_C = update_codelengths(S_C, C)

        '''optimisation : recherche de nouveaux découpages'''
        #opt_S_C, opt_C = opt.optimize(S_C, C)
        # opt_C,opt_mdl,opt_S_C=update_codelengths(opt_S_C,opt_C)

        best_C, best_mdl, best_a, best_b, best_S_C, best_word = search(S_C, C)

        while best_mdl < TOTAL:
           # print(k,stimuli,opt_C)
            end_mdl = best_mdl
            C = best_C
            S_C = best_S_C
            best_C, best_mdl, best_a, best_b, best_S_C, best_word = search(
                S_C, C)

    return C, S_C, TOTAL


def MDLChunker_search_factorized_distribution(all_stimuli, alpha):
    lexi0 = initial_lexical(all_stimuli)
    stimuli = all_stimuli[0]
    # fonction initialisation : modifier cutting avec
    S_C, C, TOTAL = initialisation(stimuli, lexi0)
    first_mdl = TOTAL

    for k in range(0, len(all_stimuli)):
        if k != 0:
            '''factorisation du dernier stimuli'''
            stimuli = all_stimuli[k]
            fact = Factorizer(C)
            fact.factorize(stimuli)
            S_C.append(fact.getBestFact())
            C, TOTAL, S_C = update_codelengths(S_C, C)

        '''optimisation : recherche de nouveaux découpages'''
        #opt_S_C, opt_C = opt.optimize(S_C, C)
        # opt_C,opt_mdl,opt_S_C=update_codelengths(opt_S_C,opt_C)

        best_C, best_mdl, best_a, best_b, best_S_C, best_word = search(S_C, C)

        while best_mdl < TOTAL and addChunkCrit(
                best_word, best_S_C, best_C, alpha):
           # print(k,stimuli,opt_C)
            end_mdl = best_mdl
            C = best_C
            S_C = best_S_C
            best_C, best_mdl, best_a, best_b, best_S_C, best_word = search(
                S_C, C)

    return C, S_C, TOTAL


# print(MDLChunker_search_factorized_distribution(all_stimuli,alpha))

def introduce_new_word(a, b, S_C, C):
    new_S_C = S_C[:]
    new_C = C[:]
    new_word = C[a]['word'] + C[b]['word']

    # Update C avec nouveau chunk
    new_C.append({'word': new_word, 'detail': [
                 new_word, C[a]['word'], C[b]['word']]})

    # Update S_C avec nouveau chunk
    new_S_C = replace_s_c(new_S_C, C[a]['word'], C[b]['word'])

    # Udpate codelenghts
    new_C, TOTAL, new_S_C = update_codelengths(new_S_C, new_C)

    return(new_S_C, new_C, TOTAL)

# new_S_C,new_C,TOTAL=introduce_new_word(3,4,S_C,C)


def search(S_C, C):
    LEXI = [dic['word'] for dic in C]
    best_mdl = 1000000
    best_a = 0
    best_b = 0
    best_C = C[:]
    best_S_C = S_C[:]
    best_word = ' '

    for a in range(0, len(LEXI)):
       # print('recherche en cours...',a/len(LEXI))
        for b in range(0, len(LEXI)):
            if countCiCjOccurences(S_C, LEXI[a], LEXI[b]) != 0:
                new_S_C, new_C, mdl = introduce_new_word(a, b, S_C, C)
                if mdl <= best_mdl:
                    best_mdl = mdl
                    best_a = LEXI[a]
                    best_b = LEXI[b]
                    best_C = new_C[:]
                    best_S_C = new_S_C[:]
                    best_word = LEXI[a] + LEXI[b]

    return best_C, best_mdl, best_a, best_b, best_S_C, best_word


# best_C,best_mdl, best_a, best_b, best_S_C, best_word=search(S_C,C)
'''MDL Chunker avec distribution'''
# C,S_C,TOTAL,end_mdl=MDLChunker_optimized_factorized(all_stimuli)


def scan_MDL_distribution(C, S_C, alpha):
    WORDS = [dic['word'] for dic in C]
    for chunk in WORDS:
        print(chunk, addChunkCrit(chunk, S_C, C, alpha))

        #print('Probability of chunk',chunk,'is larger than an random distribution',addChunkCrit(chunk,S_C,C))
    return


def initialisationTOTAL(all_stimuli, lexi):

    S_C = []

    # Initialisation Chunk
    C = lexi[:]
    for i in range(0, len(lexi)):
        C[i] = {}
        C[i]['word'] = lexi[i]
        C[i]['detail'] = [lexi[i]]
        C[i]['codelength'] = 1

    # Initialisation Stimuli|Chunk
    # print(C)
    for stimulus in all_stimuli:
        fact = Factorizer(C)
        fact.factorize(stimulus)
        S_C.append(fact.getBestFact())

    C, TOTAL, S_C = update_codelengths(S_C, C)

    return S_C, C, TOTAL


if __name__ == "__main__":
    # initialisation
    initialisation(stimuli, lexi0)

    scan_MDL_distribution(C, S_C, 1)

    initialisationTOTAL(all_stimuli, lexi0)
