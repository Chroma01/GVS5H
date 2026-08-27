import sys

# Increase recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    S = input_data[1]
    
    MOD = 998244353
    
    # If the last character is 'B', vertex 2N is Black.
    # Vertex 2N has no outgoing base edge (path ends at 2N)
    # and no outgoing added edge (since it's Black).
    # Thus, it's a sink, and the graph cannot be strongly connected.
    if S[-1] == 'B':
        print(0)
        return

    # Map S to values: W -> 1, B -> -1
    # Compute prefix sums
    # P[0] = 0
    # P[i] = sum of first i values
    # We need P[0]...P[2N-1] to find the minimums for cyclic shifts.
    # Note: P[2N] will be 0 since there are N Ws and N Bs.
    
    vals = []
    for char in S:
        if char == 'W':
            vals.append(1)
        else:
            vals.append(-1)
            
    prefix_sum = 0
    min_prefix = 0
    # We store prefix sums P[0] to P[2N-1]
    # P[0] is 0.
    # P[i] is sum(vals[0]...vals[i-1])
    
    # Let's compute all prefix sums P[0]...P[2N]
    # P[0] = 0
    # P[k] = P[k-1] + vals[k-1]
    
    P = [0] * (2 * N + 1)
    for i in range(1, 2 * N + 1):
        P[i] = P[i-1] + vals[i-1]
        
    # The number of cyclic shifts with non-negative partial sums
    # is equal to the number of indices k in {0, ..., 2N-1} such that P[k] is minimal.
    # Note: We look at P[0]...P[2N-1]. P[2N] is always 0 and equals P[0].
    # The condition for a shift starting after index k (i.e., using vals[k], vals[k+1]...)
    # to have non-negative partial sums is that P[k] is the minimum of P[0]...P[2N-1].
    
    # Find minimum in P[0]...P[2N-1]
    min_val = min(P[:2*N])
    
    # Count occurrences of min_val in P[0]...P[2N-1]
    K = 0
    for i in range(2 * N):
        if P[i] == min_val:
            K += 1
            
    # The number of valid pairings is N! * K / (2N)
    # We need to compute this modulo 998244353
    
    # Compute N!
    fact_n = 1
    for i in range(1, N + 1):
        fact_n = (fact_n * i) % MOD
        
    # Compute modular inverse of 2N
    # Using Fermat's Little Theorem: a^(MOD-2) % MOD is the inverse
    inv_2N = pow(2 * N, MOD - 2, MOD)
    
    ans = (fact_n * K) % MOD
    ans = (ans * inv_2N) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()