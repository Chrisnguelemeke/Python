import unittest
from fractions import Fraction

from my_sum import sum


class TestSum(unittest.TestCase):
    def test_list_int(self):
        """
        Test that it can sum a list of integers
        """
        data = [1, 2, 3]
        result = sum(data)
        self.assertEqual(result, 6)

    def test_list_fraction(self):
        """
        Test that it can sum a list of fractions
        """
        data = [Fraction(1, 4), Fraction(1, 4), Fraction(2, 5)]
        result = sum(data)
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()

"""
Test Results:

When I ran the tests with "python -m unittest test", 2 tests ran.
The output started with "F." which means one test failed (F) and
one test passed (.).

test_list_int passed because the sum of 1, 2, and 3 is 6, which
matches the expected value.

test_list_fraction failed on purpose. The sum of 1/4 + 1/4 + 2/5
is 9/10, but the test expected 1, so unittest showed an
AssertionError saying Fraction(9, 10) != 1.

This shows that unit tests compare what the code actually returns
to what we expect it to return. A failing test doesn't always mean
the function is broken. In this case the sum function worked
correctly, and the test itself had the wrong expected value.
"""