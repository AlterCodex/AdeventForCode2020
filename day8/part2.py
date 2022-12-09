"""
--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house:
they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left,
and right from that tree;
stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration.
(If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above;
the proposed tree house has large eaves to keep it dry,
so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees
(one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions.
For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

"""
from day8.part1 import  is_visible_right

def is_visible_left(tree, max_column, tree_line):
    view_line = 0
    for i in range(max_column):
        view_line += 1
        if int(tree_line[max_column-i-1]) >= int(tree):
            return False, view_line
    return True, view_line

def is_visible_top(tree, max_column, tree_line):
    view_line = 0
    for i in range(max_column):
        view_line += 1
        if int(tree_line[max_column-i-1]) >= int(tree):
            return False, view_line
    return True, view_line

def is_visible_bottom(tree, min_column, tree_line):
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
    visible_top, view_line_top = is_visible_top(tree, row, transpose)
    visible_bottom, view_line_bottom = is_visible_bottom(tree, row, transpose)
    return  visible_top or visible_bottom , view_line_top , view_line_bottom



def count_visible_trees(trees):
    visible_trees = 0
    max_scenery_score = 0
    for i in range(len(trees)):
        for j in range(len(trees[i])):
            left, view_line_left = is_visible_left(trees[i][j], j, trees[i])
            right, view_line_right = is_visible_right(trees[i][j], j, trees[i])
            vertical, view_line_top, view_line_down = is_visible_vertical(trees[i][j], i, j, trees)
            if left or right or vertical:
                visible_trees += 1
            scenery_score = view_line_right * view_line_left * view_line_top * view_line_down
            #print(f"view for {trees[i][j]} for {i},{j}, l: {view_line_left}, r:{view_line_right}, t:{view_line_top}, d:{view_line_down} , Scenary score: {scenery_score}")
            if scenery_score > max_scenery_score:
                max_scenery_score = scenery_score
    return visible_trees, max_scenery_score


def process(file_name):
    trees = []
    with open(file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()
            trees.append(clean_line)
    return count_visible_trees(trees)


files = {'test': 'test.txt', 'prod': 'input.txt'}

if __name__ == "__main__":
    mode = "prod"
    print(process(files[mode]))