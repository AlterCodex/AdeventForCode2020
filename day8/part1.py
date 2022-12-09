"""
--- Day 8: Treetop Tree House ---

The expedition comes across a peculiar patch of tall trees all planted carefully in a grid.
The Elves explain that a previous expedition planted these trees as a reforestation effort.
Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden.
To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input).

For example:

    30373
    25512
    65332
    33549
    35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees
in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge,
 there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

- The top-left 5 is visible from the left and top.
        (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
- The top-middle 5 is visible from the top and right.
- The top-right 1 is not visible from any direction;
        for it to be visible, there would need to only be trees of height 0 between it and an edge.
- The left-middle 5 is visible, but only from the right.
- The center 3 is not visible from any direction;
        for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
- The right-middle 3 is visible from the right.
- In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
- With 16 trees visible on the edge and another 5 visible in the interior,
    a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

To begin, get your puzzle input.
"""


def is_visible_left(tree, max_column, tree_line):
    view_line = 0
    for i in tree_line[:max_column]:
        view_line += 1
        if int(i) >= int(tree):
            return False, view_line
    return True, view_line


def is_visible_right(tree, min_column, tree_line):
    view_line = 0
    for i in tree_line[min_column + 1:]:
        view_line += 1
        if int(i) >= int(tree):
            return False, view_line
    return True, view_line


def is_visible_vertical(tree, row, column, tress):
    transpose = ""
    for i in tress:
        transpose += i[column]
    visible_top, view_line_top = is_visible_left(tree, row, transpose)
    visible_bottom, view_line_bottom = is_visible_right(tree, row, transpose)
    return  visible_top or visible_bottom , view_line_top * view_line_bottom


def count_visible_trees(trees):
    visible_trees = 0
    for i in range(len(trees)):
        for j in range(len(trees[i])):
            left, view_line_left = is_visible_left(trees[i][j], j, trees[i])
            right, view_line_right = is_visible_right(trees[i][j], j, trees[i])
            vertical, view_line_vertical = is_visible_vertical(trees[i][j], i, j, trees)
            if left or right or vertical:
                visible_trees += 1
            else:
                print(f"not visible {trees[i][j]} for {i},{j}")
    return visible_trees


def process(file_name):
    trees = []
    with open(file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()
            trees.append(clean_line)
    return count_visible_trees(trees)


files = {'test': 'test.txt', 'prod': 'input.txt'}

if __name__ == "__main__":
    mode = "test"
    print(process(files[mode]))
