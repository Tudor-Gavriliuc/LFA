import unittest

from classes import Gramamr


class TestGrammar(unittest.TestCase):
    def setUp(self):
        # This method sets up the environment before each test is run.
        # It initializes the grammar class and pre-computes all transformations.
        self.g = Gramamr()
        self.P1, self.P2, self.P3, self.P4, self.P5 = self.g.ReturnProductions()

    def test_remove_epsilon(self):
        expected_result = {'S': ['A', 'DA', 'aB'], 'A': ['BD', 'a', 'bAB', 'bDAB', 'B'], 'B': ['b', 'BA'], 'D': ['BA'],
                           'C': ['BA']}
        # Sort productions for comparison
        for key in self.P1.keys():
            self.P1[key].sort()
            expected_result[key].sort()
        self.assertEqual(self.P1, expected_result)

    def test_eliminate_unit_prod(self):
        # Test method to verify that unit productions are correctly eliminated.
        # Unit productions are productions where a non-terminal directly produces another non-terminal.
        expected_result = {
            'S': ['aB', 'DA', 'a', 'BD', 'bDAB', 'bAB', 'b', 'BA'],
            'A': ['a', 'BD', 'bDAB', 'bAB', 'b', 'BA'],
            'B': ['b', 'BA'],
            'D': ['BA'],
            'C': ['BA']
        }
        self.assertEqual(self.P2, expected_result)

    def test_eliminate_inaccesible(self):
        # Test method to verify that inaccessible symbols are correctly removed.
        # Inaccessible symbols are non-terminals that cannot be reached from the start symbol.
        expected_result = {
            'A': ['a', 'BD', 'bDAB', 'bAB', 'b', 'BA'],
            'B': ['b', 'BA'],
            'D': ['BA']
        }
        self.assertEqual(self.P3, expected_result)

    def test_remove_unprod(self):
        # Test method to verify that unproductive symbols are correctly removed.
        # Unproductive symbols are those that do not lead to terminal strings.
        expected_result = {
            'A': ['a', 'BD', 'bDAB', 'bAB', 'b', 'BA'],
            'B': ['b', 'BA'],
            'D': ['BA']
        }
        self.assertEqual(self.P4, expected_result)

    def test_obtain_cnf(self):
        # Test method to verify that the grammar is correctly transformed to Chomsky Normal Form (CNF).
        # In CNF, each production is either two non-terminals or a single terminal.
        expected_result = {
            'A': ['a', 'BD', 'CE', 'FE', 'b', 'BA'],
            'B': ['b', 'BA'],
            'D': ['BA'],
            'C': ['bD'],
            'E': ['AB'],
            'F': ['b']
        }
        self.assertEqual(self.P5, expected_result)

if __name__ == '__main__':
    unittest.main()
