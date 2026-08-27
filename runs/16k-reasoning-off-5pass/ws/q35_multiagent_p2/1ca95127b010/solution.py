import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    X = int(input_data[1])
    Y = int(input_data[2])
    S = input_data[3]
    T = input_data[4]
    
    # Count the number of 1s in S and T
    count_S = S.count('1')
    count_T = T.count('1')
    
    # Condition 1: The number of 1s must be the same
    if count_S != count_T:
        print("No")
        return
    
    # Calculate the sum of 1-based indices of 1s in S
    sum_S = 0
    for i, char in enumerate(S):
        if char == '1':
            sum_S += (i + 1)
            
    # Calculate the sum of 1-based indices of 1s in T
    sum_T = 0
    for i, char in enumerate(T):
        if char == '1':
            sum_T += (i + 1)
            
    # Condition 2: The sum of positions of 1s must be congruent modulo gcd(X, Y)
    # The operations change the sum of positions by multiples of X*Y.
    # Thus, the sum modulo gcd(X, Y) is invariant.
    # It is a known result that this condition, along with equal counts, is sufficient.
    import math
    g = math.gcd(X, Y)
    
    if sum_S % g == sum_T % g:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()