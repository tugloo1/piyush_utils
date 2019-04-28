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
    increment_scale = [0, 2, 2, 1, 2, 2, 2, 1]
    reverse_scale = [0, -1, -2, -2, -2, -1, -2, -2]
    even_intervals = [2, 5, 9, 12]
    odd_intervals = [4, 7, 11]
    piano_range = (-39, 48)

    @classmethod
    def get_full_scale(cls, key_scale: str):
        scale_shift = cls.scale_shift[key_scale]
        bottom_portion = []
        last_played = scale_shift
        while last_played > cls.piano_range[0]:
            index = len(bottom_portion) % len(cls.reverse_scale)
            last_played += cls.reverse_scale[index]
            bottom_portion.append(last_played)

        top_portion = []
        last_played = scale_shift
        while last_played < cls.piano_range[-1]:
            index = len(top_portion) % len(cls.increment_scale)
            last_played += cls.increment_scale[index]
            top_portion.append(last_played)

        return sorted(list(set(bottom_portion + top_portion)))

    @staticmethod
    def select_random_scale():
        return random.sample(RandomIntervals.scale_shift.keys(), 1)[0]

    @classmethod
    def get_random_notes_for_a_scale(cls, n: int, scale_type):
        notes = []
        if scale_type == 'base':
            scale = cls.base_scale
        elif scale_type == 'even':
            scale = cls.even_intervals
        elif scale_type == 'odd':
            scale = cls.odd_intervals
        else:
            raise Exception('Unhandled scale type ' + scale_type)
        while n > len(scale):
            n -= len(scale)
            notes += random.sample(scale, len(scale))
        notes += random.sample(scale, n)
        return notes

    @classmethod
    def generate_n_random_notes(cls, n: int, scale: str=None, scale_type: str='base'):
        duration = abjad.Duration(1, 4)
        if not scale:
            scale = cls.select_random_scale()
        print('selected scale is ' + scale)
        signature = KeySignature(scale.lower(), 'major')
        random_scale = cls.scale_shift[scale]
        notes = cls.get_random_notes_for_a_scale(n, scale_type)
        new_notes = [abjad.Note(i + random_scale, duration) for i in notes]
        staff = abjad.Staff(new_notes)
        abjad.attach(signature, staff[0])
        abjad.show(staff)

    @classmethod
    def generate_random_interval_sequences(cls, n: int, scale: str=None, scale_type: str='base'):
        duration = abjad.Duration(1, 4)
        if not scale:
            scale = cls.select_random_scale()
        print('selected scale is ' + scale)
        signature = KeySignature(scale.lower(), 'major')
        random_scale = cls.scale_shift[scale]
        notes = cls.get_random_notes_for_a_scale(n, scale_type=scale_type)
        new_notes = []
        for note in notes:
            new_notes.append(abjad.Note(random_scale, duration))
            new_notes.append(abjad.Note(note + random_scale, duration))
        staff = abjad.Staff(new_notes)
        abjad.attach(signature, staff[0])
        abjad.show(staff)


if __name__ == '__main__':
    RandomIntervals.generate_n_random_notes(100, 'Bb', 'even')

