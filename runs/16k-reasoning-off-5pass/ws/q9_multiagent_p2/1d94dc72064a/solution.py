import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N
    n = int(input_data[0])
    
    # Parse A (we need to consume it, but its values don't affect the winner)
    # The problem guarantees N integers follow.
    # We can just ignore the values of A for the logic.
    
    # The logic derived is:
    # If N is odd, Fennec wins.
    # If N is even, Snuke wins.
    # This holds true regardless of the values in A (as long as A_i >= 1).
    
    if n % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()