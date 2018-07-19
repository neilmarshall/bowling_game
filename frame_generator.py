#!/usr/bin/env python3.6

import random
import unittest
import unittest.mock as mock

def generate_pair_of_pins(last_pair=False):
    """
    Generate pairs of pins as follows:
    
        First ball is a random choice from [0, ..., 10], with greater weights
        for [6, ..., 9] and greatest weight for 10; occassionally, a foul ball
        will be thrown - denoted 'F'
        
        If first ball is 10 then second ball is None, else it is a 50/50 choice
        from (a) 10 - value of first ball, and (b) a random choice from the
        half-open interval [0, ..., 10 - value of first ball)
        
        If last_pair=True and sum of pair is 10, add a final ball randomly
        selected from interval [0, ..., 10]
    """
    possible_rolls = list(range(11)) + ['F']

    first_ball = random.choices(population=possible_rolls,
                                weights=[1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 5, 2],
                                k=1).pop()

    if first_ball == 10:
        second_ball = random.choice(possible_rolls) if last_pair else None
    elif first_ball == 'F':
        second_ball = random.choice(possible_rolls)
    else:
        second_ball = random.choice([10 - first_ball,
                                     random.randrange(0, 10 - first_ball),
                                     'F'])

    total = sum(x for x in (first_ball, second_ball) if x is not None and x != 'F')

    if last_pair and total >= 10:
        fill_ball = random.choice(possible_rolls)
        return (first_ball, second_ball, fill_ball)
    else:
        return (first_ball, second_ball)


def generate_frame():
    """
    Return list of 10 pairs of pins (last pair may include a fill ball)
    """
    return tuple([generate_pair_of_pins() for _ in range(9)] +
                 [generate_pair_of_pins(True)])
    

def generate_series():
    """
    Return a tuple of tuples - the outer tuple represents one series per player,
    and the inner tuples represent frames per series
    """
    return (tuple(generate_frame() for _ in range(3)),
            tuple(generate_frame() for _ in range(3)))


@mock.patch('random.choice')
@mock.patch('random.choices')
class TestGeneratePairs(unittest.TestCase):

    def test_generate_basic(self, mock_choices, mock_choice):
        mock_choices.return_value = [5]
        mock_choice.return_value = 4
        self.assertTupleEqual(generate_pair_of_pins(), (5, 4))

    def test_generate_strike(self, mock_choices, mock_choice):
        mock_choices.return_value = [10]
        self.assertTupleEqual(generate_pair_of_pins(), (10, None))

    def test_generate_spare(self, mock_choices, mock_choice):
        mock_choices.return_value = [8]
        mock_choice.return_value = 2
        self.assertTupleEqual(generate_pair_of_pins(), (8, 2))

    def test_generate_basic_as_last_pair(self, mock_choices, mock_choice):
        mock_choices.return_value = [5]
        mock_choice.return_value = 4
        self.assertTupleEqual(generate_pair_of_pins(True), (5, 4))

    def test_generate_strike_as_last_pair(self, mock_choices, mock_choice):
        mock_choices.return_value = [10]
        mock_choice.side_effect = [4, 6]
        self.assertTupleEqual(generate_pair_of_pins(True), (10, 4, 6))

    def test_generate_spare_as_last_pair(self, mock_choices, mock_choice):
        mock_choices.return_value = [8]
        mock_choice.side_effect = [2, 3]
        self.assertTupleEqual(generate_pair_of_pins(True), (8, 2, 3))

    def test_generate_basic_with_two_fouls(self, mock_choices, mock_choice):
        mock_choices.return_value = ['F']
        mock_choice.return_value = 'F'
        self.assertTupleEqual(generate_pair_of_pins(), ('F', 'F'))

    def test_generate_basic_with_foul_first_ball(self, mock_choices, mock_choice):
        mock_choices.return_value = ['F']
        mock_choice.return_value = 4
        self.assertTupleEqual(generate_pair_of_pins(), ('F', 4))

    def test_generate_basic_with_foul_second_ball(self, mock_choices, mock_choice):
        mock_choices.return_value = [7]
        mock_choice.return_value = 'F'
        self.assertTupleEqual(generate_pair_of_pins(), (7, 'F'))

    def test_generate_spare_with_foul_first_ball(self, mock_choices, mock_choice):
        mock_choices.return_value = ['F']
        mock_choice.return_value = 10
        self.assertTupleEqual(generate_pair_of_pins(), ('F', 10))

    def test_generate_basic_with_foul_first_ball_as_last_pair(self, mock_choices, mock_choice):
        mock_choices.return_value = ['F']
        mock_choice.return_value = 4
        self.assertTupleEqual(generate_pair_of_pins(True), ('F', 4))

    def test_generate_basic_with_foul_second_ball_as_last_pair(self, mock_choices, mock_choice):
        mock_choices.return_value = [7]
        mock_choice.return_value = 'F'
        self.assertTupleEqual(generate_pair_of_pins(True), (7, 'F'))

    def test_generate_spare_with_foul_first_ball_as_last_pair(self, mock_choices, mock_choice):
        mock_choices.return_value = ['F']
        mock_choice.side_effect = [10, 5]
        self.assertTupleEqual(generate_pair_of_pins(True), ('F', 10, 5))


    def test_generate_strike_with_subsequent_fouls(self, mock_choices, mock_choice):
        mock_choices.return_value = [10]
        mock_choice.side_effect = ['F', 'F']
        self.assertTupleEqual(generate_pair_of_pins(True), (10, 'F', 'F'))


class TestGenerateFrame(unittest.TestCase):

    @mock.patch('__main__.generate_pair_of_pins')
    def test_generate_frame(self, mock_pairs):
        scores = ((4, 5), (4, 0), (10, None), (8, 2), (7, 1), (3, 6), (0, 0), (1, 0), (10, None), (9, 0))
        mock_pairs.side_effect = scores
        self.assertTupleEqual(generate_frame(), scores)


class TestGenerateSeries(unittest.TestCase):

    @mock.patch('__main__.generate_frame')
    def test_assert_generate_frame_called(self, mock_frames):
        series = generate_series()
        self.assertEqual(mock_frames.call_count, 6)
        self.assertIsInstance(series, tuple)


class TestGenerateFullTests(unittest.TestCase):
    
    def setUp(self):
        random.seed(0)
    
    def test_generate_pair_of_pins_complete_no_last_pair(self):
        pairs = [generate_pair_of_pins() for _ in range(6)]
        self.assertListEqual(pairs, [(10, None), (10, None), (7, 'F'), (8, 1), (6, 'F'), (3, 7)])

    def test_generate_pair_of_pins_complete_with_last_pair(self):
        pairs = [generate_pair_of_pins(True) for _ in range(6)]
        self.assertListEqual(pairs, [(10, 6, 0), (5, 4), (7, 1), (6, 'F'), (3, 7, 9), (10, 8, 'F')])

    def test_generate_frame_complete(self):
        frame = generate_frame()
        self.assertTupleEqual(frame, ((10, None), (10, None), (7, 'F'), (8, 1), (6, 'F'), (3, 7), (9, 'F'), ('F', 9), (10, None), (6, 'F')))

    def test_generate_series_complete(self):
        series = generate_series()
        self.assertEqual(len(series), 2)
        self.assertEqual(len(series[0]), 3)
        self.assertEqual(len(series[1]), 3)
        self.assertTupleEqual(series[0][0][0], (10, None))
        self.assertTupleEqual(series[0][1][1], (7, 'F'))
        self.assertTupleEqual(series[0][2][2], (5, 'F'))
        self.assertTupleEqual(series[1][0][-1], (10, 8, 4))
        self.assertTupleEqual(series[1][1][-1], (7, 0))
        self.assertTupleEqual(series[1][2][-1], (10, 1, 0))


if __name__ == '__main__':
    unittest.main()

