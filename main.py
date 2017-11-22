from MDLChunker import MDLChunker_search_factorized_distribution as mdla
from MDLChunker import MDLChunker_search_factorized as mdl
from fonctions_aux import extract_words


print('\n****** Exemple 1 ******')
string = "blablabla blablabla"
alpha = 1.
all_stimuli = extract_words(string)
C, S_C, TOTAL = mdla(all_stimuli, alpha)
print("\nstring = ", string)
print("alpha = ", alpha)
print("C =  ", C)
print("S_C =  ", S_C)
print("TOTAL =  ", TOTAL)


print('\n****** Exemple 2 ******')
string = "clakjo kjo kjo kjoclakjo kjoclakjokjo clakjocla kjo cla claclakjo clacla"
alpha = 1.
all_stimuli = extract_words(string)
C, S_C, TOTAL = mdla(all_stimuli, alpha)
print("\nstring = ", string)
print("alpha = ", alpha)
print("C =  ", C)
print("S_C =  ", S_C)
print("TOTAL =  ", TOTAL)


print('\n****** Exemple 3 ******')
string = "In this solemn hour it is a consolation to recall and to dwell upon our repeated efforts for peace. All have been ill-starred, but all have been faithful and sincere. This is of the highest moral value--and not only moral value, but practical value--at the present time, because the wholehearted concurrence of scores of millions of men and women, whose co-operation is indispensable and whose comradeship and brotherhood are indispensable, is the only foundation upon which the trial and tribulation of modern war can be endured and surmounted. This moral conviction alone affords that ever-fresh resilience which renews the strength and energy of people in long, doubtful and dark days. Outside, the storms of war may blow and the lands may be lashed with the fury of its gales, but in our own hearts this Sunday morning there is peace. Our hands may be active, but our consciences are at rest. We must not underrate the gravity of the task which lies before us or the temerity of the ordeal, to which we shall not be found unequal. We must expect many disappointments, and many unpleasant surprises, but we may be sure that the task which we have freely accepted is one not beyond the compass and the strength of the British Empire and the French Republic. The Prime Minister said it was a sad day, and that is indeed true, but at the present time there is another note which may be present, and that is a feeling of thankfulness that, if these great trials were to come upon our Island, there is a generation of Britons here now ready to prove itself not unworthy of the days of yore and not unworthy of those great men, the fathers of our land, who laid the foundations of our laws and shaped the greatness of our country."
alpha = .0
all_stimuli = extract_words(string)
C, S_C, TOTAL = mdla(all_stimuli, alpha)
print("\nstring = ", string)
print("alpha = ", alpha)
print("C =  ", C)
print("S_C =  ", S_C)
print("TOTAL =  ", TOTAL)