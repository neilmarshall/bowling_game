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

    Test perfect game:
        Note: Frame scores = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
    >>> score_game([(10, None), (10, None), (10, None), (10, None), (10, None), \
                    (10, None), (10, None), (10, None), (10, None), (10, 10, 10)])
    300
    """
    s = 0
    on_strike = on_spare = False
    # pdb.set_trace()
    for pin in frame:
        s += pin[0] * (2 if on_strike or on_spare else 1)
        s += (pin[1] if pin[1] else 0) * (2 if on_strike else 1)
        on_strike = pin[0] == 10
        on_spare = pin[0] != 10 and sum(x if x else 0 for x in pin) == 10
    return s

if __name__ == '__main__':
    import pdb
    import doctest; doctest.testmod()
