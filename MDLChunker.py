
# coding: utf-8

import numpy as np

import sys

import time

import functools
# In[98]:rend une liste avec les longueurs de chaque syllabe du lexique

def ll(b):

    r=[]
    for i in range(len(b)):
        r+=[len(b[i])]
    return r

ll(["10","1","0"])


# In[99]: Découper un texte avec un lexique donné

def cutting(a,b):
    # a est le stream à découper, b le lexique avec lequel on le fait
    cutstream=[]
    while a!="":
        i=0
        while a[:ll(b)[i]]!=b[i] :
            i+=1
        cutstream+=[b[i]]
        a=a[ll(b)[i]:]
    return cutstream


# In[107]: Traitement du string initial

def extract_words(string):
    string=string.replace('.','')
    string=string.replace(',','')
    string=string.replace('?',' ')
    string=string.replace(':','')
    string=string.replace('!','')
    string=string.replace('-','')
    string=string.lower()
    texte=string.split( )
    return texte


# In[108]: Définir lexique initial "canonical chunks"

def initial_lexical(texte):
    lexi=[]
    for string in texte:
        for i in range(len(string)):
            if string[i] not in lexi:
                lexi.append(string[i])
    return lexi


# In[109]: 

string="This process corresponds to an encoding of the input stimuli described using only the canonical chunks into a new representation in terms of the extended alphabet containing all the Chunks. Among all possible encodings, the aim is to find the shortest one. The factorization of each stimulus is generally not unique, and finding the shortest encoding is not trivial when chunks overlap."
string="In this solemn hour it is a consolation to recall and to dwell upon our repeated efforts for peace. All have been ill-starred, but all have been faithful and sincere. This is of the highest moral value--and not only moral value, but practical value--at the present time, because the wholehearted concurrence of scores of millions of men and women, whose co-operation is indispensable and whose comradeship and brotherhood are indispensable, is the only foundation upon which the trial and tribulation of modern war can be endured and surmounted. This moral conviction alone affords that ever-fresh resilience which renews the strength and energy of people in long, doubtful and dark days. Outside, the storms of war may blow and the lands may be lashed with the fury of its gales, but in our own hearts this Sunday morning there is peace. Our hands may be active, but our consciences are at rest. We must not underrate the gravity of the task which lies before us or the temerity of the ordeal, to which we shall not be found unequal. We must expect many disappointments, and many unpleasant surprises, but we may be sure that the task which we have freely accepted is one not beyond the compass and the strength of the British Empire and the French Republic. The Prime Minister said it was a sad day, and that is indeed true, but at the present time there is another note which may be present, and that is a feeling of thankfulness that, if these great trials were to come upon our Island, there is a generation of Britons here now ready to prove itself not unworthy of the days of yore and not unworthy of those great men, the fathers of our land, who laid the foundations of our laws and shaped the greatness of our country." 
texte=extract_words(string)
lexi0=initial_lexical(texte)

# In[221]: MDL CHunker

stimuli=['123','123','45','12345','45','45','123','45','12345']
#lexi0=initial_lexical(stimuli)
lexi0=['1','2','3','4','5','6']

def MDL(stimuli,lexi0,a,b):
    
    S_C,C=initialisation(stimuli,lexi0)
    
    S_C,C,TOTAL=introduce_new_word(a,b,S_C,C)
    print(C)

    return TOTAL,C

TOTAL,C=MDL(stimuli,lexi0,3,4)

# In[235]: Mise à jour codelenghts
def update_codelengths(S_C,C):
    TOTAL=0 #Cout total du S_C et C
    ELTS=0 #Nombre d'éléments dans S_C et C
    for word in S_C:
        ELTS+=len(word) #compte le nombre d'éléments dans S_C
    for word in C:
        ELTS+=len(word['detail']) #compte le nombre d'éléments dans 
  #  print('number of chunks in S|C and C = ',ELTS)
  
    DETAIL=[dic['detail'] for dic in C]
    print(DETAIL)
    WORDS=[dic['word'] for dic in C]

    i=-1
    for chunk in WORDS: 
        i+=1
        comptSC=countStringOccurence(S_C,chunk)
        comptC=countStringOccurence(DETAIL,chunk)

        #print('Chunk',chunk,':',comptSC,'times in S|C',';',comptC,'times in C')
        
        C[i]['codelenght']=-comptC*np.log2((comptC+comptSC)/(ELTS))
        TOTAL+=-(comptC+comptSC)*np.log2((comptC+comptSC)/(ELTS))
   # print('Updated Chunk =',C)
    #print(TOTAL)
    return C,TOTAL

