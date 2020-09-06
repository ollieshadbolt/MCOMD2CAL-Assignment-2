from itertools import chain, combinations


def powerset(iterable):
    """ https://docs.python.org/2/library/itertools.html#recipes
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def countFacts(facts):
    count = 0
    for fact in facts:
        if facts[fact] is not None:
            count += 1
    return count


def printFacts(facts):
    for fact in facts:
        print("{0} is {1}".format(fact, facts[fact]))


def getAntecedents(facts):
    """ Returns all facts which are antecedent.
    """
    # Get a list of all fact combinations
    factSets = []
    for _set in list(powerset(facts)):
        _dict = {}
        for fact in facts:
            _dict[fact] = fact in _set
        factSets.append(_dict)

    # Check if each fact is consequent
    consequentFacts = []
    for fact in facts:
        for _set in factSets:
            _setCopy = _set.copy()
            infer(_setCopy)
            if _set[fact] is not _setCopy[fact]:
                consequentFacts.append(fact)
                break

    # Yield the results
    for fact in facts:
        if fact not in consequentFacts:
            yield fact


class KnowledgeBase:
    def ruleA(self, facts):
        # FACTS.weatherIsCold ? FACTS.winterTime = true
        # : FACTS.summerTime = true;
        """ The ordering of the top two rules was swapped, as one rule's results
        could have a direct influence on how the next rule is run. Swapping
        these potentially reduces the number of iterations.
        """
        if facts['weatherIsCold'] is True:
            facts['winterTime'] = True
        else:
            facts['summerTime'] = True

    def ruleB(self, facts):
        # FACTS.winterTime ? FACTS.wearCoat = true : FACTS.wearCoat = false;
        if facts['winterTime'] is True:
            facts['wearCoat'] = True
        else:
            facts['wearCoat'] = False

    def ruleC(self, facts):
        # FACTS.itsRaining ? FACTS.darkClouds = true
        # : FACTS.sunIsShining = false;
        # FACTS.itsRaining ? FACTS.openUmbrella = true
        # : FACTS.openUmbrella = false;
        """ As both rules checked for the same condition, the results can be
        combined with the same condition to make a single rule with the same
        functionality.
        """
        if facts['itsRaining'] is True:
            facts['darkClouds'] = True
            facts['openUmbrella'] = True
        else:
            facts['sunIsShining'] = False
            facts['openUmbrella'] = False

    def ruleD(self, facts):
        # (FACTS.sunIsShining && FACTS.summerTime)
        # ? FACTS.wearSunGlasses = true : FACTS.wearSunGlasses = false;
        if facts['sunIsShining'] is True and facts['summerTime'] is True:
            facts['wearSunGlasses'] = True
        else:
            facts['wearSunGlasses'] = False

    def ruleE(self, facts):
        # (FACTS.sunIsShining && FACTS.winterTime)
        # ? FACTS.wearSunGlasses = false : FACTS.darkClouds = false ;
        if facts['sunIsShining'] is True and facts['winterTime'] is True:
            facts['wearSunGlasses'] = False
        else:
            facts['darkClouds'] = False

    def ruleF(self, facts):
        # FACTS.summerTime ? FACTS.weatherIsHot = true
        # : FACTS.weatherIsHot = false;
        if facts['summerTime'] is True:
            facts['weatherIsHot'] = True
        else:
            facts['weatherIsHot'] = False


def infer(facts):
    knowledgeBase = KnowledgeBase()
    while True:
        numberOfFacts = countFacts(facts)
        knowledgeBase.ruleA(facts)
        knowledgeBase.ruleB(facts)
        knowledgeBase.ruleC(facts)
        knowledgeBase.ruleD(facts)
        knowledgeBase.ruleE(facts)
        knowledgeBase.ruleF(facts)
        if numberOfFacts is countFacts(facts):
            break


def main():
    facts = {
        'sunIsShining': False,
        'weatherIsHot': False,
        'weatherIsCold': False,
        'wearSunGlasses': False,
        'summerTime': False,
        'winterTime': False,
        'darkClouds': False,
        'itsRaining': False,
        'openUmbrella': False,
        'wearCoat': False,
    }

    for antecedent in getAntecedents(facts):
        while True:
            _input = input(antecedent + " [Y/n]: ").lower()
            if _input == 'y':
                facts[antecedent] = True
                break
            elif _input == 'n':
                facts[antecedent] = False
                break

    infer(facts)
    printFacts(facts)


if __name__ == '__main__':
    main()
