import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        Y = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # Count 1s in S and T
    count_S = S.count('1')
    count_T = T.count('1')
    
    if count_S != count_T:
        print("No")
        return

    # Calculate sum of 1-based indices of 1s
    sum_S = 0
    sum_T = 0
    
    for i in range(N):
        if S[i] == '1':
            sum_S += (i + 1)
        if T[i] == '1':
            sum_T += (i + 1)
            
    # Check the invariant: sum of indices modulo (X * Y) must be equal
    mod_val = X * Y
    
    if (sum_S % mod_val) == (sum_T % mod_val):
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()