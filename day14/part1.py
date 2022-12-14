"""
--- Day 14: Regolith Reservoir ---
The distress signal leads you to a giant waterfall! Actually,
hang on - the signal seems like it's coming from the waterfall itself,
and that doesn't make any sense. However, you do notice a little path that leads behind the waterfall.

Correction: the distress signal leads you behind a giant waterfall! There seems to be a large cave system here,
and the signal definitely leads further inside.

As you begin to make your way deeper underground, you feel the ground rumble for a moment.
Sand begins pouring into the cave!
If you don't quickly figure out where the sand is going, you could quickly become trapped!

Fortunately, your familiarity with analyzing the path of falling material will come in handy here.
You scan a two-dimensional vertical slice of the cave above you (your puzzle input)
 and discover that it is mostly air with structures made of rock.

Your scan traces the path of each solid rock structure and reports the x,y coordinates that form the shape of the path,
where x represents distance to the right and y represents distance down.
Each path appears as a single line of text in your scan.
After the first point of each path,
each point indicates the end of a straight horizontal or vertical line to be drawn from the previous point. For example:

498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
This scan means that there are two paths of rock; the first path consists of two straight lines,
and the second path consists of three straight lines.
(Specifically,
the first path consists of a line of rock from 498,4
through 498,6 and another line of rock from 498,6 through 496,6.)

The sand is pouring into the cave from point 500,0.

Drawing rock as #, air as ., and the source of the sand as +, this becomes:


  4     5  5
  9     0  0
  4     0  3
0 ......+...
1 ..........
2 ..........
3 ..........
4 ....#...##
5 ....#...#.
6 ..###...#.
7 ........#.
8 ........#.
9 #########.

Sand is produced one unit at a time,
and the next unit of sand is not produced until the previous unit of sand comes to rest.
A unit of sand is large enough to fill one tile of air in your scan.

A unit of sand always falls down one step if possible.
If the tile immediately below is blocked (by rock or sand),
the unit of sand attempts to instead move diagonally one step down and to the left.

If that tile is blocked, the unit of sand attempts to instead move diagonally one step down and to the right.
Sand keeps moving as long as it is able to do so, at each step trying to move down,
 then down-left, then down-right. If all three possible destinations are blocked,
  the unit of sand comes to rest and no longer moves,
  at which point the next unit of sand is created back at the source.

So, drawing sand that has come to rest as o, the first unit of sand simply falls straight down and then stops:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
......o.#.
#########.

The second unit of sand then falls straight down, lands on the first one, and then comes to rest to its left:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
........#.
.....oo.#.
#########.
After a total of five units of sand have come to rest, they form this pattern:

......+...
..........
..........
..........
....#...##
....#...#.
..###...#.
......o.#.
....oooo#.
#########.
After a total of 22 units of sand:

......+...
..........
......o...
.....ooo..
....#ooo##
....#ooo#.
..###ooo#.
....oooo#.
...ooooo#.
#########.
Finally, only two more units of sand can possibly come to rest:

......+...
..........
......o...
.....ooo..
....#ooo##
...o#ooo#.
..###ooo#.
....oooo#.
.o.ooooo#.
#########.
Once all 24 units of sand shown above have come to rest, all further sand flows out the bottom,
falling into the endless void. Just for fun, the path any new sand takes before falling forever is shown here with ~:

.......+...
.......~...
......~o...
.....~ooo..
....~#ooo##
...~o#ooo#.
..~###ooo#.
..~..oooo#.
.~o.ooooo#.
~#########.
~..........
~..........
~..........

Using your scan, simulate the falling sand.
How many units of sand come to rest before sand starts flowing into the abyss below?
"""
import os
from time import sleep

from utils.files import files


def build(file_name, part=1):
    with open(file_name, "r") as file:
        rocks = []
        for line in file:
            rocks.append([x.strip() for x in line.strip().split('->')])
        max_x = 0
        max_y = 0
        clean_coordinates = []
        for rock_line in rocks:
            rocks_line = []
            for rock in rock_line:
                x, y = int(rock.split(',')[0]), int(rock.split(',')[1])
                if x >= max_x:
                    max_x = x
                if y >= max_y:
                    max_y = y
                rocks_line.append((x, y))
            clean_coordinates.append(rocks_line)
        print(clean_coordinates)
        cave_map = []
        for i in range(max_y + part):
            cave_map.append(['.'] * (max_x + 1000))
        for i in range(len(clean_coordinates)):
            for coordinates in range(len(clean_coordinates[i]) - 1):
                start = min([clean_coordinates[i][coordinates], clean_coordinates[i][coordinates + 1]])
                end = max([clean_coordinates[i][coordinates], clean_coordinates[i][coordinates + 1]])
                if start[0] == end[0]:
                    for j in range(start[1], end[1] + 1):
                        cave_map[j][start[0]] = '#'
                else:
                    for j in range(start[0], end[0] + 1):
                        cave_map[start[1]][j] = '#'

        if part == 2:
            cave_map.append(['#'] * (max_x + 1000))
        cave_map[0][500] = '+'
        for line in cave_map:
            print(line[0] + ''.join(line[300:]))
        print()
        return cave_map


def is_air(space):
    return space == '.'


def is_rock_or_sand(space):
    return space == '#' or space == 'o'


def simulate(cave_map, part=1):
    turns = 0
    while True:
        print()
        turns += 1

        column, row = 500, 0
        can_move = True
        while can_move:
            if row + 1 >= len(cave_map):
                return turns - 1
            if is_air(cave_map[row + 1][column]):
                row, column = row + 1, column
            elif is_rock_or_sand(cave_map[row + 1][column]):
                if is_air(cave_map[row + 1][column - 1]):
                    row, column = row + 1, column - 1
                elif is_air(cave_map[row + 1][column + 1]):
                    row, column = row + 1, column + 1
                else:
                    can_move = False
                    if part == 2 and cave_map[row][column] == '+':
                        cave_map[row][column] = "o"
                        return turns + 1
                    cave_map[row][column] = "o"
      #  os.system('cls')
      #  for line in cave_map:
      #      print(''.join(line[350:600]))


if __name__ == "__main__":
    mode = "prod"
    part = 2
    cave_map = build(files[mode], part)
    arena = simulate(cave_map, part)
    sand = 0
    if part == 2:
        for row in cave_map:
            for column in row:
                if column == 'o':
                    sand += 1
    if part == 2:
        print(sand)
    else:
        print(arena)
