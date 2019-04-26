import abjad
import random
from abjad import KeySignature


class RandomIntervals(object):
    scale_shift = {
        'Bb': -2,
        'C': 0,
        'D': 2,
        'E': 4,
        'F': 5,
        'G': 7,
        'A': 9,
        'B': 11
    }
    base_scale = [0, 2, 4, 5, 7, 9, 11, 12]


    @staticmethod
    def select_random_scale():
        return random.sample(RandomIntervals.scale_shift.keys(), 1)[0]

    @classmethod
    def generate_n_random_notes(cls, n: int, scale: str=None):
        duration = abjad.Duration(1, 4)
        if not scale:
            scale = cls.select_random_scale()
        print('selected scale is ' + scale)
        signature = KeySignature(scale.lower(), 'major')
        random_scale = cls.scale_shift[scale]
        notes = []
        while n > len(cls.base_scale):
            n -= len(cls.base_scale)
            notes += random.sample(cls.base_scale, len(cls.base_scale))
        notes += random.sample(cls.base_scale, n)
        new_notes = [abjad.Note(i + random_scale, duration) for i in notes]
        staff = abjad.Staff(new_notes)
        abjad.attach(signature, staff[0])
        abjad.show(staff)


if __name__ == '__main__':
    RandomIntervals.generate_n_random_notes(20, 'Bb')

