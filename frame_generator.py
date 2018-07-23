import random

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

