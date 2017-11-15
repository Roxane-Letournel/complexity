# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:31:59 2017

@author: roxan
"""
import numpy as np

import sys

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
    

# In[107]: Traitement du string initial

def extract_words(string):
    string=string.replace('.','')
    string=string.replace(',','')
    string=string.replace('?',' ')
    string=string.replace(':','')
    string=string.replace('!','')
    string=string.replace('-','')
    string=string.lower()
    texte=string.split(' ')
    return texte


# In[108]: Définir lexique initial "canonical chunks"

def initial_lexical(texte):
    lexi=[]
    for string in texte:
        for i in range(len(string)):
            if string[i] not in lexi:
                lexi.append(string[i])
    return lexi
