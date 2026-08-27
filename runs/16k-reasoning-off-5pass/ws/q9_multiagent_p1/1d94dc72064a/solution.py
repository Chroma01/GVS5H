import sys

def solve():
    # Read all input from standard input
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N
    iterator = iter(input_data)
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        # The sequence A follows, but its values do not affect the winner
        # under optimal play. We simply consume the iterator to skip them 
        # or ignore them since the logic depends only on N.
        # We do not need to explicitly iterate through A_i for the solution.
        
        # Game Logic Analysis:
        # The game ends when the set S contains all indices {1, 2, ..., N}.
        # This requires exactly N "useful" moves (choosing an index i not in S).
        # Players can also make "wasted" moves (choosing an index i already in S)
        # as long as A_i >= 1.
        # The winner is determined by the parity of the total number of moves M.
        # - If M is odd, Fennec (who starts first) makes the last move and wins.
        # - If M is even, Snuke makes the last move and wins.
        #
        # Under optimal play:
        # 1. If N is odd:
        #    The minimum number of moves to fill S is N (odd).
        #    Fennec can always ensure the total number of moves M is odd.
        #    (If Snuke tries to waste a move to change parity, Fennec can counter
        #     or the structure of the game forces the parity to remain odd).
        #    Therefore, Fennec wins.
        #
        # 2. If N is even:
        #    The minimum number of moves to fill S is N (even).
        #    Snuke can always ensure the total number of moves M is even.
        #    (Snuke can mirror Fennec's moves or choose to waste moves to maintain
        #     even parity).
        #    Therefore, Snuke wins.
        #
        # Conclusion: The winner is determined solely by the parity of N.
        
        if N % 2 != 0:
            print("Fennec")
        else:
            print("Snuke")
            
    except StopIteration:
        pass

if __name__ == '__main__':
    solve()