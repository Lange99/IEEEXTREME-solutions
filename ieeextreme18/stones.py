# Stones -> 11% of the test cases passed.
# Time limit: 2500 ms
# Memory limit: 256 MB
#
# Alice and Bob are playing a game with red and blue stones. Each has an initial amount of red and blue stones,
# and they know each other's amounts. The game is played in turns, where each turn involves the following steps:
#
# 1. Player A chooses a color (red or blue) and writes it down.
# 2. Player B tries to guess the chosen color:
#    - If B guesses correctly, A loses one stone of that color.
#    - If B guesses incorrectly, B loses one stone of that color.
#
# The game alternates roles each turn: Alice takes on the role of A in the first turn and Bob in the second turn,
# then they alternate. The game ends when any player loses their last stone of any color, resulting in their loss.
#
# The goal is to calculate the probability that Alice will win the game, assuming both players maximize their chances
# of winning, regardless of their opponent's moves.
#
# Input:
# - The first line contains four integers:
#   - R1 and B1: the number of red and blue stones for Alice.
#   - R2 and B2: the number of red and blue stones for Bob.
#
# Output:
# - Output a single real number representing the probability that Alice wins the game.
# - The result should have a relative or absolute error of at most 10^-6 to be considered correct.
#
# Constraints:
# - 1 ≤ R1, R2 ≤ 40
# - 1 ≤ B1, B2 ≤ 40
#
# Notes:
# - Both players aim to maximize their chances of winning.
# - The probability calculation involves analyzing all possible moves and outcomes across both colors and players.


def solve(R1, B1, R2, B2):
    # dp[r1][b1][r2][b2] will store the probability of Alice winning
    dp = [[[[None for _ in range(41)] for _ in range(41)] for _ in range(41)] for _ in range(41)]

    def probability(r1, b1, r2, b2):
        # Base cases
        if r1 == 0 or b1 == 0:
            return 0.0  # Alice loses if she runs out of any color
        if r2 == 0 or b2 == 0:
            return 1.0  # Alice wins if Bob runs out of any color

        # If we have already calculated this state, return the stored value
        if dp[r1][b1][r2][b2] is not None:
            return dp[r1][b1][r2][b2]

        # Alice chooses optimally to maximize her winning probability
        p_red = r1 / (r1 + b1)
        p_blue = b1 / (r1 + b1)

        prob_if_red = p_red * (1 - probability(r1 - 1, b1, r2, b2)) if r1 > 0 else 0
        prob_if_blue = p_blue * (1 - probability(r1, b1 - 1, r2, b2)) if b1 > 0 else 0

        # Calculate the probability of Alice winning considering Bob's optimal guess
        prob_as_a = prob_if_red + prob_if_blue

        # Bob's turn as A, Alice guesses optimally
        p_red = r2 / (r2 + b2)
        p_blue = b2 / (r2 + b2)

        prob_if_red = p_red * (1 - probability(r1, b1, r2 - 1, b2)) if r2 > 0 else 0
        prob_if_blue = p_blue * (1 - probability(r1, b1, r2, b2 - 1)) if b2 > 0 else 0

        prob_as_b = prob_if_red + prob_if_blue

        # Average the probabilities since turns alternate
        prob = 0.5 * (prob_as_a + prob_as_b)

        # Store the result in dp array
        dp[r1][b1][r2][b2] = prob
        return prob

    # Start the game with Alice's turn
    return probability(R1, B1, R2, B2)


# Input handling
R1, B1, R2, B2 = map(int, input().split())
print(f"{solve(R1, B1, R2, B2):.9f}")
