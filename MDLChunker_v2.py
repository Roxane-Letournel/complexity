
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


# In[109]: 

string="This process corresponds to an encoding of the input stimuli described using only the canonical chunks into a new representation in terms of the extended alphabet containing all the Chunks. Among all possible encodings, the aim is to find the shortest one. The factorization of each stimulus is generally not unique, and finding the shortest encoding is not trivial when chunks overlap."
string="In this solemn hour it is a consolation to recall and to dwell upon our repeated efforts for peace. All have been ill-starred, but all have been faithful and sincere. This is of the highest moral value--and not only moral value, but practical value--at the present time, because the wholehearted concurrence of scores of millions of men and women, whose co-operation is indispensable and whose comradeship and brotherhood are indispensable, is the only foundation upon which the trial and tribulation of modern war can be endured and surmounted. This moral conviction alone affords that ever-fresh resilience which renews the strength and energy of people in long, doubtful and dark days. Outside, the storms of war may blow and the lands may be lashed with the fury of its gales, but in our own hearts this Sunday morning there is peace. Our hands may be active, but our consciences are at rest. We must not underrate the gravity of the task which lies before us or the temerity of the ordeal, to which we shall not be found unequal. We must expect many disappointments, and many unpleasant surprises, but we may be sure that the task which we have freely accepted is one not beyond the compass and the strength of the British Empire and the French Republic. The Prime Minister said it was a sad day, and that is indeed true, but at the present time there is another note which may be present, and that is a feeling of thankfulness that, if these great trials were to come upon our Island, there is a generation of Britons here now ready to prove itself not unworthy of the days of yore and not unworthy of those great men, the fathers of our land, who laid the foundations of our laws and shaped the greatness of our country." 
texte=extract_words(string)
lexi0=initial_lexical(texte)

# In[221]: 

stimuli=['123','123','45','12345','45','45','123','45','12345']
#lexi0=initial_lexical(stimuli)
lexi0=['1','2','3','4','5','6']

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
    #Initialisation Stimuli|Chunk
 #   S_C=stimuli[:]
  #  for i in range(0,len(stimuli)):
   #     S_C[i]=cutting(stimuli[i],lexi)
    S_C=[]
    #Initialisation Chunk
    C=lexi[:]
    for i in range(0,len(lexi)):
        C[i]={}
        C[i]['word']=lexi[i]
        C[i]['detail']=[lexi[i]]
        C[i]['codelength']=1
    
    fact=Factorizer(C)
    fact.factorize(stimuli)
    S_C.append(fact.getBestFact())
    
    C,TOTAL,S_C=update_codelengths(S_C,C)

    return S_C,C,TOTAL

initialisation(stimuli,lexi0)
    
    
# In[ ]: 
'''MDL avec ajout de mots'''
stimuli=['123','123','45','12345','45','45','123','45','12345']
#lexi0=initial_lexical(stimuli)
lexi0=['1','2','3','4','5','6']
all_stimuli=stimuli[:]
lexi0=initial_lexical(all_stimuli)

def MDLChunker_optimized_factorized(all_stimuli):
    lexi0=initial_lexical(all_stimuli)
    stimuli=all_stimuli[0]
    S_C,C,TOTAL=initialisation(stimuli,lexi0) #fonction initialisation : modifier cutting avec 
    end_mdl=TOTAL
        
    for k in range(1,len(all_stimuli)):
        '''factorisation du dernier stimuli'''
        stimuli=all_stimuli[k]
        fact=Factorizer(C)
        fact.factorize(stimuli)
        S_C.append(fact.getBestFact())
        C,TOTAL,S_C=update_codelengths(S_C,C)
        
        '''optimisation : recherche de nouveaux découpages'''
        opt_S_C, opt_C = opt.optimize(S_C, C)
        opt_C,opt_mdl,opt_S_C=update_codelengths(opt_S_C,opt_C)

        
        if opt_mdl<TOTAL:
            print(k,stimuli,opt_C)
            end_mdl=opt_mdl
            C=opt_C
            S_C=opt_S_C
    print(' ')
    print('S_C final =',S_C)
    print(' ')
    print('C final =',C)
            
    return C,S_C,TOTAL,end_mdl
    
    
MDLChunker_optimized_factorized(all_stimuli)
    

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
