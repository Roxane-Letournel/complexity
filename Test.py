# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 11:29:31 2017

@author: roxan
"""

from MDLChunker import *

from fonctions_aux import *
import factorizer

import matplotlib.pylab as plt


# In[ ]:
'''Test de l'article'''
texte = ['123', '123', '45', '12345', '45', '45', '123', '45', '12345']
lexi0 = ['1', '2', '3', '4', '5', '6']

# print(MDLChunker_optimized_factorized(texte))

# In[109]:
'''Si l'entrée est un texte quelconque'''
string = "In this solemn hour it is a consolation to recall and to dwell upon our repeated efforts for peace. All have been ill-starred, but all have been faithful and sincere. This is of the highest moral value--and not only moral value, but practical value--at the present time, because the wholehearted concurrence of scores of millions of men and women, whose co-operation is indispensable and whose comradeship and brotherhood are indispensable, is the only foundation upon which the trial and tribulation of modern war can be endured and surmounted. This moral conviction alone affords that ever-fresh resilience which renews the strength and energy of people in long, doubtful and dark days. Outside, the storms of war may blow and the lands may be lashed with the fury of its gales, but in our own hearts this Sunday morning there is peace. Our hands may be active, but our consciences are at rest. We must not underrate the gravity of the task which lies before us or the temerity of the ordeal, to which we shall not be found unequal. We must expect many disappointments, and many unpleasant surprises, but we may be sure that the task which we have freely accepted is one not beyond the compass and the strength of the British Empire and the French Republic. The Prime Minister said it was a sad day, and that is indeed true, but at the present time there is another note which may be present, and that is a feeling of thankfulness that, if these great trials were to come upon our Island, there is a generation of Britons here now ready to prove itself not unworthy of the days of yore and not unworthy of those great men, the fathers of our land, who laid the foundations of our laws and shaped the greatness of our country."


# In[109]:
string = 10 * '·− ·− −··· −··· −··· ·− −··· ·− −··· −··· ·− ·− −··· −··· ·− ·− −··· '

#string=10*'·− −··· ·− −··· ·− −··· ·− −···  ·− −··· ·− −··· ·−  ·− ·− −··· −···  ·− −··· −··· −··· ·−  ·− ·− ·− −··· −··· −···  −··· −··· −··· ·− ·− ·−  ·− ·− ·− −··· −··· −···  ·− −··· −··· ·−  ·− −··· −···  ·−  −··· −···  ·− ·− ·− −···  ·− ·− −···  '

# In[109]:
string = 20 * '−− −−− − ···  · −  −− · ·−· ···− · ·· ·−·· ·−·· · ···  −·· ·−−−−· ·· −·−· ··  · −  −·· ·−−−−· ·− ·· ·−·· ·−·· · ··− ·−· ··· '
#string=10*'ABABABAB ABABA AABB ABBBA AAABBB BBBAAA AAABBB ABBA ABB A BB AAAB AAB '

#string=10*'A B A B A B A B   A B A B A   A A B B   A B B B A   A A A B B B   B B B A A A   A A A B B B   A B B A   A B B   A   B B   A A A B   A A B'
# In[109]:
string = 3 * 'un chasseur sachant chasser sans son chien est un bon chasseur '
string = 50 * '··− −·  −·−· ···· ·− ··· ··· · ··− ·−·  ··· ·− −·−· ···· ·− −· −  −·−· ···· ·− ··· ··· · ·−·  ··· ·− −· ···  ··· −−− −·  −·−· ···· ·· · −·  · ··· −  ··− −·  −··· −−− −·  −·−· ···· ·− ··· ··· · ··− ·−· '
# In[109]:
string = '123 123 44 12344 44 44 123 44 12344 44 44'
string = 10 * 'all dwell ill hyll moll hull '

# In[109]:
string = 10 * 'aabbcbbaa baaaabbcb bcbbaaaab '  # bonne langue
# In[109]:
string = 10 * 'aabcabaab bcbbcbbcb baabacabaa '  # mauvaise langue

# In[109]:
string = 'Peter Piper picked a peck of pickled peppers\
A peck of pickled peppers Peter Piper picked\
If Peter Piper picked a peck of pickled peppers\
Where’s the peck of pickled peppers Peter Piper picked?\
Betty Botter bought some butter\
But she said the butter’s bitter\
If I put it in my batter, it will make my batter bitter\
But a bit of better butter will make my batter better\
So ‘twas better Betty Botter bought a bit of better butter\
How much wood would a woodchuck chuck if a woodchuck could chuck wood?\
He would chuck, he would, as much as he could, and chuck as much wood\
As a woodchuck would if a woodchuck could chuck wood\
She sells seashells by the seashore\
How can a clam cram in a clean cream can?\
I scream, you scream, we all scream for ice cream\
I saw Susie sitting in a shoeshine shop\
Susie works in a shoeshine shop. Where she shines she sits, and where she sits she shines'

# In[109]: Discours Churchill
string = 'In this solemn hour it is a consolation to recall and to dwell upon our repeated efforts for peace. All have been ill-starred, but all have been faithful and sincere. This is of the highest moral value--and not only moral value, but practical value--at the present time, because the wholehearted concurrence of scores of millions of men and women, whose co-operation is indispensable and whose comradeship and brotherhood are indispensable, is the only foundation upon which the trial and tribulation of modern war can be endured and surmounted. This moral conviction alone affords that ever-fresh resilience which renews the strength and energy of people in long, doubtful and dark days. Outside, the storms of war may blow and the lands may be lashed with the fury of its gales, but in our own hearts this Sunday morning there is peace. Our hands may be active, but our consciences are at rest.\
We must not underrate the gravity of the task which lies before us or the temerity of the ordeal, to which we shall not be found unequal. We must expect many disappointments, and many unpleasant surprises, but we may be sure that the task which we have freely accepted is one not beyond the compass and the strength of the British Empire and the French Republic. The Prime Minister said it was a sad day, and that is indeed true, but at the present time there is another note which may be present, and that is a feeling of thankfulness that, if these great trials were to come upon our Island, there is a generation of Britons here now ready to prove itself not unworthy of the days of yore and not unworthy of those great men, the fathers of our land, who laid the foundations of our laws and shaped the greatness of our country.\
This is not a question of fighting for Danzig or fighting for Poland. We are fighting to save the whole world from the pestilence of Nazi tyranny and in defense of all that is most sacred to man. This is no war of domination or imperial aggrandizement or material gain; no war to shut any country out of its sunlight and means of progress. It is a war, viewed in its inherent quality, to establish, on impregnable rocks, the rights of the individual, and it is a war to establish and revive the stature of man. Perhaps it might seem a paradox that a war undertaken in the name of liberty and right should require, as a necessary part of its processes, the surrender for the time being of so many of the dearly valued liberties and rights. In these last few days the House of Commons has been voting dozens of Bills which hand over to the executive our most dearly valued traditional liberties. We are sure that these liberties will be in hands which will not abuse them, which will use them for no class or party interests, which will cherish and guard them, and we look forward to the day, surely and confidently we look forward to the day, when our liberties and rights will be restored to us, and when we shall be able to share them with the peoples to whom such blessings are unknown.'

# In[109]: Discours ML King
string = 'Let us not wallow in the valley of despair, I say to you today, my friends.\
And so even though we face the difficulties of today and tomorrow, I still have a dream. It is a dream deeply rooted in the American dream.\
I have a dream that one day this nation will rise up and live out the true meaning of its creed: We hold these truths to be self-evident, that all men are created equal.\
I have a dream that one day on the red hills of Georgia, the sons of former slaves and the sons of former slave owners will be able to sit down together at the table of brotherhood.\
I have a dream that one day even the state of Mississippi, a state sweltering with the heat of injustice, sweltering with the heat of oppression, will be transformed into an oasis of freedom and justice.\
I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.\
I have a dream today!\
I have a dream that one day, down in Alabama, with its vicious racists, with its governor having his lips dripping with the words of interposition and nullification one day right there in Alabama little black boys and black girls will be able to join hands with little white boys and white girls as sisters and brothers.\
I have a dream today!\
I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight and the glory of the Lord shall be revealed and all flesh shall see it together.'
# In[109]:
all_stimuli = extract_words(string)
lexi0 = initial_lexical(all_stimuli)
init = initialisationTOTAL(all_stimuli, lexi0)[-1]
print('Codelength with canonical chunks only =', init)
print(' ')


print('Sans distribution')
C, S_C, TOTAL0 = MDLChunker_search_factorized_distribution(all_stimuli, 0)
print('Chunks :', [dic['word'] for dic in C])
#print('Stimuli|Chunk :',S_C)
print('Final codelength =', TOTAL0)
print(' ')

C, S_C, TOTAL1 = MDLChunker_search_factorized_distribution(all_stimuli, 1)
print('Avec distribution')
print('Chunks :', [dic['word'] for dic in C])
#print('Stimuli|Chunk :',S_C)
print('Final codelength =', TOTAL1)
print(' ')
# In[109]:
nb_points = 3
x = np.linspace(0, 1, nb_points)

TOT = [TOTAL0]
C = [
    'i',
    'n',
    't',
    'h',
    's',
    'o',
    'l',
    'e',
    'm',
    'u',
    'r',
    'a',
    'c',
    'd',
    'w',
    'p',
    'f',
    'v',
    'b',
    'g',
    'y',
    'k',
    'q',
    'x',
    'z',
    ';',
    'nd',
    'th',
    'on',
    'and',
    'al',
    'en',
    'the',
    'of',
    'wh',
    'is',
    're',
    'ou',
    'our',
    'or',
    'no',
    'not',
    'at',
    'in',
    'ion',
    'ation',
    'that',
    'this',
    'be',
    'bu',
    'but',
    'ing',
    'bl',
    'gh',
    'igh',
    'ight',
    'an',
    'it',
    'whi',
    'whic',
    'which',
    'for',
    'who',
    'ar',
    'war',
    'ay',
    'abl',
    'to']
for alpha in x[1:-1]:
    new_C, new_S_C, new_TOTAL = MDLChunker_search_factorized_distribution(
        all_stimuli, alpha)
    TOT.append(new_TOTAL)
    C.append(new_C)

y = [init / TOTAL0] + [init / TOT[i]
                       for i in range(1, nb_points)] + [init / TOTAL1]
# In[109]:
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('alpha')
ax.set_ylabel('Compression ratio')
plt.scatter(x, y)
plt.show()
print(y)
# all_stimuli_in_one=''.join(all_stimuli)
# all_stimuli_in_one=[all_stimuli_in_one]
#print('Un seul mot')
# C,S_C,TOTAL=MDLChunker_search_factorized(all_stimuli_in_one)
##print('Chunks :',[dic['word'] for dic in C])
##print('Stimuli|Chunk :',S_C)
#print('Final codelength =',TOTAL)
