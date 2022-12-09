"""
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input).
For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files).
The outermost directory is called /.
You can navigate around the filesystem,
moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output,
lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory),
a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion.
To do this, you need to determine the total size of each directory.
The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly.
(Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596),
plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.

As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes.
In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584).
(As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
"""


class Directory:

    def __init__(self, name):
        self._name = name
        self._childs = []
        self._size = None
        self._parent = None

    def set_parent(self, parent):
        self._parent = parent

    def parent(self):
        return self._parent

    def name(self):
        return self._name

    def add_child(self, child):
        self._childs.append(child)

    def go_root(self):
        folder = self
        while folder.parent() is not None:
            folder = folder.parent()
        return folder

    def calculate_size(self):
        if self._size is None:
            return sum(child.calculate_size() for child in self._childs)
        else:
            return self._size

    def set_size(self, size):
        self._size = size

    def is_directory(self):
        return self._size is None

    def get_folder_by_name(self, name):
        if name == self._name:
            return self
        elif len(self._childs) == 0:
            return None
        else:
            for child in self._childs:
                found = child.get_folder_by_name(name)
                if found is not None:
                    return found

    def get_child_by_name(self, name):
        if len(self._childs) == 0:
            return None
        else:
            for child in self._childs:
                if child.name() == name:
                    return child

    def has_child(self, name):
        for child in self._childs:
            child.name() == name

    def find_folders_with_less_size_than(self, most_size):
        folders_with_less_size_than = []
        if self.is_directory() and  self.calculate_size() < most_size:
            folders_with_less_size_than.append(self)
        for child in self._childs:
            if child.is_directory:
                temps_folder = child.find_folders_with_less_size_than(most_size)
                folders_with_less_size_than.extend(temps_folder)
        return folders_with_less_size_than

    def find_folders_with_more_size_than(self, at_least_size):
        folders_with_more_size_than = []
        if self.is_directory() and  self.calculate_size() > at_least_size:
            folders_with_more_size_than.append(self)
        for child in self._childs:
            if child.is_directory:
                temps_folder = child.find_folders_with_more_size_than(at_least_size)
                folders_with_more_size_than.extend(temps_folder)
        return folders_with_more_size_than

    def __repr__(self):
        return "<Folder %s, %s, %s >" %(self._name, self._size, self._childs)

class Instruction:

    def __init__(self, command, argument):
        self._command = command
        self._argument = argument
        self._results = []

    def command(self):
        return self._command

    def argument(self):
        return self._argument

    def results(self):
        return self._results

    def add_result(self, result):
        self._results.append(result)

    def append_result(self, result):
        self._results.append(result)

    def __repr__(self):
        return "Instruction($ %s, %s)" % (self._command, self._argument)


def build_graph(instructions: [Instruction]):
    root = Directory("/")
    current_directory = root
    for instruction in instructions:
        if instruction.command() == 'cd':
            if instruction.argument() == '..':
                current_directory = current_directory.parent()
            elif instruction.argument() == '/':
                current_directory = current_directory.go_root()
            else:
                found_folder = current_directory.get_child_by_name(instruction.argument())
                if found_folder is not None:
                    current_directory = found_folder
                else:
                    new_child = Directory(instruction.argument())
                    new_child.set_parent(current_directory)
                    current_directory.add_child(new_child)
                    current_directory = new_child
        elif instruction.command() == 'ls':
            for result in instruction.results():
                value, name = result.split(' ')
                if not current_directory.has_child(name):
                    new_child = Directory(name)
                    new_child.set_parent(current_directory)
                    if value != 'dir':
                        size = int(value)
                        new_child.set_size(size)
                    current_directory.add_child(new_child)
    return current_directory.go_root()


def process(file_name):
    instructions = build_instrucctions(file_name)
    root = build_graph(instructions)
    folders = root.find_folders_with_less_size_than(100000)

    return sum(folder.calculate_size() for folder in folders)


def build_instrucctions(file_name):
    instructions = []
    actual_instruction = None
    with open(file_name, 'r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line.startswith('$'):
                splitted_line = clean_line.split(' ')
                if splitted_line[1] == 'cd':
                    actual_instruction = Instruction(splitted_line[1], splitted_line[2])
                else:
                    actual_instruction = Instruction(splitted_line[1], None)
                instructions.append(actual_instruction)
            else:
                actual_instruction.add_result(clean_line)
    return instructions


files = {'test': 'test.txt', 'prod': 'input.txt'}

if __name__ == "__main__":
    mode = "prod"
    print(process(files[mode]))
