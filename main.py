from MDLChunker import MDLChunker_search_factorized_distribution as mdla
from optimization import lexi


stimulis = ""
with open('data.txt', 'r') as myfile:
        stimulis = myfile.read().replace('\n', '')




C, S_C, total = mdla(stimulis[1:200], 1)
print(lexi(S_C))
