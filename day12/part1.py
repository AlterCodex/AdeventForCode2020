"""
--- Day 12: Hill Climbing Algorithm ---
You try contacting the Elves using your handheld device,
but the river you're following must be too low to get a decent signal.

You ask the device for a heightmap of the surrounding area (your puzzle input).
The heightmap shows the local area from above broken into a grid;
the elevation of each square of the grid is given by a single lowercase letter,
where a is the lowest elevation, b is the next-lowest, and so on up to the highest elevation, z.

Also included on the heightmap are marks for your current position (S) and the location that
should get the best signal (E).
Your current position (S) has elevation a, and the location that should get the best signal (E) has elevation z.

You'd like to reach E, but to save energy, you should do it in as few steps as possible.
During each step, you can move exactly one square up, down, left, or right.
To avoid needing to get out your climbing gear,
the elevation of the destination square can be at most one higher than the elevation of your current square;
that is, if your current elevation is m, you could step to elevation n, but not to elevation o.
(This also means that the elevation of the destination square can be much lower than the elevation of your current square.)

For example:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi

Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right,
 but eventually you'll need to head toward the e at the bottom. From there, you can spiral around to the goal:

v..v<<<<
>v.vv<<^
.>vv>E^^
..v>>>^^
..>>>>>^

In the above diagram,
 the symbols indicate whether the path exits each square moving up (^), down (v), left (<), or right (>).
The location that should get the best signal is still E, and . marks unvisited squares.

This path reaches the goal in 31 steps, the fewest possible.

What is the fewest steps required to move from your current position to the location that should get the best signal?

--- Part Two ---
As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail.
The beginning isn't very scenic, though; perhaps you can find a better starting point.

To maximize exercise while hiking, the trail should start as low as possible: elevation a.
The goal is still the square marked E.
However, the trail should still be direct, taking the fewest steps to reach its goal.
So, you'll need to find the shortest path from any square at elevation a to the square marked E.

Again consider the example from above:

Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
Now, there are six choices for starting position (five marked a,
plus the square marked S that counts as being at elevation a).
If you start at the bottom-left square, you can reach the goal most quickly:

...v<<<<
...vv<<^
...v>E^^
.>v>>>^^
>^>>>>>^
This path reaches the goal in only 29 steps, the fewest possible.

What is the fewest steps required to move starting from any square with elevation a to the location that should get the best signal?

"""
import math
import queue

from day10.part1 import files


class Node:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.childs = []
        self.height = height

    def build_childs(self, mountain_height_map, nodes):
        if self.x - 1 >= 0:
            node_height = mountain_height_map[self.x - 1][self.y]
            self.append_child(node_height, nodes, self.x - 1, self.y)
        if self.y - 1 >= 0:
            node_height = mountain_height_map[self.x][self.y - 1]
            self.append_child(node_height, nodes, self.x, self.y - 1)
        if self.x + 1 < len(mountain_height_map):
            node_height = mountain_height_map[self.x + 1][self.y]
            self.append_child(node_height, nodes, self.x + 1, self.y)
        if self.y + 1 < len(mountain_height_map[self.x]):
            node_height = mountain_height_map[self.x][self.y + 1]
            self.append_child(node_height, nodes, self.x, self.y + 1)

    def append_child(self, node_height, nodes, x, y):
        if (x, y) not in nodes:
            nodes[(x, y)] = Node(x, y, node_height)
        if (node_height - self.height) <= 1:
            self.childs.append(nodes[(x, y)])

    def __repr__(self):
        return f"NODE({self.x}, {self.y}, {self.height})"


def to_int(height: chr) -> int:
    if height == 'S':
        height = 'a'
    elif height == 'E':
        height = 'z'
    return ord(height) - ord('a')


def build(file_name):
    mountain_map = []
    start = None
    end = None
    with open(file_name, 'r') as file:
        l = 0
        for line in file:
            j = 0
            mountain_map.append([])
            clean_line = line.strip()
            for height in clean_line:
                if height == 'S':
                    start = (l, j)
                if height == 'E':
                    end = (l, j)
                j += 1
                mountain_map[l].append(to_int(height))
            l += 1
    return mountain_map, start, end


def make_graph(mountain_height_map):
    nodes = {}
    for i in range(len(mountain_height_map)):
        for j in range(len(mountain_height_map[i])):
            if (i, j) not in nodes:
                nodes[(i, j)] = Node(i, j, mountain_height_map[i][j])
            nodes[(i, j)].build_childs(mountain_height_map, nodes)
    return nodes


def find_min_distance_brute_force(graph, start, end, visited, steps):
    print(f"Node {start})")
    steps += 1
    child_distance = []
    node = graph[start]
    if end == (node.x, node.y):
        print(f"end {steps}")
        return len(visited)
    if start in visited or len(node.childs) == 0:
        return math.inf
    else:
        for i in node.childs:
            child_distance.append(find_min_distance_brute_force(graph, (i.x, i.y), end, visited + [start], steps))
        return sorted(child_distance)[0]


def find_min_distance_fsb(graph, start, end, visited, steps):
    queue = [start]
    visited[start] = 0
    shortest_path_length = float('inf')
    while not len(queue) == 0:
        node_cords = queue.pop(0)
        steps = visited[node_cords]
        next_steps = steps + 1
        if node_cords == end:
            shortest_path_length = min(shortest_path_length, steps)
        else:
            for i in graph[node_cords].childs:
                eval_node = (i.x, i.y)
                if eval_node not in visited or visited[eval_node] > next_steps:
                    queue.append((i.x, i.y))
                    visited[i.x, i.y] = next_steps
    return shortest_path_length


def find_all_nodes_in_height(graph, height):
    for i in graph:
        if graph[i].height == height:
            yield i
    pass


if __name__ == "__main__":
    mode = "prod"

    mountain_map, start, end = build(files[mode])
    graph = make_graph(mountain_map)
    distance = find_min_distance_fsb(graph, start, end, {}, 0)  # part1
    print(f'start: {start}, end: {end}, distance: {distance}')
    distances = []
    for possible in find_all_nodes_in_height(graph, 0):  # part2
        distances.append(find_min_distance_fsb(graph, possible, end, {}, 0))
    min_distance = min(distances)
    print(f'start: {possible}, end: {end}, distance: {min_distance}')