import random
import os
import shutil
import time

# Function to get terminal size dynamically
def get_terminal_size():
    size = shutil.get_terminal_size((80, 24))  # Default size if detection fails
    return size.columns, size.lines

# Number of stars that can exist at the same time
MAX_STARS = 20  
DELAY = 0.5  # Speed of tail growth (lower = faster)

EMPTY_CHAR = ' '  # Background space
STAR_CHAR = '⭐️'  # The star (head)
TAIL_CHAR = '\\'  # The tail (diagonal up-left)

# List to track shooting stars (stars remain fixed, only tails extend)
shooting_stars = []  # [x_pos, y_pos, tail_length]

try:
    while True:
        # Get current terminal size
        WIDTH, HEIGHT = get_terminal_size()

        # Add a new star with 20% probability
        if len(shooting_stars) < MAX_STARS and random.random() < 0.2:
            start_x = random.randint(2, WIDTH - 1)  # Start anywhere in width
            start_y = random.randint(2, HEIGHT - 1)  # Start anywhere in height
            shooting_stars.append([start_x, start_y, 0])  # [x, y, tail_length=0]

        # Clear screen buffer
        screen = [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]

        # Update and draw shooting stars
        for star in shooting_stars:
            x, y, tail_length = star

            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                screen[y][x] = STAR_CHAR  # Keep the star in its original place

                # Extend the tail diagonally up-left
                for i in range(1, tail_length + 1):
                    tail_x = x - i
                    tail_y = y - i
                    if 0 <= tail_x < WIDTH and 0 <= tail_y < HEIGHT:
                        screen[tail_y][tail_x] = TAIL_CHAR  

                # Increase tail length over time
                star[2] += 1  

        # Print updated scene
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        for row in screen:
            print(''.join(row))

        time.sleep(DELAY)  # Control speed of tail growth

except KeyboardInterrupt:
    print("\nShooting Stars stopped. 🌠")