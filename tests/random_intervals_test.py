from unittest import TestCase
from music.random_intervals import RandomIntervals


class RandomIntervalsTest(TestCase):

    def test_get_possible_notes_with_range(self):
        start, end = -1, 14
        valid = [-1, 1, 3, 4, 6, 8, 10, 11, 13]
        o = RandomIntervals.get_possible_notes_with_range(-1, 14)
        self.assertEqual(o, valid)

    def test_get_full_scale(self):
        i = RandomIntervals.get_full_scale('C')
        bottom = [-39, -37, -36, -34, -32, -31, -29, -27, -25, -24, -22, -20, -19, -17, -15, -13, -12,
                 -10, -8, -7, -5, -3, -1, 0]
        top = [2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24, 26, 28, 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47,
               48]
        self.assertEqual(bottom + top, i)
