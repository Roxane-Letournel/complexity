
class Factorizer:

    def __init__(self, chunks):
        self.chunks = sorted(chunks, key=lambda t: len(t['word']), reverse=True) # largest strings first
        self.bestCost = -1
        self.bestFact = []
        self.toDo = []

    def setChunks(self, newChunks):
        self.chunks = sorted(newChunks, key=lambda t: len(t['word']), reverse=True) # largest strings first
        self.bestCost = -1
        self.bestFact = []
        self.toDo = []

    def getBestFact(self):
        return self.bestFact
        
    def fastFactorize(self, stimulus):
        self.bestCost = 0
        residual = stimulus
        while(len(residual)!=0):
            previousResidual = residual
            for chunk in self.chunks:
                if chunk['word'] == residual[:min(len(residual),len(chunk['word']))]: 
                    self.bestCost += chunk['codelength']
                    self.bestFact += [chunk['word']]
                    residual = residual[len(chunk['word']):]
                    break
            if residual and previousResidual == residual:
                raise NameError("Can't factorize: C is incomplete (missing canonical chunks)")

    def factorize(self, stimulus):

        # first fast factorization to cut branches faster later
        if (self.bestCost < 0):
            self.fastFactorize(stimulus)

        # initializing toDo tasks list
        usedChunks = []
        currentCost = 0
        self.toDo += [(stimulus, usedChunks, currentCost)]

        # exploring possibilities
        while self.toDo:
            residual, usedChunks, currentCost = self.toDo.pop()
            for chunk in self.chunks:
                if residual and chunk['word'] == residual[:min(len(residual),len(chunk['word']))]:
                    currentCost_temp = currentCost + chunk['codelength']
                    if currentCost_temp < self.bestCost:
                        residual_temp = str(residual[len(chunk['word']):])
                        usedChunks_temp = list(usedChunks) + [chunk['word']]
                        if not residual_temp: 
                            if currentCost_temp < self.bestCost:
                                self.bestCost = currentCost_temp
                                self.bestFact = usedChunks_temp
                        else:
                            self.toDo += [(residual_temp, list(usedChunks_temp), currentCost_temp)]


if __name__ == '__main__':

    """
    C = [
    {'word': "aaaa", 'codelength':3},
    {'word': "a", 'codelength':5}, 
    {'word': "b", 'codelength':10}, 
    {'word': "c", 'codelength':7}, 
    {'word': "aab", 'codelength':1},
    {'word': "cc", 'codelength':4}
    ]

    stimulus = "accaaabaacaa"

    print("initialise Factorizer")
    fact = Factorizer(C)
    fact.factorize(stimulus)

    print("C = ", C)
    print("stimulus = ", stimulus)
    print("Factorization = ", fact.bestFact, " (cost: ", fact.bestCost, ")")

    """

    C = [{'word': 'a', 'detail': ['a'], 'codelength': 5.6234073537484237}, 
    {'word': 'b', 'detail': ['b'], 'codelength': 3.4594316186372973}, 
    {'word': 'aa', 'detail': ['aa', 'a', 'a'], 'codelength': 0.65207669657969314}]


    stimulus = "aaaa"

    print("initialise Factorizer")
    fact = Factorizer(C)
    fact.factorize(stimulus)

    print("C = ", C)
    print("stimulus = ", stimulus)
    print("Factorization = ", fact.bestFact, " (cost: ", fact.bestCost, ")")
