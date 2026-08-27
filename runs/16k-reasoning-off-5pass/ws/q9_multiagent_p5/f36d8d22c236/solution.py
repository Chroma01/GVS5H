import sys

# Increase recursion depth just in case, though we use an iterative approach.
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]
    t = input_data[2]

    # Mapping array: mapping[char_code] = target_char_code
    # Initialize with -1
    mapping = [-1] * 26
    
    # Step 1: Build the mapping and check for consistency
    # If S[i] == S[j], then T[i] must equal T[j]
    # We store the first seen target for each source character.
    # If we see the source again, the target must match.
    
    possible = True
    for i in range(n):
        u = ord(s[i]) - ord('a')
        v = ord(t[i]) - ord('a')
        
        if mapping[u] == -1:
            mapping[u] = v
        else:
            if mapping[u] != v:
                possible = False
                break
    
    if not possible:
        print("-1")
        return

    # Step 2: Identify unique characters in S and determine which need change
    # A character c needs change if mapping[c] != c
    # We only care about characters present in S.
    
    chars_in_s = set()
    for char in s:
        chars_in_s.add(char)
    
    # Count how many unique characters in S need to be changed
    # and prepare the graph for cycle detection
    nodes_to_process = []
    for char_code in range(26):
        if char_code in chars_in_s:
            target_code = mapping[char_code]
            if target_code != char_code:
                nodes_to_process.append(char_code)
    
    # Step 3: Detect cycles in the functional graph restricted to nodes_to_process
    # Since each node has exactly one outgoing edge (mapping), we can detect cycles.
    # We only care about cycles formed by nodes that actually need to change.
    # A self-loop (mapping[c] == c) is not in nodes_to_process, so we ignore it.
    
    visited = [False] * 26
    cycle_count = 0
    
    for start_node in nodes_to_process:
        if visited[start_node]:
            continue
        
        # Traverse the path
        curr = start_node
        path = []
        
        while not visited[curr]:
            visited[curr] = True
            path.append(curr)
            curr = mapping[curr]
            
            # If we hit a node that is not in our 'nodes_to_process' list, 
            # it means the chain leads to a character that doesn't need change 
            # (either it's a fixed point or not in S). 
            # However, we must ensure we don't count a cycle that includes 
            # a fixed point or a node not in S.
            # But wait, if mapping[curr] != curr, then curr MUST be in nodes_to_process 
            # because we built nodes_to_process based on mapping[c] != c.
            # Exception: If mapping[curr] points to a node NOT in S?
            # If mapping[curr] points to a node not in S, that target node is not in nodes_to_process.
            # So the chain stops there. No cycle can be formed involving a node not in S 
            # because the cycle must consist of nodes that map to each other.
            # If a node maps to something outside the set, it can't be part of a cycle 
            # within the set.
            
            # Check if we hit a node already in the current path (cycle)
            if curr in path:
                cycle_count += 1
                break
            # If we hit a node that was visited in a previous traversal, 
            # it means this path merges into an already processed component.
            # Since that component was already checked for cycles, we don't count a new one.
            # And since we only traverse unvisited nodes, we won't re-process.
            # But wait, if we hit a visited node that is NOT in current path, 
            # we just stop.
            if visited[curr]:
                # This node was visited in a previous iteration. 
                # It belongs to a component already analyzed. 
                # Since we are traversing from an unvisited start_node, 
                # and we hit a visited node, we have merged into an existing tree/cycle.
                # No new cycle is formed here.
                break

    # Step 4: Calculate result
    # Result = (Number of unique chars in S that need change) + (Number of cycles)
    ans = len(nodes_to_process) + cycle_count
    print(ans)

if __name__ == '__main__':
    solve()