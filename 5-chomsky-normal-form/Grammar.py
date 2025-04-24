class Grammar:
    def __init__(self):
        # default grammar from variant
        self.default_P = {
            'S': ['bA', 'B'],
            'A': ['a', 'aS', 'bAaAb'],
            'B': ['AC', 'bS', 'aAa'],
            'C': ['epsilon', 'AB'],
            'E': ['BA']
        }
        self.default_V_N = ['S', 'A', 'B', 'C', 'E']
        self.default_V_T = ['a', 'b']
        
        # start with default values
        self.P = self.default_P.copy()
        self.V_N = self.default_V_N.copy()
        self.V_T = self.default_V_T.copy()

    def set_custom_grammar(self, P, V_N, V_T):
        # set custom grammar rules with validation
        if not self._validate_grammar(P, V_N, V_T):
            return False
        
        self.P = P
        self.V_N = V_N
        self.V_T = V_T
        return True

    def _validate_grammar(self, P, V_N, V_T):
        # check if all non-terminals in P are in V_N
        for nt in P.keys():
            if nt not in V_N:
                return False
        
        # check if all symbols in productions are either in V_N or V_T
        for productions in P.values():
            for prod in productions:
                for symbol in prod:
                    if symbol not in V_N and symbol not in V_T and symbol != 'epsilon':
                        return False
        
        return True

    def reset_to_default(self):
        # reset to default grammar
        self.P = self.default_P.copy()
        self.V_N = self.default_V_N.copy()
        self.V_T = self.default_V_T.copy()

    def elim_epsilon(self):
        nt_epsilon = []
        for key, value in self.P.items():
            s = key
            productions = value
            for p in productions:
                if p == 'epsilon':
                    nt_epsilon.append(s)

        for key, value in self.P.items():
            for ep in nt_epsilon:
                for v in value:
                    prod_copy = v
                    if ep in prod_copy:
                        for c in prod_copy:
                            if c == ep:
                                value.append(prod_copy.replace(c, ''))

        P1 = self.P.copy()
        for key, value in self.P.items():
            if key in nt_epsilon and len(value) < 2:
                del P1[key]
            else:
                for v in value:
                    if v == 'epsilon':
                        P1[key].remove(v)

        print(f"1. eliminating epsilon productions:")
        for key, value in P1.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P1.copy()
        return P1

    def elim_unit_prod(self):
        P2 = self.P.copy()
        for key, value in self.P.items():
            for v in value:
                if len(v) == 1 and v in self.V_N:
                    P2[key].remove(v)
                    for p in self.P[v]:
                        P2[key].append(p)
        print(f"2. eliminating unit productions:")
        for key, value in P2.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P2.copy()
        return P2

    def elim_inaccesible_symb(self):
        P3 = self.P.copy()
        accesible_symbols = self.V_N
        for key, value in self.P.items():
            for v in value:
                for s in v:
                    if s in accesible_symbols:
                        accesible_symbols.remove(s)

        for el in accesible_symbols:
            del P3[el]

        print(f"3. eliminating inaccessible symbols:")
        for key, value in P3.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P3.copy()
        return P3

    def elin_unnprod_symb(self):
        P4 = self.P.copy()
        productive = set()
        
        # find all productive symbols
        for key, value in self.P.items():
            for v in value:
                if len(v) == 1 and v in self.V_T:
                    productive.add(key)
                    break
        
        # find symbols that can produce productive symbols
        changed = True
        while changed:
            changed = False
            for key, value in self.P.items():
                if key not in productive:
                    for v in value:
                        if all(c in productive or c in self.V_T for c in v):
                            productive.add(key)
                            changed = True
                            break
        
        # remove unproductive symbols
        for key in list(P4.keys()):
            if key not in productive:
                del P4[key]
        
        # remove productions with unproductive symbols
        for key in list(P4.keys()):
            P4[key] = [v for v in P4[key] if all(c in productive or c in self.V_T for c in v)]

        print(f"4. eliminating unproductive symbols:")
        for key, value in P4.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        self.P = P4.copy()
        return P4

    def transf_to_cnf(self):
        P5 = self.P.copy()
        temp = {}
        vocabulary = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                      'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        free_symbols = [v for v in vocabulary if v not in self.P.keys()]
        for key, value in self.P.items():
            for v in value:
                if (len(v) == 1 and v in self.V_T) or (len(v) == 2 and v.isupper()):
                    continue
                else:
                    left = v[:len(v) // 2]
                    right = v[len(v) // 2:]
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

                    P5[key] = [temp_key1 + temp_key2 if item == v else item for item in P5[key]]

        for key, value in temp.items():
            P5[key] = [value]

        print(f"5. obtain chomsky normal form(cnf):")
        for key, value in P5.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        return P5

    def ReturnProductions(self):
        print(f"initial grammar:")
        for key, value in self.P.items():
            print(f"{key} -> {' | '.join(value)}")
        print("------------------------------------------------")
        P1 = self.elim_epsilon()
        P2 = self.elim_unit_prod()
        P3 = self.elim_inaccesible_symb()
        P4 = self.elin_unnprod_symb()
        P5 = self.transf_to_cnf()
        return P1, P2, P3, P4, P5

if __name__ == "__main__":
    g = Grammar()
    P1, P2, P3, P4, P5 = g.ReturnProductions() 