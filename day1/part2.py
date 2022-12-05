"""
--- Part Two ---
By the time you calculate the answer to the Elves' question,
hey've already realized that the Elf carrying the most Calories of food might eventually run out of snacks.

To avoid this unacceptable situation,
the Elves would instead like to know the total Calories carried by the top three
Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories),
then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories).
The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
"""


def calculate_calories():
    elf = 1
    max_elf = elf
    max_calories = 1
    calculated_calories = 0
    calories_collection = []
    with open("input1.txt", "r") as file:
        for line in file:
            if line != '\n' and line != '':
                calculated_calories += int(line)
            else:
                calories_collection.append(calculated_calories)
                calculated_calories = 0
                elf += 1
    calories_collection.sort(reverse=True)
    max_calories = sum(calories_collection[0:3])

    print(max_elf)
    print(max_calories)


if __name__ == "__main__":
    print(calculate_calories())
