import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # Parse N
    n = int(input_data[0])
    
    # Parse A
    # A starts from index 1 to N in input_data
    a = []
    for i in range(1, n + 1):
        a.append(int(input_data[i]))
        
    # Calculate the sum of (A_i - 1)
    # This represents the total number of "extra" moves available beyond the mandatory N moves
    # to cover all indices.
    sum_extra = 0
    for val in a:
        sum_extra += (val - 1)
        
    # If the sum of extra moves is odd, Fennec (the first player) wins.
    # If the sum of extra moves is even, Snuke (the second player) wins.
    if sum_extra % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()