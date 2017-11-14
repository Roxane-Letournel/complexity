# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:29:31 2017

@author: roxan
"""
import MDLChunker_v2
import optimization
import fonctions_aux
import distribution
import factorizer

# In[ ]:  
'''Test de l'article'''
texte=['123','123','45','12345','45','45','123','45','12345']
lexi0=['1','2','3','4','5','6']    

print(MDLChunker_optimized_factorized(texte))

# In[ ]: 
'''Pour comparer avec un mot unique'''
all_stimuli=texte[:]
all_stimuli_in_one=''.join(all_stimuli)
all_stimuli_in_one=[all_stimuli_in_one]
lexi0=initial_lexical(all_stimuli)

print(MDLChunker_optimized_factorized(all_stimuli_in_one))
# In[109]: 
'''Si l'entrée est un texte quelconque'''
string="In this solemn hour it is a consolation to recall and to dwell upon our repeated efforts for peace. All have been ill-starred, but all have been faithful and sincere. This is of the highest moral value--and not only moral value, but practical value--at the present time, because the wholehearted concurrence of scores of millions of men and women, whose co-operation is indispensable and whose comradeship and brotherhood are indispensable, is the only foundation upon which the trial and tribulation of modern war can be endured and surmounted. This moral conviction alone affords that ever-fresh resilience which renews the strength and energy of people in long, doubtful and dark days. Outside, the storms of war may blow and the lands may be lashed with the fury of its gales, but in our own hearts this Sunday morning there is peace. Our hands may be active, but our consciences are at rest. We must not underrate the gravity of the task which lies before us or the temerity of the ordeal, to which we shall not be found unequal. We must expect many disappointments, and many unpleasant surprises, but we may be sure that the task which we have freely accepted is one not beyond the compass and the strength of the British Empire and the French Republic. The Prime Minister said it was a sad day, and that is indeed true, but at the present time there is another note which may be present, and that is a feeling of thankfulness that, if these great trials were to come upon our Island, there is a generation of Britons here now ready to prove itself not unworthy of the days of yore and not unworthy of those great men, the fathers of our land, who laid the foundations of our laws and shaped the greatness of our country." 
all_stimuli=extract_words(string)
lexi0=initial_lexical(all_stimuli)

print(MDLChunker_optimized_factorized(all_stimuli))