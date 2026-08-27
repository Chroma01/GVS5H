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
        
    # Calculate the sum of A
    sum_a = sum(a)
    
    # The winner is determined by the parity of (sum_a + N)
    # If (sum_a + N) is odd, Fennec wins.
    # If (sum_a + N) is even, Snuke wins.
    
    if (sum_a + n) % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == '__main__':
    solve()