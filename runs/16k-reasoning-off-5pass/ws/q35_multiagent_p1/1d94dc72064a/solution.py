import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N
    n = int(input_data[0])
    
    # Parse A (the next N integers)
    # We don't actually need the values of A for the logic, 
    # but we must consume them to follow the input format correctly.
    # The logic depends only on the parity of N.
    
    # According to the analysis:
    # If N is odd, Fennec (first player) wins.
    # If N is even, Snuke (second player) wins.
    
    if n % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()