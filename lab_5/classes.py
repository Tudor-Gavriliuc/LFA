class Gramamr():
    def __init__(self):
        self.P = {
            'S': ['aB', 'DA'],
            'A': ['a', 'BD', 'bDAB'],
            'B': ['b', 'BA'],
            'D': ['eps', 'BA'],
            'C': ['BA']
        }
        self.V_N = ['S', 'A', 'B', 'D', 'C']
        self.V_T = ['a', 'b']

    def RemoveEpsilon(self):
        P1 = self.P.copy()
        eps_producers = [nt for nt, prods in P1.items() if 'eps' in prods]

        # Remove 'eps' from the productions of epsilon producers
        for nt in eps_producers:
            if 'eps' in P1[nt]:
                P1[nt].remove('eps')

        # Create new productions by removing epsilon-producing non-terminals from other productions
        for nt in eps_producers:
            for key, productions in list(P1.items()):  # use list to copy for safe iteration
                new_productions = []
                for prod in productions:
                    if nt in prod:
                        # Create a new production with the non-terminal removed
                        new_prod = prod.replace(nt, '')
                        if new_prod:  # Ensure it's not empty
                            new_productions.append(new_prod)
                if new_productions:
                    P1[key].extend(new_productions)
                    P1[key] = list(set(P1[key]))  # Remove duplicates

        print("Without epsilon productions:\n", P1)
        return P1

    def EliminateUnitProd(self):
        # 2. Eliminate any renaiming (unit productions)
        # new productions for next step
        P2 = self.P.copy()
        for key, value in self.P.items():
            # replace unit productions
            for v in value:
                if len(v) == 1 and v in self.V_N:
                    P2[key].remove(v)
                    for p in self.P[v]:
                        P2[key].append(p)
        print(f"Without unit productions:\n{P2}")
        self.P = P2.copy()
        return P2

    def EliminateInaccesible(self):
        # 3. Eliminate inaccesible symbols
        P3 = self.P.copy()
        accesible_symbols = self.V_N
        # find elements that are inaccesible
        for key, value in self.P.items():
            for v in value:
                for s in v:
                    if s in accesible_symbols:
                        accesible_symbols.remove(s)
        # remove inaccesible symbols
        for el in accesible_symbols:
            del P3[el]
        print(f"Without inaccesible symbols:\n{P3}")
        self.P = P3.copy()
        return P3

    def RemoveUnprod(self):
        P4 = self.P.copy()
        productive = set()

        # First identify all terminals and non-terminals that can lead directly to terminals
        for key, values in P4.items():
            for value in values:
                if all(c in self.V_T or c in productive for c in value):
                    productive.add(key)
                    break

        # Check in multiple passes as adding one productive symbol may make others productive
        changed = True
        while changed:
            changed = False
            for key, values in P4.items():
                if key not in productive:
                    for value in values:
                        if all(c in self.V_T or c in productive for c in value):
                            productive.add(key)
                            changed = True
                            break

        # Now remove unproductive symbols
        to_remove = [key for key in P4 if key not in productive]
        for key in to_remove:
            del P4[key]

        # Remove productions containing unproductive symbols
        for key in list(P4.keys()):
            P4[key] = [prod for prod in P4[key] if all(c in self.V_T or c in productive for c in prod)]
            if not P4[key]:  # If no productions left, remove the non-terminal
                del P4[key]

        print(f"Without unproductive symbols:\n{P4}")
        self.P = P4.copy()
        return P4

    def TransformToCNF(self):
        # 5. Obtain CNF
        P5 = self.P.copy()
        temp = {}

        # define a list of free symbols
        vocabulary = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                      'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        free_symbols = [v for v in vocabulary if v not in self.P.keys()]
        for key, value in self.P.items():
            for v in value:

                # check if oriduction satisfies CNF
                if (len(v) == 1 and v in self.V_T) or (len(v) == 2 and v.isupper()):
                    continue
                else:

                    # split production into two parts
                    left = v[:len(v) // 2]
                    right = v[len(v) // 2:]

                    # get the new symbols for each half
                    if left in temp.values():
                        temp_key1 = ''.join([i for i in temp.keys() if temp[i] == left])
                    else:
                        temp_key1 = free_symbols.pop(0)
                        temp[temp_key1] = left
                    if right in temp.values():
                        temp_key2 = ''.join([i for i in temp.keys() if temp[i] == right])
                    else:
                        temp_key2 = free_symbols.pop(0)
                        temp[temp_key2] = right

                    # replace the production with the new symbols
                    P5[key] = [temp_key1 + temp_key2 if item == v else item for item in P5[key]]

        # add new productions
        for key, value in temp.items():
            P5[key] = [value]

        print(f"5. Final CNF:\n{P5}")
        return P5

    def ReturnProductions(self):
        print(f"Initial Grammar:\n{self.P}")
        P1 = self.RemoveEpsilon()
        P2 = self.EliminateUnitProd()
        P3 = self.EliminateInaccesible()
        P4 = self.RemoveUnprod()
        P5 = self.TransformToCNF()
        return P1, P2, P3, P4, P5


if __name__ == "__main__":
    g = Gramamr()
    P1, P2, P3, P4, P5 = g.ReturnProductions()