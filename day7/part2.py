"""
--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000.
To run the update, you need unused space of at least 30000000.
You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165;
this means that the size of the unused space must currently be 21618835,
which isn't quite the 30000000 required by the update.

Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However,
directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update.
What is the total size of that directory?
"""
import math

from day7.part1 import files, build_instrucctions, build_graph


def process(file_name):
    instructions = build_instrucctions(file_name)
    root = build_graph(instructions)
    used_size = root.calculate_size()
    free_space = 70000000 - used_size
    need_to_delete =30000000 - free_space
    folders = root.find_folders_with_more_size_than(need_to_delete)
    minimum_size=math.inf
    for folder in folders:
        size = folder.calculate_size()
        if size < minimum_size:
            minimum_size = size
    return minimum_size

if __name__ == "__main__":
    mode = "prod"
    print(process(files[mode]))
