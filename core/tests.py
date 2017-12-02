from django.test import TestCase

from core.mem_curve import calc_ranks


class TestCalc_ranks(TestCase):
    def test_calc_ranks(self):
        self.assertEqual((0, 0), calc_ranks(0, 0, True))
        # self.assertEqual((0, -5), calc_ranks(0, 1, True))
        self.assertEqual((2, 40), calc_ranks(0, 2, True))
        # self.assertEqual((0, 5), calc_ranks(0, 3, True))
        self.assertEqual((3, 50), calc_ranks(0, 4, True))

        # self.assertEqual((0, 0), calc_ranks(0, 0, False))
        self.assertEqual((2, 35), calc_ranks(40, 1, False))
        self.assertEqual((2, 40), calc_ranks(40, 2, False))
        self.assertEqual((3, 45), calc_ranks(40, 3, False))
        # self.assertEqual((3, 50), calc_ranks(0, 4, False))
