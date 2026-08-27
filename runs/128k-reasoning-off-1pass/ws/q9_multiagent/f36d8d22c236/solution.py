import sys

# Increase recursion depth just in case, though 26 nodes is small.
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n_str = next(iterator)
        N = int(n_str)
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # Map to store the required transformation for each character in S
    # mapping[char_in_S] = char_in_T
    mapping = {}
    
    # Step 1: Check consistency
    # If S[i] == S[j], then T[i] must equal T[j].
    # If S[i] maps to multiple different characters in T, it's impossible.
    for i in range(N):
        u = S[i]
        v = T[i]
        
        if u in mapping:
            if mapping[u] != v:
                print("-1")
                return
        else:
            mapping[u] = v
            
    # Step 2: Check for cycles in the mapping graph
    # The graph consists of characters 'a'-'z'.
    # An edge exists from u to mapping[u] if u is in mapping.
    # We only care about cycles involving characters that are actually in S.
    
    # We use a visited array to detect cycles.
    # States: 0 = unvisited, 1 = visiting (in current recursion stack), 2 = visited
    state = {c: 0 for c in "abcdefghijklmnopqrstuvwxyz"}
    
    def detect_cycle_dfs(u):
        state[u] = 1 # Mark as visiting
        if u in mapping:
            v = mapping[u]
            if state[v] == 1:
                return True # Cycle detected
            if state[v] == 0:
                if detect_cycle_dfs(v):
                    return True
        state[u] = 2 # Mark as visited
        return False

    for char in S:
        if state[char] == 0:
            if detect_cycle_dfs(char):
                print("-1")
                return

    # Step 3: Count operations
    # The number of operations is the number of unique characters in S 
    # that need to be changed (i.e., mapping[c] != c).
    # Each such character requires exactly one operation "replace c with mapping[c]".
    # Even if there are dependencies (chains), the count is simply the number of 
    # distinct source characters that are not fixed points.
    
    operations = 0
    for char in mapping:
        if mapping[char] != char:
            operations += 1
            
    print(operations)

if __name__ == '__main__':
    solve()