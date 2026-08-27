import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    
    # Count piles with A_i == 1 and sum of (A_i - 1) for piles with A_i >= 2
    ones = 0
    sum_rem = 0  # Sum of (A_i - 1) for piles with A_i >= 2
    count_big = 0  # Number of piles with A_i >= 2
    
    for x in a:
        if x == 1:
            ones += 1
        else:
            sum_rem += x - 1
            count_big += 1
    
    # Case 1: All piles are 1. Game lasts exactly N moves.
    if count_big == 0:
        print("Fennec" if n % 2 == 1 else "Snuke")
        return
    
    # Case 2: Exactly one pile with value >= 2.
    # The first player can control the parity of the game length by choosing
    # how many times to revisit the big pile on their first move.
    if count_big == 1:
        print("Fennec")
        return
    
    # Case 3: Multiple piles with value >= 2.
    # The game is equivalent to a parity game on the total number of "excess" moves
    # (sum of A_i - 1 for big piles) plus the mandatory N first-touches.
    # The winner is determined by the parity of (sum(A_i) - N).
    # Since sum(A_i) - N = sum_rem + ones - count_big + count_big = sum_rem + ones,
    # we check the parity of sum_rem + ones.
    if (sum_rem + ones) % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    solve()