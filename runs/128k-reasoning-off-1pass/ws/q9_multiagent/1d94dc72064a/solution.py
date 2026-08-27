import sys

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        
        # We don't necessarily need to store A, we can process on the fly
        # but storing is fine given constraints N <= 2*10^5
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # The game logic for this specific problem (AtCoder ABC 173 D) relies on the parity
    # of the total number of "waste" moves available.
    # A "waste" move is decrementing A_i where i is already in S.
    # The total number of such moves possible is sum(A_i - 1) for all i.
    # If this sum is odd, the first player (Fennec) wins.
    # If this sum is even, the second player (Snuke) wins.
    
    waste_sum = 0
    for x in A:
        waste_sum += (x - 1)
    
    if waste_sum % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()