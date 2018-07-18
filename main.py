#!/usr/bin/env python3.6

from itertools import zip_longest

def score_game(frame):
    """
    Args : frame (list)
        List of pins as tuples indicating score on first and second
        balls. If a strike is achieved (i.e. score on first pin is
        10) then second ball will be 'None'.

    Basic test with no strikes / spares:
        Note: Frame scores = [9, 8, 1, 7, 9, 0, 6, 5, 5, 7]
    >>> score_game([(8, 1), (8, 0), (1, 0), (6, 1), (6, 3), \
                    (0, 0), (0, 6), (4, 1), (4, 1), (5, 2)])
    57

    Test including strikes / spares but not ending in a strike / spare:
        Note: Frame scores = [18, 8, 17, 7, 10, 10, 6, 20, 17, 7]
    >>> score_game([(8, 2), (8, 0), (10, None), (6, 1), (7, 3), \
                    (0, 10), (0, 6), (9, 1), (10, None), (5, 2)])
    120

    Test with frame ending in a strike, resulting in 2 fill balls
        Note: Frame scores = [20, 19, 9, 18, 8, 10, 6, 30, 28, 19]
    >>> score_game([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                    (8, 2), (0, 6), (10, None), (10, None), (10, 8, 1)])
    167

    Test with frame ending in a spare, resulting in a fill ball
        Note: Frame scores = [20, 19, 9, 18, 8, 10, 6, 29, 20, 11]
    >>> score_game([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                    (8, 2), (0, 6), (10, None), (10, None), (9, 1, 1)])
    150

    Test with frame ending in a spare, resulting in a fill ball, which is missed
        Note: Frame scores = [20, 19, 9, 18, 8, 10, 6, 29, 20, 10]
    >>> score_game([(10, None), (7, 3), (9, 0), (10, None), (0, 8), \
                    (8, 2), (0, 6), (10, None), (10, None), (9, 1, 0)])
    149

    Test perfect game:
        Note: Frame scores = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    >>> score_game([(10, None), (10, None), (10, None), (10, None), (10, None), \
                    (10, None), (10, None), (10, None), (10, None), (10, 10, 10)])
    300

    Test first frame produced by frame generator:
        Note: Frame scores = [27, 18, 8, 8, 15, 5, 18, 8, 2, 7]
    >>> score_game([(10, None), (10, None), (7, 1), (7, 1), (6, 4), (5, 0), \
                    (10, None), (8, 0), (1, 1), (7, 0)])
    116
    """
    def score_pair(pair1, pair2, pair3):
        if pair1 == (10, None):
            return 10 + pair2[0] + (pair2[1] if pair2[1] is not None else pair3[0])  # score strikes
        elif len(pair1) == 2 and sum(pair1) == 10:
            return 10 + pair2[0]  # score spares
        else:
            return sum(pair1)  # scores non-strikes/spares
    return sum([score_pair(p1, p2, p3) for p1, p2, p3 in zip_longest(frame, frame[1:], frame[2:])])


if __name__ == '__main__':
    import doctest; doctest.testmod()

