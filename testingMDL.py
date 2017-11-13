
from optimization import Optimizer
from factorization import Factorizer


print("*** initialise Optimizer ***")

opt = Optimizer()
s = ["aab aaab abba baab"]
s_c = [["c", "a", "b"], ["a", "c", "a", "b"], ["a", "b", "c", "c"],
       ["b", "c", "a", "b"], ['a', 'b'], ['a', 'b']]
c = [{"word": "a", "detail": ["a"]}, {"word": "b", "detail": ["b"]},
     {"word": "c", "detail": ["c"]}]
print(opt.optimize(s_c, c))


print("*** initialise Factorizer ***")

C = [
{'word': "aaaa", 'codelength':3},
{'word': "a", 'codelength':5}, 
{'word': "b", 'codelength':10}, 
{'word': "c", 'codelength':7}, 
{'word': "aab", 'codelength':1},
{'word': "cc", 'codelength':4}
]

stimulus = "accaaabaacaa"

fact = Factorizer(C)
fact.factorize(stimulus)

print("C = ", C)
print("stimulus = ", stimulus)
print("Factorization = ", fact.bestFact, " (cost: ", fact.bestCost, ")")