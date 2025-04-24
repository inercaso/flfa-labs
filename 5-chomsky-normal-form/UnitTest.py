from Grammar import Grammar
import unittest


class TestGrammar(unittest.TestCase):
    def setUp(self):
        self.g = Grammar()
        self.P1, self.P2, self.P3, self.P4, self.P5 = self.g.ReturnProductions()

    def test_elim_epsilon(self):
        expected_result = {'S': ['bA', 'AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'A': ['a', 'aS', 'bAaAb'],
                           'B': ['AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'C': ['AB'],
                           'E': ['BA']
                           }
        self.assertEqual(self.P1, expected_result)

    def test_elim_unit_prod(self):
        expected_result = {'S': ['bA', 'AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'A': ['a', 'aS', 'bAaAb'],
                           'B': ['AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'C': ['AB'],
                           'E': ['BA']
                           }
        self.assertEqual(self.P2, expected_result)

    def test_elim_inaccesible_sumb(self):
        expected_result = {'S': ['bA', 'AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'A': ['a', 'aS', 'bAaAb'],
                           'B': ['AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'C': ['AB']
                           }
        self.assertEqual(self.P3, expected_result)

    def test_elim_unprod_symb(self):
        expected_result = {'S': ['bA', 'AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'A': ['a', 'aS', 'bAaAb'],
                           'B': ['AC', 'bS', 'aAa', 'a', 'aS', 'bAaAb'],
                           'C': ['AB']
                           }
        self.assertEqual(self.P4, expected_result)

    def test_transform_to_cnf(self):
        expected_result = {'S': ['DE', 'AC', 'DF', 'GH', 'a', 'GF', 'IJ'],
                           'A': ['a', 'GF', 'IJ'],
                           'B': ['AC', 'DF', 'GH', 'a', 'GF', 'IJ'],
                           'C': ['AB'],
                           'D': ['b'],
                           'E': ['A'],
                           'F': ['S'],
                           'G': ['a'],
                           'H': ['Aa'],
                           'I': ['bA'],
                           'J': ['aAb']
                           }
        self.assertEqual(self.P5, expected_result)


if __name__ == '__main__':
    unittest.main() 