import sys

# Set recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(200005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]
    
    MOD = 998244353
    
    # The problem asks for the number of ways to pair N white vertices with N black vertices
    # in a line of 2N vertices (with fixed edges i -> i+1) such that the resulting graph is strongly connected.
    #
    # The graph is strongly connected if and only if for every cut k (1 <= k < 2N), there is at least one edge
    # going from the set {k+1, ..., 2N} to the set {1, ..., k}.
    # An edge goes from right to left if a White vertex in the right set is paired with a Black vertex in the left set.
    #
    # Let W_R(k) be the set of white vertices in the suffix k+1...2N, and B_R(k) be the set of black vertices in the suffix.
    # The condition fails (graph is disconnected) if all vertices in W_R(k) are paired with vertices in B_R(k).
    # This is only possible if |W_R(k)| <= |B_R(k)|.
    #
    # A known combinatorial result for this specific problem structure (line graph + matching) is that the number of
    # valid matchings is given by the product of terms (w_k - b_k + 1) for all cuts k, where w_k and b_k are the
    # counts of white and black vertices in the suffix starting after the cut.
    # If for any cut, w_k - b_k + 1 <= 0, then the answer is 0.
    #
    # Algorithm:
    # 1. Compute suffix counts of 'W' and 'B' for all positions.
    # 2. Iterate through all cuts k from 0 to 2N-2 (representing the split between index k and k+1).
    # 3. For each cut, let w = count of 'W' in s[k+1:] and b = count of 'B' in s[k+1:].
    # 4. Multiply the answer by max(0, w - b + 1). If the term is <= 0, the answer is 0.
    
    # Precompute suffix counts
    # suffix_w[i] = count of 'W' in s[i:]
    # suffix_b[i] = count of 'B' in s[i:]
    # We use size 2N + 1 to handle the empty suffix at the end easily.
    
    suffix_w = [0] * (2 * n + 1)
    suffix_b = [0] * (2 * n + 1)
    
    current_w = 0
    current_b = 0
    
    # Iterate from right to left to fill suffix counts
    for i in range(2 * n - 1, -1, -1):
        if s[i] == 'W':
            current_w += 1
        else:
            current_b += 1
        suffix_w[i] = current_w
        suffix_b[i] = current_b
        
    ans = 1
    
    # Iterate through all cuts.
    # A cut k (0-indexed) splits the graph into {0, ..., k} and {k+1, ..., 2N-1}.
    # We need to check the condition for the suffix starting at k+1.
    # k ranges from 0 to 2N-2.
    
    for k in range(2 * n - 1):
        w = suffix_w[k+1]
        b = suffix_b[k+1]
        val = w - b + 1
        
        if val <= 0:
            print(0)
            return
        
        ans = (ans * val) % MOD
        
    print(ans)

if __name__ == '__main__':
    solve()