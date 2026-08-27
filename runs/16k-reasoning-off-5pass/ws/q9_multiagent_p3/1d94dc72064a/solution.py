import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        total_sum = sum(A)
        
        # The game ends when the set S contains all indices from 1 to N.
        # The total number of moves M determines the winner:
        # If M is odd, Fennec (1st player) wins.
        # If M is even, Snuke (2nd player) wins.
        #
        # Analysis shows that the parity of the total moves M is determined by:
        # M % 2 == (sum(A) + N) % 2
        # Therefore, Fennec wins if (sum(A) + N) is odd.
        
        if (total_sum + N) % 2 == 1:
            print("Fennec")
        else:
            print("Snuke")
            
    except StopIteration:
        pass

if __name__ == '__main__':
    solve()