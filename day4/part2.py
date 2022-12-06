"""
--- Part Two ---
It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

5-7,7-9 overlaps in a single section, 7.
2-8,3-7 overlaps all of the sections 3 through 7.
6-6,4-6 overlaps in a single section, 6.
2-6,4-8 overlaps in sections 4, 5, and 6.
So, in this example, the number of overlapping assignment pairs is 4.
"""

files = {'test': 'test.txt', 'prod': 'input.txt'}

def does_overlap(section1,section2):
    section_overlap= section1 & section2
    return len(section_overlap)

def find_overlap(mode):
    overlaps = 0
    with open(files[mode], "r") as file:
        for line in file:
            pair1, pair2 = line.strip().split(',')
            lower1, upper1 = pair1.split('-')
            lower2, upper2 = pair2.split('-')
            section1, section2 = set(range(int(lower1),int(upper1)+1)),set(range(int(lower2),int(upper2)+1))
            if does_overlap(section1,section2):
                overlaps += 1
    return overlaps

if __name__ == "__main__":
    print(find_overlap("test"))
    print(find_overlap("prod"))


















