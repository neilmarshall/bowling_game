import random

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
                                k=1)
    if first_ball == 10:
        second_ball = None
    else:
        second_ball = random.choice([10 - first_ball, random.randrange(0, 10 - first_ball)])

    if last_pair and (first_ball == 10 or first_ball + second_ball == 10):
        fill_ball = random.randint(0, 10)
    else:
        fill_ball = None

    return (first_ball, second_ball, fill_ball) if fill_ball else (first_ball, second_ball)

def generate_frame():
    """
    Return list of 10 pairs of pins (last pair may include a fill ball)
    """
    return [generate_pair_of_pins() for _ in range(9)] + [generate_pair_of_pins(True)]
    
