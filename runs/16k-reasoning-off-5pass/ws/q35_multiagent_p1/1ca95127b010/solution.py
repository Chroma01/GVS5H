import sys
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

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

    # Count zeros in S and T
    zeros_S = []
    zeros_T = []
    
    for i in range(N):
        if S[i] == '0':
            zeros_S.append(i + 1) # 1-indexed position
        if T[i] == '0':
            zeros_T.append(i + 1) # 1-indexed position
            
    # Condition 1: Number of zeros must be equal
    if len(zeros_S) != len(zeros_T):
        print("No")
        return

    # Condition 2: Positions modulo gcd(X, Y) must match for corresponding zeros
    G = gcd(X, Y)
    
    for z_s, z_t in zip(zeros_S, zeros_T):
        if z_s % G != z_t % G:
            print("No")
            return
            
    print("Yes")

if __name__ == '__main__':
    solve()