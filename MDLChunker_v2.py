
# coding: utf-8

import numpy as np

import sys

import time

import functools

# In[ ]:
import optimization
import fonctions_aux
import distribution
import factorizer

# In[235]: Mise à jour codelengths
def update_codelengths(S_C,C):
    TOTAL=0 #Cout total du S_C et C
    ELTS=0 #Nombre d'éléments dans S_C et C
    for word in S_C:
        ELTS+=len(word) #compte le nombre d'éléments dans S_C
    for word in C:
        ELTS+=len(word['detail']) #compte le nombre d'éléments dans 
  #  print('number of chunks in S|C and C = ',ELTS)
  
    DETAIL=[dic['detail'] for dic in C]
    WORDS=[dic['word'] for dic in C]

    i=-1
    for chunk in WORDS: 
        i+=1
        comptSC=countStringOccurence(S_C,chunk)
        comptC=countStringOccurence(DETAIL,chunk)

        #print('Chunk',chunk,':',comptSC,'times in S|C',';',comptC,'times in C')
        
        C[i]['codelength']=-comptC*np.log2((comptC+comptSC)/(ELTS))
        TOTAL+=-(comptC+comptSC)*np.log2((comptC+comptSC)/(ELTS))
   # print('Updated Chunk =',C)
    #print(TOTAL)
    return C,TOTAL,S_C

# In[ ]:
def initialisation(stimuli,lexi):

    S_C=[]
    
    #Initialisation Chunk
    C=lexi[:]
    for i in range(0,len(lexi)):
        C[i]={}
        C[i]['word']=lexi[i]
        C[i]['detail']=[lexi[i]]
        C[i]['codelength']=1
    
    #Initialisation Stimuli|Chunk
    fact=Factorizer(C)
    fact.factorize(stimuli)
    S_C.append(fact.getBestFact())
    
    C,TOTAL,S_C=update_codelengths(S_C,C)

    return S_C,C,TOTAL
    
    
# In[ ]: 
'''MDL avec ajout de mots'''

def MDLChunker_optimized_factorized(all_stimuli):
    lexi0=initial_lexical(all_stimuli)
    stimuli=all_stimuli[0]
    S_C,C,TOTAL=initialisation(stimuli,lexi0) #fonction initialisation : modifier cutting avec 
    first_mdl=TOTAL
        
    for k in range(0,len(all_stimuli)):
        if k!=0:
            '''factorisation du dernier stimuli'''
            stimuli=all_stimuli[k]
            fact=Factorizer(C)
            fact.factorize(stimuli)
            S_C.append(fact.getBestFact())
            C,TOTAL,S_C=update_codelengths(S_C,C)
       # print('S_C before opt',S_C)
        #print(' ')
        #print('C before opt',C)
        '''optimisation : recherche de nouveaux découpages'''
        opt_S_C, opt_C = opt.optimize(S_C, C)
        opt_C,opt_mdl,opt_S_C=update_codelengths(opt_S_C,opt_C)

        
        if opt_mdl<TOTAL:
           # print(k,stimuli,opt_C)
            end_mdl=opt_mdl
            C=opt_C
            S_C=opt_S_C
            
    return C,S_C,TOTAL
    
    
print(MDLChunker_optimized_factorized(all_stimuli))

#print(MDLChunker_optimized_factorized(all_stimuli_in_one))

# In[ ]: 
'''MDL Chunker avec distribution'''

C,S_C,TOTAL,end_mdl=MDLChunker_optimized_factorized(all_stimuli)

def scan_MDL_distribution(C,S_C):    
    WORDS=[dic['word'] for dic in C]
    for chunk in WORDS:
        print('Probability of chunk',chunk,'is larger than an random distribution',addChunkCrit(chunk,S_C,C))
    return 

scan_MDL_distribution(C,S_C)

# In[ ]:
