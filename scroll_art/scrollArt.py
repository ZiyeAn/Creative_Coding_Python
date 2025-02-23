import random
import time
import os
import shutil

#terminal size
def get_terminal_size():
    size = shutil.get_terminal_size((80, 24))
    return size.columns, size.lines

# Terminal width
WIDTH, HEIGHT = get_terminal_size()

DELAY = 0.05  
NEW_STAR_PROB = 0.3  

capacity = 1
step = 0
increasing_capacity = True
CAPACITY_INC_EVERY = 10  
CAPACITY_DEC_EVERY = 3 
MAX_CAPACITY = 20 

# List of stars [x_pos, length, progress]
shooting_stars = []

try:
    while True:
        WIDTH, HEIGHT = get_terminal_size() 
        step += 1  

        # add or delete star
        if increasing_capacity and step == CAPACITY_INC_EVERY:
            step = 0
            capacity += 1
            if capacity == MAX_CAPACITY:
                increasing_capacity = False
        elif not increasing_capacity and step >= CAPACITY_DEC_EVERY and len(shooting_stars) < capacity:
            step = 0
            capacity -= 1
            if capacity == 0:
                increasing_capacity = True

        # chekc if meet capacity
        if len(shooting_stars) < capacity and random.random() < NEW_STAR_PROB:
            start_x = random.randint(0, WIDTH - 1)  # Start anywhere in width
            length = random.randint(5, 15)  # Random length between 5 and 15
            shooting_stars.append([start_x, length, 0])  # [x, length, progress]

        line = [' '] * WIDTH

        # draw stars
        new_stars = []
        for x, length, progress in shooting_stars:
            if progress < length:
                char = '⭐️' if progress == length - 1 else '\\'
                if 0 <= x < WIDTH:
                    line[x] = char
                new_stars.append([x + 1, length, progress + 1])

        shooting_stars = new_stars

        print(''.join(line))

        time.sleep(DELAY)

except KeyboardInterrupt:
    print("\nShooting Stars stopped. 🌠")