"""
--- Part Two ---
The Elf finishes helping with the tent and sneaks back over to you.
 "Anyway, the second column says how the round needs to end:
 X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way,
but now you need to figure out what shape to choose so the round ends as indicated.
The example above now goes like this:

In the first round, your opponent will choose Rock (A),
and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.
Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.
"""

def play():

    win_map = {
        'A': 'C',
        'B': 'A',
        'C': 'B'}
    lose_map = {
        'C': 'A',
        'A': 'B',
        'B': 'C'}
    win_score = {
        'X': 0,
        'Y': 3,
        'Z': 6}
    score_shape = {
        'A': 1,
        'B': 2,
        'C': 3}

    score = 0
    with open("input.txt", "r") as file:

        for line in file:
            line = str(line).strip()
            play1 = line[0]
            play2 = line[-1]
            shape = play1
            if play2 == 'X': #lose
                shape = win_map[play1]
            elif play2 == 'Z': #win
                shape = lose_map[play1]
            score += score_shape[shape] + win_score[play2]





    print(score)


if __name__ == "__main__":
    print(play())
