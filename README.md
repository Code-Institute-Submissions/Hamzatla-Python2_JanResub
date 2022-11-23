War Ships
----------------------

Table Of Contents:
1. Introduction
2. Game Map
3. Rules
4. Win Condition
5. Lose Condition
6. How to Run

Introduction
    War Ships is a text based strategy game that runs in the command-line. The player is supplied with a limited amount of bullets, which they must use to discover and destroy
    hidden enemy warships in the game map.

Game Map
    The game takes place in a N x N grid, with each cell containing any one of the following characters, each symbolizing a different aspect:
    1. '~' - Water (empty space)
    2. 'O' - Part of the ship (always hidden in the map, player must find it by using bombs)
    3. 'X' - Part of ship bombed by player (always visible in map, gives an indication as to the rest of the ship's location)
    4. '#' - Part of the water that has been bombed by the player (indicates a "miss" on the player's part, due to wrongly guessing the location of the warship)

Rules
    1. The player is given an N x N grid, that is populated with T number of war ships
    2. Each war ship occupies two or more cells in a single row or a single column (i.e. 1 cell wide)
    3. The ship is oriented either vertically or horizontally, never diagonally
    4. The player is given X number of bombs initially, which they must use to destroy parts of the ship
    5. Each bombing consumes 1 bomb from the player's inventory
    6. Bombing a cell has several outcomes:
        i) The cell contains part of the enemy warship          -> That part is destroyed and replaced with an 'X'
        ii) The cell contains water                             -> The water is considered bombed and replaced with an '#'
        iii) The cell contains a previously bombed area         -> Cannot be bombed again
    7. Once all the parts of a single ship are bombed (marked 'X'), the ship is considered completely destroyed.

Win Condition: The player wins if all the ships are completely destroyed before bombs run out

Lose Condition: The player loses if bombs run out before destroying all the ships completely

How to Run
    From the command-line, run the project as:
    >> python regame.py
