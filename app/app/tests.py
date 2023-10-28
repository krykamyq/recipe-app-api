"""Test for calc.py"""

from django.test import SimpleTestCase

from .calc import add, sub


class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        res = add(5, 6)
        self.assertEqual(res, 11)

    def test_substract_numbers(self):
        res = sub(20, 11)
        self.assertEqual(res, 9)
