#!/usr/bin/env python3.6

import random
import unittest
import unittest.mock as mock

def generate_pair_of_pins(last_pair=False):
    """
    Generate pairs of pins as follows:
    
        First ball is a random choice from [0, ..., 10], with greater weights
        for [6, ..., 9] and greatest weight for 10
        
        If first ball is 10 then second ball is None, else it is a 50/50 choice
        from (a) 10 - value of first ball, and (b) a random choice from the
        half-open interval [0, ..., 10 - value of first ball)
        
        If last_pair=True and sum of pair is 10, add a final ball randomly
        selected from interval [0, ..., 10]
    """
    first_ball = random.choices(population=list(range(11)),
                                weights=[1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 5],
                                k=1).pop()

    if first_ball == 10:
        second_ball = random.randint(0, 10) if last_pair else None
    else:
        second_ball = random.choice([10 - first_ball, random.randrange(0, 10 - first_ball)])

    if last_pair and (first_ball == 10 or first_ball + second_ball == 10):
        fill_ball = random.randint(0, 10)
        return (first_ball, second_ball, fill_ball)
    else:
        return (first_ball, second_ball)


def generate_frame():
    """
    Return list of 10 pairs of pins (last pair may include a fill ball)
    """
    return [generate_pair_of_pins() for _ in range(9)] + [generate_pair_of_pins(True)]
    

@mock.patch('random.randint')
@mock.patch('random.choice')
@mock.patch('random.choices')
class TestGeneratePairs(unittest.TestCase):

    def test_generate_basic(self, mock_choices, mock_choice, mock_randint):
        mock_choices.return_value = [5]
        mock_choice.return_value = 4
        self.assertTupleEqual((5, 4), generate_pair_of_pins())

    def test_generate_strike(self, mock_choices, mock_choice, mock_randint):
        mock_choices.return_value = [10]
        self.assertTupleEqual((10, None), generate_pair_of_pins())

    def test_generate_spare(self, mock_choices, mock_choice, mock_randint):
        mock_choices.return_value = [8]
        mock_choice.return_value = 2
        self.assertTupleEqual((8, 2), generate_pair_of_pins())

    def test_generate_basic_as_last_pair(self, mock_choices, mock_choice, mock_randint):
        mock_choices.return_value = [5]
        mock_choice.return_value = 4
        self.assertTupleEqual((5, 4), generate_pair_of_pins(True))

    def test_generate_strike_as_last_pair(self, mock_choices, mock_choice, mock_randint):
        mock_choices.return_value = [10]
        mock_randint.side_effect = [4, 6]
        self.assertTupleEqual((10, 4, 6), generate_pair_of_pins(True))

    def test_generate_spare_as_last_pair(self, mock_choices, mock_choice, mock_randint):
        mock_choices.return_value = [8]
        mock_choice.return_value = 2
        mock_randint.return_value = 3
        self.assertTupleEqual((8, 2, 3), generate_pair_of_pins(True))


class TestGenerateFrame(unittest.TestCase):

    @mock.patch('__main__.generate_pair_of_pins')
    def test_generate_frame(self, mock_pairs):
        scores = [(4, 5), (4, 0), (10, None), (8, 2), (7, 1), (3, 6), (0, 0), (1, 0), (10, None), (9, 0)]
        mock_pairs.side_effect = scores
        self.assertListEqual(scores, generate_frame())


class TestGenerateFullTests(unittest.TestCase):
    
    def setUp(self):
        random.seed(0)
    
    def test_generate_pair_of_pins_complete_no_last_pair(self):
        pairs = [generate_pair_of_pins() for _ in range(6)]
        self.assertListEqual(pairs, [(10, None), (10, None), (7, 1), (7, 1), (6, 4), (5, 0)])

    def test_generate_pair_of_pins_complete_with_last_pair(self):
        pairs = [generate_pair_of_pins(True) for _ in range(6)]
        self.assertListEqual(pairs, [(10, 6, 0), (5, 4), (7, 1), (6, 4, 4), (2, 1), (10, 8, 9)])

    def test_generate_frame_complete(self):
        frame = generate_frame()
        self.assertListEqual(frame, [(10, None), (10, None), (7, 1), (7, 1), (6, 4), (5, 0), (10, None), (8, 0), (1, 1), (7, 0)])


if __name__ == '__main__':
    unittest.main()

