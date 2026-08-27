import sys

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        # Read N
        n_str = next(iterator)
        N = int(n_str)
        
        # Read sequence A (we need to consume it to advance the iterator, 
        # but the values themselves do not affect the outcome)
        # We just need to ensure we read N integers.
        for _ in range(N):
            next(iterator)
            
    except StopIteration:
        return

    # Game Logic Analysis:
    # The game ends when the set S contains all indices from 1 to N.
    # Each index i must be chosen at least once (when A[i] > 0) to be added to S.
    # Once i is in S, subsequent choices of i only decrement A[i] without changing S.
    # The player who makes the move that completes S (i.e., adds the N-th unique index) wins.
    #
    # If all A[i] == 1 initially:
    #   Players are forced to pick a new index every turn.
    #   The game lasts exactly N moves.
    #   If N is odd, Fennec (1st player) makes the last move (move N). Fennec wins.
    #   If N is even, Snuke (2nd player) makes the last move (move N). Snuke wins.
    #
    # If there exists at least one A[i] > 1:
    #   Players have the option to "waste" a move by decrementing an already collected index.
    #   However, optimal play dictates that the winner is determined solely by the parity of N.
    #   - If N is odd: Fennec can always ensure the game ends on an odd move (her turn).
    #     Even if Snuke tries to waste a move to change parity, Fennec can counter or simply
    #     proceed to collect the next new index, maintaining the advantage.
    #   - If N is even: Snuke can always ensure the game ends on an even move (his turn).
    #     Similarly, Fennec cannot force the game to end on an odd move against optimal play from Snuke.
    #
    # Conclusion: The winner is determined strictly by the parity of N.
    # If N % 2 != 0 -> Fennec wins.
    # If N % 2 == 0 -> Snuke wins.
    
    if N % 2 != 0:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()