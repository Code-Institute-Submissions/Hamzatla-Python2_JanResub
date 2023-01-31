import os
import time
import random

"""
    Title: WARSHIPS
    Author:Hamzat


    Mechanics:
    1. A NxN grid has several scattered in hidden locations
    2. The player has T number of bullets to take them down
    3. The player can choose a coordinate to fire a bullet
    4. Every shot shows up as either hit or miss
    5. discover and destroy the ships before bullets run out, in order to win

    Symbols used:
    - Water: ~
    - Ship:  O
    - Bombed Ship: X
    - Bombed water: # (counts as miss)
"""

is_game_over = False

num_bullets = 50
num_enemy_ships = 3
grid_size = 9
ship_min_size = 3
ship_max_size = 5

grid = [[]]
ships = [[]]

For debugging
show_ships = True

Types of tiles
WATER = '~'
BOMBED_SHIP = 'X'
BOMBED_WATER = '#'
SHIP = 'O'

Directions of ship placement(a primitive enum)
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

AXES = [UP, DOWN, LEFT, RIGHT]

num_ships_remaining = num_enemy_ships
num_bullets_remaining = num_bullets

"""
creates ships according to starting row and column, length and direction,
validates its placement in the grid,
and places it in the grid
"""
def create_ship(row, col, direction, length):

    global grid, ships
    global grid_size

    Check if potential ship fits inside the grid
    if direction == UP:
        if (row - length) < 0:
            return False
    elif direction == DOWN:
        if (row + length) >= grid_size:
            return False
    elif direction == LEFT:
        if (col - length) < 0:
            return False
    elif direction == RIGHT:
        if (col + length) >= grid_size:
            return False

    Ship fits the grid
 Now check if ship placement is blocked by any object, if not, place the ship

    if direction == UP:
        
        Ship can be placed only in water
        for i in range(length):
            if not (grid[row - i][col] == WATER):
                return False

        Place ship
        for i in range(length):
            grid[row - i][col] = SHIP

        ships.append([row - length + 1, col, row, col])

    elif direction == DOWN:

        ship can be placed only in water
        for i in range(length):
            if not (grid[row + i][col] == WATER):
                return False
        
        Place ship
        for i in range(length):
            grid[row + i][col] = SHIP

        ships.append([row, col, row + length - 1, col])

    elif direction == LEFT:

        Ship can be placed only in water
        for j in range(length):
            if not (grid[row][col - j] == WATER):
                return False

        Place ship
        for j in range(length):
            grid[row][col - j] = SHIP

        ships.append([row, col - length + 1, row, col])

    elif direction == RIGHT:

        Ship can be placed only in water
        for j in range(length):
            if not (grid[row][col + j] == WATER):
                return False

        Place ship
        for j in range(length):
            grid[row][col + j] = SHIP

        ships.append([row, col, row, col + length - 1])

    Ship placed successfully
    return True

""" 
Function creates a square grid according to give grid_size,
populates is with water, and random ships
"""
def make_grid():
    global grid_size
    global grid, ships, num_enemy_ships
    global ship_min_size, ship_max_size

    random.seed(time.time())

    grid = []

    #Fill grid with water first
    for i in range(grid_size):
        row = []
        for j in range(grid_size):
            row.append(WATER)
        grid.append(row)

    ships_created = 0
    failures = 0

    ships = []

    while ships_created < num_enemy_ships and failures < 100000:

        ship_row = random.randint(0, grid_size - 1)
        ship_col = random.randint(0, grid_size - 1)

        ship_length = random.randrange(2, 5)
        direction = random.choice(AXES)

        if create_ship(ship_row, ship_col, direction, ship_length):
            #Ship was created and placed in the grid successfully
            ships_created += 1
        else:
            #The function was unable to find a place for the given starting point and length of ship given 
            failures += 1

    if ships_created < num_enemy_ships:
        print("Error: Please adjust ship creation parameters to feasible levels")
        is_game_over = True
        return

""" 
Does the obvious, plus has a debug function that can show the location of the ships if the flag 'show_ships' = True
"""
def print_grid():
    global grid, ships
    global grid_size

    #Prints leading spaces for the first line, which has the column labels
    print("  ", end="")

    #Prints the column labels, starting from 1 (internally all grid indices are from 0 - N)
    for i in range(grid_size):
        print(i + 1, end=" ")

    #For new line
    print("")

    for i in range(grid_size):
        #Prints the row labels (A-Z)
        print(chr(ord('A') + i), end=" ")

        #Prints the actual grid data
        for j in range(grid_size):
            if show_ships:
                print(grid[i][j], end=" ")
            else:
                #In actual game, ships are not visible to the player - instead Water is shown
                if grid[i][j] == SHIP:
                    print(WATER, end=" ")
                else:
                    print(grid[i][j], end=" ")


        print("")
