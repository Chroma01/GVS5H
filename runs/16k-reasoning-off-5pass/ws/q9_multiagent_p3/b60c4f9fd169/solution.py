import sys
from collections import deque

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        K = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    n = len(S)
    m = len(T)

    # If lengths differ by more than K, it's impossible (since each op changes length by at most 1)
    if abs(n - m) > K:
        print("No")
        return

    # BFS State: (index_in_S, index_in_T, cost)
    # We use a set to keep track of visited states to avoid cycles and redundant work
    # visited = set of (i, j)
    
    # Optimization: We only care about states where cost <= K.
    # Also, we can prune if |i - j| > K because the minimum operations to bridge the gap is |i-j|.
    # However, the condition `cost + max(n-i, m-j) > K` covers the remaining length constraint effectively.
    
    start_node = (0, 0)
    # Deque for 0-1 BFS: stores tuples (i, j, cost)
    queue = deque([(0, 0, 0)])
    visited = {start_node}
    
    # Directions logic embedded in the loop:
    # If S[i] == T[j], we can match them with cost 0 -> (i+1, j+1)
    # If S[i] != T[j], we have three options with cost 1:
    #   1. Replace S[i] with T[j] -> (i+1, j+1)
    #   2. Delete S[i] -> (i+1, j)
    #   3. Insert T[j] -> (i, j+1)
    
    while queue:
        i, j, c = queue.popleft()
        
        # If we reached the end
        if i == n and j == m:
            print("Yes")
            return
        
        # Pruning: if current cost exceeds K, stop (should be handled by push check, but safe to keep)
        if c > K:
            continue
            
        # Lower bound pruning:
        # The minimum operations needed to finish is at least max(n-i, m-j).
        # This is because we can at best match all remaining characters (cost 0 for matches),
        # but we still need to advance both pointers. The "distance" in the grid is max(n-i, m-j).
        # If current cost + this lower bound > K, we can't reach the target.
        if c + max(n - i, m - j) > K:
            continue
            
        # Transitions
        if i < n and j < m:
            if S[i] == T[j]:
                # Match: cost 0
                ni, nj = i + 1, j + 1
                if (ni, nj) not in visited:
                    visited.add((ni, nj))
                    # Push to front for 0-cost edge
                    queue.appendleft((ni, nj, c))
            else:
                # Mismatch: cost 1 for all options
                # 1. Replace
                if (i+1, j+1) not in visited:
                    visited.add((i+1, j+1))
                    queue.append((i+1, j+1, c+1))
                # 2. Delete S[i]
                if (i+1, j) not in visited:
                    visited.add((i+1, j))
                    queue.append((i+1, j, c+1))
                # 3. Insert T[j]
                if (i, j+1) not in visited:
                    visited.add((i, j+1))
                    queue.append((i, j+1, c+1))
        elif i < n:
            # Only S left, must delete the rest
            # Cost needed = n - i
            if c + (n - i) <= K:
                print("Yes")
                return
        elif j < m:
            # Only T left, must insert the rest
            # Cost needed = m - j
            if c + (m - j) <= K:
                print("Yes")
                return
        else:
            # Both exhausted but not at (n, m)? Impossible if loop condition is correct.
            pass

    print("No")

if __name__ == '__main__':
    solve()