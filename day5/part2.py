"""
--- Part Two ---
As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away.
The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning,
leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]
[N] [C]
[Z] [M] [P]
 1   2   3
However,
the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order,
resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3
Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3
Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3
In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes,
update your simulation so that the Elves know where they should stand to be ready to unload the final supplies.
After the rearrangement procedure completes, what crate ends up on top of each stack?

"""

files = {'test': 'test.txt', 'prod': 'input.txt'}


def build_stack(mode):
    building_stack = True
    stacks = {}
    rules = []
    with open(files[mode], "r") as file:
        for line in file:
            if building_stack:
                if line.strip() == "":
                    building_stack = False
                else:
                    for i in range(len(line)):
                        if line[i].isalpha():
                            if i // 4 + 1 not in stacks:
                                stacks[i // 4 + 1] = []
                            stacks[i // 4 + 1].insert(0, line[i])
            else:
                rules.append(line.strip())
        return stacks, rules


def apply_rules(stacks, rules):
    for rule in rules:
        conditions = rule.split(' ')
        quantity, origin, destination = int(conditions[1]), int(conditions[3]), int(conditions[5])
        if destination not in stacks:
            stacks[destination] = []
        value = []
        for i in range(quantity):
            value.append(stacks[origin].pop())
        value.reverse()
        stacks[destination].extend(value)
    return stacks


def result(stacks):
    keys = sorted(stacks.keys())
    res = ""
    for k in keys:
        res = res + stacks[k].pop()
    return res


if __name__ == "__main__":
    stacks, rules = build_stack("prod")
    print(result(apply_rules(stacks, rules)))
