from unittest import TestCase
from music.random_intervals import RandomIntervals


class RandomIntervalsTest(TestCase):

    def test_get_possible_notes_with_range(self):
        start, end = -1, 14
        valid = [-1, 1, 3, 4, 6, 8, 10, 11, 13]
        o = RandomIntervals.get_possible_notes_with_range(-1, 14)
        self.assertEqual(o, valid)
