from MDLChunker import MDLChunker_search_factorized_distribution as mdla
from MDLChunker import MDLChunker_search_factorized as mdl
from fonctions_aux import extract_words

"""
    string = "aaa aaabbb bbbaaabbb bbb bbb aaabbb bbbbbbaaa bbbaaaaaabbb aaa bbb \
    aaabbb bbbaaa aaaaaa bbbaaa aaa aaabbb bbbaaabbb bbb bbb aaabbb bbbbbbaaa \
    bbbaaaaaabbb aaa bbb aaabbb bbbaaa aaaaaa bbbaaa"
    """

#string = "blablabla blablabla"

string = "clakjo kjo kjo kjoclakjo kjoclakjokjo clakjocla kjo cla claclakjo clacla"

alpha = 1.

all_stimuli = extract_words(string)

C, S_C, TOTAL = mdla(all_stimuli, alpha)
#C, S_C, TOTAL = mdl(all_stimuli)

print("\nstring = ", string)
print("alpha = ", alpha)
print("\nC =  ", C)
print("\nS_C =  ", S_C)
print("\nTOTAL =  ", TOTAL)
