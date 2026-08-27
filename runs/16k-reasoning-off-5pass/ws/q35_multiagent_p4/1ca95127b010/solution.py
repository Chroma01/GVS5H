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

    # Check if the number of 1s is the same in S and T
    count_S = S.count('1')
    count_T = T.count('1')
    
    if count_S != count_T:
        print("No")
        return

    # Check the invariant: prefix sums modulo (X + Y)
    # Weight for '0' is Y, weight for '1' is -X
    # P_i = sum_{j=1}^i w(S_j)
    # We need P_i(S) == P_i(T) (mod X+Y) for all i
    
    mod_val = X + Y
    
    current_P_S = 0
    current_P_T = 0
    
    possible = True
    
    for i in range(N):
        char_S = S[i]
        char_T = T[i]
        
        # Update prefix sum for S
        if char_S == '0':
            current_P_S += Y
        else:
            current_P_S -= X
            
        # Update prefix sum for T
        if char_T == '0':
            current_P_T += Y
        else:
            current_P_T -= X
            
        # Check invariant
        if current_P_S % mod_val != current_P_T % mod_val:
            possible = False
            break
            
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == '__main__':
    solve()