# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:39:51 2017

@author: roxan
"""
import numpy as np

import sys

"""partie Jordan 10/11"""
# In[ ]:
# critère de sélection d'un nouveau chunk

#crée la liste des mots différents dans S_C et donne le nombre de mots différents et la longueur du mot le plus long
def reducedStimuli(S_C):
    diffS_C=[]
    maxLen=0
    for s_c in S_C:
        if s_c not in diffS_C:
            diffS_C+=[s_c]
            if len(s_c)>maxLen:
                maxLen=len(s_c)
    return diffS_C,len(diffS_C),maxLen

#probabilité de trouver au moins une fois n'importe quel chunk dans un stimulus 
# de longueur k, avec un lexique de n chunks en supposant leur apparition
# équiprobable
def proba(k,n):
    return 1-(1-1/n)**k

#pseudo-score d'un chunk s'il apparaît aléatoirement et de façon équiprobable
def aleaDistrib_Score(S_C,C):
    diffS_C,nbDiffS_C,maxLen=reducedStimuli(S_C)
    #maxLen=max(map(len,S_C))
    n=len(C)    #nombre de chunks
    Sk=[sum([len(diffS_C[i])==k for i in range(len(diffS_C))]) for k in range(1,maxLen+1)]   #contien le nombre de mots de longueur k
    return (1/nbDiffS_C)*sum([Sk[k-1]*proba(k,n) for k in range(1,maxLen+1)])
    #Sk=[sum([len(S_C[i])==k for i in range(len(S_C))]) for k in range(1,maxLen+1)]   #contien le nombre de mots de longueur k
    #return (1/len(S_C))*sum([Sk[k-1]*proba(k,n) for k in range(1,maxLen+1)])

#pseudo-score d'un chunk dans la liste réduite S_C = 'bonne' distribution
# on ajoute 1 s'il est présent au moins une fois dans le mot
def distribScore(newChunk,S_C): #utiliser C et C[-1] ?
    score=0
    diffS_C, nbDiffS_C,maxLen=reducedStimuli(S_C)
    return sum([newChunk in s_c for s_c in diffS_C])

#critère pour garder un nouveau chunk qui vient d'être proposé
def addChunkCrit(newChunk,S_C,C): #remplacer newChunk par C[-1] ?
    diffS_C, nbDiffS_C,maxLen=reducedStimuli(S_C)
    threshold=aleaDistrib_Score(S_C,C)
    return threshold < (1/nbDiffS_C)*distribScore(newChunk,S_C)
    #return (1/nbDiffS_C)*distribScore(newChunk,S_C)


"""fin partie Jordan 10/11"""