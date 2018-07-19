#!/usr/bin/env python3.6

from itertools import zip_longest

def score_frame(frame):
    """
    Args : frame (list)
        List of pins as tuples indicating score on first and second
        balls. If a strike is achieved (i.e. score on first pin is
        10) then second ball will be 'None'. Foul balls will be
        denoted as 'F'.

    Basic test with no strikes / spares:
        Note: Frame scores = [9, 8, 1, 7, 9, 0, 6, 5, 5, 7]
    >>> score_frame([(8, 1), (8, 0), (1, 0), (6, 1), (6, 3), \
                    (0, 0), (0, 6), (4, 1), (4, 1), (5, 2)])
    57

    Test including strikes / spares but not ending in a strike / spare:
        Note: Frame scores = [18, 8, 17, 7, 10, 10, 6, 20, 17, 7]
    >>> score_frame([(8, 2), (8, 0), (10, None), (6, 1), (7, 3), \
                    (0, 10), (0, 6), (9, 1), (10, None), (5, 2)])
    120

    Test with frame ending in a strike, resulting in 2 fill balls
        Note: Frame scores = [20, 19, 9, 18, 8, 10, 6, 30, 28, 19]
    >>> score_frame([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                    (8, 2), (0, 6), (10, None), (10, None), (10, 8, 1)])
    167

    Test with frame ending in a spare, resulting in a fill ball
        Note: Frame scores = [20, 19, 9, 18, 8, 10, 6, 29, 20, 11]
    >>> score_frame([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                    (8, 2), (0, 6), (10, None), (10, None), (9, 1, 1)])
    150

    Test with frame ending in a spare, resulting in a fill ball, which is missed
        Note: Frame scores = [20, 19, 9, 18, 8, 10, 6, 29, 20, 10]
    >>> score_frame([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                    (8, 2), (0, 6), (10, None), (10, None), (9, 1, 0)])
    149

    Test perfect game:
        Note: Frame scores = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    >>> score_frame([(10, None), (10, None), (10, None), (10, None), (10, None), \
                    (10, None), (10, None), (10, None), (10, None), (10, 10, 10)])
    300

    Test frame produced by frame generator:
        Note: Frame scores = [27, 18, 8, 8, 15, 5, 18, 8, 2, 7]
    >>> score_frame([(10, None), (10, None), (7, 1), (7, 1), (6, 4), (5, 0), \
                    (10, None), (8, 0), (1, 1), (7, 0)])
    116

    Test frame with foul balls:
        Note: Frame scores = [27, 17, 7, 9, 6, 19, 9, 9, 16, 6]
    >>> score_frame([(10, None), (10, None), (7, 'F'), (8, 1), (6, 'F'), \
                    (3, 7), (9, 'F'), ('F', 9), (10, None), (6, 'F')])
    125
    """
    def replace_fouls(pair):
        return tuple(x if x != 'F' else 0 for x in pair)
    def score_pair(pair1, pair2, pair3):
        pair1, pair2, pair3 = map(replace_fouls, (pair1, pair2, pair3))
        if pair1 == (10, None):
            return 10 + pair2[0] + (pair2[1] if pair2[1] is not None else pair3[0])  # score strikes
        elif len(pair1) == 2 and sum(pair1) == 10:
            return 10 + pair2[0]  # score spares
        else:
            return sum(pair1)  # scores non-strikes/spares
    return sum([score_pair(p1, p2, p3) for p1, p2, p3 in zip_longest(frame, frame[1:], frame[2:], fillvalue=(None, None))])


def calculate_total_pins(series):
    """
    >>> frame1 = ([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                   (8, 2), (0, 6), (10, None), (10, None), (9, 1, 1)])
    >>> frame2 = ([(10, None), (10, None), (7, 'F'), (8, 1), (6, 'F'), \
                   (3, 7), (9, 'F'), ('F', 9), (10, None), (6, 'F')])
    >>> frame3 = ([(10, None), (10, None), (10, None), (10, None), (10, None), \
                   (10, None), (10, None), (10, None), (10, None), (10, 10, 10)])
    >>> calculate_total_pins((frame1, frame2, frame3))
    300
    """
    return sum(sum(roll for turn in frame for roll in turn if roll is not None and roll != 'F') for frame in series)


def score_match(series):
    """
    A match between two players consists of three frames, collectively called a series.

    For each frame, the player with the higher score receives two points (or both players
    receive a point eac if their scores are tied).

    In addition, the player with the most pins knocked down in total across all three
    frames (bonus points for strikes and spares do NOT count, but fill balls do) receives
    an additional point. No points are awarded here in the event of a tie.

    Function returns who won the match.

    >>> frame1 = (((10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                   (8, 2), (0, 6), (10, None), (10, None), (9, 1, 1)))
    >>> frame2 = (((8, 2), (8, 0), (10, None), (6, 1), (7, 3), \
                   (0, 10), (0, 6), (9, 1), (10, None), (5, 2)))
    >>> frame3 = (((10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                   (8, 2), (0, 6), (10, None), (10, None), (10, 8, 1)))

    >>> frameA = (((8, 1), (8, 0), (1, 0), (6, 1), (6, 3), \
                   (0, 0), (0, 6), (4, 1), (4, 1), (5, 2)))
    >>> frameB = (((10, None), (10, None), (7, 'F'), (8, 1), (6, 'F'), \
                   (3, 7), (9, 'F'), ('F', 9), (10, None), (6, 'F')))
    >>> frameC = (((10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                   (8, 2), (0, 6), (10, None), (10, None), (10, 8, 1)))

    Scores for the frames are ([150, 120, 167], [57, 125, 167])
    Total pins knocked down are (284, 245)
    Points are therefore {Player 1: [2, 0, 1, 1], Player 2: [0, 2, 1, 0]}

    >>> score_match(((frame1, frame2, frame3), (frameA, frameB, frameC)))
    'Player 1 won!'

    >>> frame1 = ((10, None), (6, 2), (9, 1), (9, 0), (10, None),\
                  (9, 'F'), (5, 5), (6, 1), ('F', 1), (8, 0))
    >>> frame2 = ((4, 3), (9, 'F'), (0, 10), (9, 0), (7, 1),\
                  (7, 'F'), (10, None), (10, None), (3, 7), (9, 0))
    >>> frame3 = ((8, 2), (6, 'F'), (7, 0), ('F', 9), (6, 1), \
                  ('F', 1), (10, None), (6, 2), (9, 1), (6, 4, 0))

    >>> frameA = ((5, 5), (7, 1), (10, None), ('F', 2), (7, 1), \
                  (10, None), (10, None), (7, 3), (4, 6), (5, 'F'))
    >>> frameB = ((9, 'F'), ('F', 10), (6, 'F'), (9, 1), (7, 1), \
                  ('F', 3), ('F', 10), (7, 3), (10, None), (9, 'F'))
    >>> frameC = ((8, 2), (9, 'F'), (5, 'F'), ('F', 1), (10, None), \
                  (1, 7), (10, None), ('F', 0), (5, 2), (10, 5, 6))

    Scores for the frames are ([114, 130, 98], [128, 124, 98])
    Total pins knocked down are (249, 249)
    Points are therefore {Player 1: [0, 2, 1, 0], Player 2: [2, 0, 1, 0]}

    >>> score_match(((frame1, frame2, frame3), (frameA, frameB, frameC)))
    'The match is a draw!'
    """
    scores = {i: tuple(score_frame(frame) for frame in series[i]) for i in range(2)}

    points = {i: [] for i in range(2)}

    for frame in range(3):
        if scores[0][frame] > scores[1][frame]:
            points[0].append(2)
            points[1].append(0)
        elif scores[0][frame] < scores[1][frame]:
            points[0].append(0)
            points[1].append(2)
        else:
            points[0].append(1)
            points[1].append(1)

    total_pins = {i: calculate_total_pins(series[i]) for i in range(2)}

    if total_pins[0] > total_pins[1]:
        points[0].append(1)
        points[1].append(0)
    elif total_pins[0] < total_pins[1]:
        points[0].append(0)
        points[1].append(1)

    if sum(points[0]) > sum(points[1]):
        return "Player 1 won!"
    elif sum(points[0]) < sum(points[1]):
        return "Player 2 won!"
    else:
        return "The match is a draw!"


if __name__ == '__main__':
    import doctest; doctest.testmod(verbose=True)

