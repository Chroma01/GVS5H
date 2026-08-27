import sys

# Increase recursion depth just in case, though 26 nodes is small
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # Check consistency and build the mapping
    # Constraint: If S[i] == S[j], then T[i] must == T[j]
    # This implies that for a specific character 'c' in S, 
    # it must always map to the same character in T.
    
    mapping = {}
    for i in range(N):
        s_char = S[i]
        t_char = T[i]
        
        if s_char == t_char:
            continue
        
        if s_char in mapping:
            if mapping[s_char] != t_char:
                print("-1")
                return
        else:
            mapping[s_char] = t_char

    # Now we have a functional graph where each node (char in S) has at most one outgoing edge.
    # We need to check for cycles. Since the graph is functional (out-degree <= 1),
    # a cycle exists if we can traverse from a node and return to it.
    # Note: Self-loops (s_char -> s_char) are not in our mapping because we skipped s_char == t_char.
    # So any cycle must be of length >= 2.
    
    visited = [False] * 26
    rec_stack = [False] * 26
    char_to_idx = {chr(ord('a') + i): i for i in range(26)}
    
    def has_cycle(u_char):
        u_idx = char_to_idx[u_char]
        if visited[u_idx]:
            return False
        if rec_stack[u_idx]:
            return True
        
        visited[u_idx] = True
        rec_stack[u_idx] = True
        
        if u_char in mapping:
            v_char = mapping[u_char]
            if has_cycle(v_char):
                return True
        
        rec_stack[u_idx] = False
        return False

    # Check for cycles in all nodes that have an outgoing edge
    for char in mapping:
        if has_cycle(char):
            print("-1")
            return

    # If no cycles, the answer is simply the number of edges (operations)
    # because we can order them topologically (reverse topological sort) to execute them.
    # Each edge represents one operation.
    print(len(mapping))

if __name__ == '__main__':
    solve()