# In[ ]:
def initialisation(stimuli,lexi):
    #Initialisation Stimuli|Chunk
    S_C=stimuli[:]
    for i in range(0,len(stimuli)):
        S_C[i]=cutting(stimuli[i],lexi)
    
    #Initialisation Chunk
    C=lexi[:]
    for i in range(0,len(lexi)):
        C[i]={}
        C[i]['word']=lexi[i]
        C[i]['detail']=[lexi[i]]
    
    C,TOTAL=update_codelengths(S_C,C)

    return S_C,C




# In[ ]:

def introduce_new_word(a,b,S_C,C):
    new_word=C[a]['word']+C[b]['word']
    
    #Update C avec nouveau chunk
    C.append({'word':new_word,'detail':[new_word,C[a]['word'],C[b]['word']]})
    
    #Update S_C avec nouveau chunk
    C.reverse()
    for i in range(0,len(stimuli)):
        S_C[i]=cutting(stimuli[i],[dic['word'] for dic in C])
    C.reverse()
    
    #Udpate codelenghts
    C,TOTAL=update_codelengths(S_C,C)
    return(S_C,C,TOTAL)


# In[ ]: factorisation d'un seul stimuli
#def factorisation(stimuli,C):


# In[ ]:
def countStringOccurence(S_C,s):
    '''
    Nombre de fois ou le string s apparait dans tous les stimulis
    '''
    return sum([e.count(s) for e in S_C])


# In[ ]:
def counts(S_C):
    '''
    Renvoi un dictionnaire contenant le decompte de chaque motif
16         {"motif1": 25, "motif2": 30}

'''
    return functools.reduce(lambda x,y: x+y, map(Counter,S_C))
    

# In[ ]:
    #Algo de recherche exhaustif:
def search(C,stimuli):
    LEXI=[dic['word'] for dic in C]
    best_mdl=1000
    for a in range(0,len(LEXI)):
        for b in range(0,len(LEXI)):
            mdl,C_mdl=MDL(stimuli,LEXI,a,b)
            if mdl<=best_mdl:
                best_mdl=mdl
                best_a=LEXI[a]
                best_b=LEXI[b]
                best_C=C_mdl
    return best_C,best_mdl, best_a, best_b



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
    n=len(C)    #nombre de chunks
    Sk=[sum([len(diffS_C[i])==k for i in range(len(diffS_C))]) for k in range(1,maxLen+1)]   #contien le nombre de mots de longueur k
    return (1/nbDiffS_C)*sum([Sk[k-1]*proba(k,n) for k in range(1,maxLen+1)])

#pseudo-score d'un chunk dans la liste réduite S_C = 'bonne' distribution
# on ajoute 1 s'il est présent au moins une fois dans le mot
def distribScore(newChunk,S_C): #utiliser C et C[-1] ?
    score=0
    diffS_C, nbDiffS_C,maxLen=reducedStimuli(S_C)
    return (1/nbDiffS_C)*sum([newChunk in s_c for s_c in diffS_C])

#critère pour garder un nouveau chunk qui vient d'être proposé
def addChunkCrit(newChunk,S_C,C): #remplacer newChunk par C[-1] ?
    diffS_C, nbDiffS_C,maxLen=reducedStimuli(S_C)
    threshold=aleaDistrib_Score(S_C,C)
    return threshold < distribScore(newChunk,S_C)



"""fin partie Jordan 10/11"""
# In[ ]:


def MDLChunker(lexi0,stimuli):
    S_C,C=initialisation(stimuli,lexi0)
    C,TOTAL=update_codelengths(S_C,C)
    end_mdl=TOTAL
    
    best_C,best_mdl, best_a, best_b=search(C,stimuli)
    
    while best_mdl<end_mdl:
        end_mdl=best_mdl
        C=best_C
        best_C,best_mdl, best_a, best_b=search(C,stimuli)

    return C,TOTAL,end_mdl

#MDLChunker(lexi0,stimuli)