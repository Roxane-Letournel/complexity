
# coding: utf-8

import numpy as np

import sys

import time

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


# In[103]: calcule la factorielle de n (entier >= 0)

def fact(n):
    
    if n<2:
        return 1
    else:
        return n*fact(n-1)
 

# In[104]: trouve la complexité d'un texte sachant un lexique

def find_complexity(texte,lexi):
    union=[]
    for word in texte:
        complexity=0
        union=union+cutting(word,lexi)
    
    for syllab in lexi:
        nboccur=0
        for i in range(0,len(union)):
            if union[i]==syllab:
                nboccur+=1
            
        if nboccur!=0:
            #print('syllabe :',syllab,'apparition =',nboccur,'complexité =',nboccur*np.log2(nboccur/len(union)))
            complexity=complexity-nboccur*np.log2(nboccur/len(union))
    return(complexity)


# In[105]: première fonction pour proposer un nouveau lexique de longueur de syllabes <=nb

def concatenate(lexi,nb):
    new_lexi=lexi
    for i in range(0,len(lexi)-1):
        for j in range(i+1,len(lexi)):
            if lexi[i]!=lexi[j]:
                new_word1=lexi[i]+lexi[j]
                new_word2=lexi[j]+lexi[i]
                if new_word1 not in new_lexi and len(new_word1)<=nb:
                    new_lexi=new_lexi+[new_word1]
                if new_word2 not in new_lexi and len(new_word2)<=nb:
                    new_lexi=new_lexi+[new_word2]
    return new_lexi


# In[110]: Propose un nouveau lexique 

def new_lexical(lexi0,best_lexical):
    lexi=best_lexical+lexi0
    lexi=list(set(lexi))
    lexi=sorted(lexi, key=len)
    lexi.reverse()
    return lexi

# In[106]: Code principal 1ère version

def find_best_lexical(lexi,texte,nb):

    # Liste des syllabes qu'on envisage de rajouter au lexique 
    potential=lexi  
    for k in range(1,2):
        potential=concatenate(potential,nb)

    cost_lex=0 #Coût du lexique

    # on initialise : complexité pour le lexique initial

    cost_text=find_complexity(texte,lexi)
    total_cost=cost_text+cost_lex
    print('Initial complexity =',cost_text)
    print(' ')
    i=0
    temps1=0
    temps2=0
    for candidate in potential:
        i=i+1
        print(i/len(potential)*100,'%',',','temps restant =',(temps2-temps1)*(len(potential)-i))
        temps1=time.clock()
        lexi1=[candidate]+lexi  #on ajoute une syllabe au lexique

        # calcul complexité avec cette syllabe ajoutée            
        cost_text1=find_complexity(texte,lexi1)
        #cost_lex1=cost_lex+3*np.log2(3)  # le coût du lexique augmente
        cost_lex1=0 # on ne tient pas compte de la pénalité du lexique
        

        if cost_text1+cost_lex1<cost_text+cost_lex:
            cost_text=cost_text1
            cost_lex=cost_lex1
            lexi=lexi1  # si la complexité a été diminuée, la syllabe est effectivement ajoutée au lexique
           # word=candidate # si la complexité a été diminuée, on retient en mémoire le best cost et on teste les autres
        temps2=time.clock()
        
#Supprimer les mots du lexiques inutiles
    union=[]
    for word in texte:
        complexity=0
        union=union+cutting(word,lexi)
        

    compteur=[]
    for word in lexi:
        k=union.count(word)
        compteur.append(k)
    
    lexi_used=lexi[:]
    
    for i in range(0,len(lexi)):
        if compteur[i]==0:
            lexi_used=[l for l in lexi_used if l != lexi[i]]
    print(compteur)
    compteur=[i for i in compteur if i != 0]
        
    print('Best lexical =',lexi_used)
    print("Compteurs =",compteur)
    print('Associated cost =',cost_text)

    return lexi_used



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
lexi0=['1','2','3','4','5','6']
lexi=lexi0[:]

#Initialisation Stimuli|Chunk
S_C=stimuli[:]
for i in range(0,len(stimuli)):
    S_C[i]=cutting(stimuli[i],lexi)
print('Initial Stimuli|Chunk =',S_C)
print(' ')

#Initialisation Chunk
C=lexi[:]
for i in range(0,len(lexi0)):
    bit=-C.count(lexi[i])*np.log2((C.count(lexi[i])+S_C.count(lexi[i]))/(len(S_C)+len(C)))
    C[i]={}
    C[i]['word']=lexi[i]
    C[i]['codelenght']=bit
    C[i]['detail']=[lexi[i]]
print('Initial Chunk =',C)
print(' ')

#search new factorisation --> lexi[3]+lexi[4]
new_word=lexi[3]+lexi[4]
lexi=lexi+[new_word]
C=C+[{'word': new_word, "detail": [new_word,lexi[3],lexi[4]]}]
print('New chunk =',C)
print(' ')

lexi.reverse()
for i in range(0,len(stimuli)):
    S_C[i]=cutting(stimuli[i],lexi)
print('Stimuli|Chunk after factorisation =',S_C)
print(' ')
lexi.reverse()

# In[235]:

TOTAL=0
COMP=0
for k in range(0,len(S_C)):
    COMP+=len(S_C[k])
for k in range(0,len(C)):
    COMP+=len(C[k]['detail'])
print(COMP)
for i in range(0,len(lexi)): #compteur du mot lexi[i]
    comptSC=0
    comptC=0
    for k in range(0,len(S_C)): #compteur du mot lexi[i] dans SC
        comptSC+=S_C[k].count(lexi[i])
    for k in range(0,len(C)):
        if lexi[i] in C[k]['detail']:
            comptC+=1
    print(lexi[i],comptSC,comptC)
    
    bit=-comptC*np.log2((comptC+comptSC)/(COMP))
    C[i]['codelenght']=bit
    TOTAL+=-(comptC+comptSC)*np.log2((comptC+comptSC)/(COMP))
print('Updated Chunk =',C)
print(TOTAL)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