""" 
Function validates input, and checks if the targetted area is already bombed, or a new area
"""
def get_valid_input():

    global grid, ships
    global grid_size

    coords = ''

    print(">> Enter a valid coordinate from the grid (A1-" + str(chr(ord('A') + grid_size - 1)) + str(grid_size) + ")")

    while True:
        coords = input("\n>> ")
        coords = coords.upper()

        #A valid input contains 2 characters
        if len(coords) != 2:
            print("\n>> Invalid Input!\n>> Enter a single letter for the row (e.g. A) followed by a single number for the column (e.g. 5), such as (e.g. A5)\n")
            continue

        #Check if the second coordinate is numeric
        if not coords[1].isnumeric():
            print("\n>> Invalid Input!\n>> Enter a single letter for the row (e.g. A) followed by a single number for the column (e.g. 5), such as (e.g. A5)\n")
            continue

        letter = coords[0]
        number = int(coords[1])

        row = ord(coords[0]) - ord('A') #Convert first coordinate from alphanumeric (A-Z) to grid index (0-n)
        col = int(coords[1]) - 1 #Convert second coordinate from 1-based to 0-based

        #Check if both coords are in range of the grid size
        if row < 0 or row >= grid_size or col < 0 or col >= grid_size:
            print("\n>> Invalid Input!\n>> Enter a single letter for the row (e.g. A) followed by a single number for the column (e.g. 5), such as (e.g. A5)\n")
            continue

        if grid[row][col] == BOMBED_SHIP or grid[row][col] == BOMBED_WATER:
            print("\n>> Area already bombed! Please pick another coordinate\n")
            continue

        if grid[row][col] == WATER or grid[row][col] == SHIP:
            return row, col

"""
Function returns True if the ship at the current coordinate has all of its parts bombed, thus completely destroyed,
else False 
"""
def is_ship_sunk(row, col):
    global grid, ships
    global grid_size

    #print("Sunk coords: " + str(row) + ", " + str(col))

    #Loop through the start and end coordinates of each ship, to see if the current ship coordinate matches
    for ship in ships:

        #If the current coordinate is within this ship
        if (ship[0] <= row <= ship[2]) and (ship[1] <= col <= ship[3]):
            #print("Checking: ", end="")
            #print(ship)

            #Check if all the areas of this ship are bombed
            for i in range(ship[0], ship[2]+1):
                for j in range(ship[1], ship[3]+1):
                    #print("---Checking: " + str(i) + ", " + str(j))
                    if grid[i][j] != BOMBED_SHIP:
                        return False

    return True

"""
Function gets user input and fires the bullet
"""
def fire_bullet():
    global grid, ships
    global grid_size, num_bullets_remaining, num_ships_remaining

    row, col = get_valid_input()
    #Bullet successfully fired, can be at either empty water or enemy ship

    if grid[row][col] == WATER:
        print("\n>> You missed! Try again!\n")
        grid[row][col] = BOMBED_WATER
    elif grid[row][col] == SHIP:
        print("\n>> You hit a ship!\n", end=" ")
        grid[row][col] = BOMBED_SHIP
        if is_ship_sunk(row, col):
            print("You sunk a ship completely! Congratulations!\n")
            num_ships_remaining -= 1
        print("")

    num_bullets_remaining -= 1

"""
The game is over if:
+ All ships are destroyed (Win condition)
(or)
+ No bullets are remaining (Lose condition)
"""
def check_game_over():
    global grid, ships
    global grid_size, num_bullets_remaining, num_ships_remaining
    global is_game_over

    if num_ships_remaining <= 0:
        print("----------------------------------------------------")
        print("Congratulations, you won! Ships remaining = 0")
        print("----------------------------------------------------")
        is_game_over = True
        return
    
    if num_bullets_remaining <= 0 and num_ships_remaining > 0:
        print("----------------------------------------------------")
        print("You ran out of bullets! Game Over!")
        print("----------------------------------------------------")
        is_game_over = True
        return

def main():
    os.system('cls')

    print("--------------------------------- Welcome to Warships!-------------------------------------")
    print("A strategy text-based game where you try to blow up enemy ships by guessing their positions")
    print("-------------------------------------------------------------------------------------------")

    print("You have " + str(num_bullets) + " bullets to take out " + str(num_enemy_ships) + " enemy ships.")
    print("Get started!")
    print("-------------------------------------------------------------------------------------------")

    make_grid()

    for s in ships:
    #    print(s)

    #while(not is_game_over):
        print_grid()
        print("\n[" + str(num_ships_remaining) + " enemy ships remaining]")
        print("\n[" + str(num_bullets_remaining) + " bullets remaining]\n")

        fire_bullet()
        check_game_over()


if __name__ == '__main__':
    main()
