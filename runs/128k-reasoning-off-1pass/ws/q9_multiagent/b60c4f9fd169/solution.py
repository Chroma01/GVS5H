import sys
from collections import deque

def solve():
    # Read all input from stdin efficiently
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

    # Pruning: If the length difference is greater than K, 
    # it's impossible to transform S to T with <= K operations
    if abs(n - m) > K:
        print("No")
        return

    # We use a BFS (specifically 0-1 BFS) to find the minimum edit distance.
    # State: (i, j) representing we have processed S[:i] and T[:j].
    # We want to reach (n, m) with cost <= K.
    # Optimization: We only visit states where |i - j| <= K.
    
    # To save memory, we use a 1D array for the visited status of the "band".
    # visited[i][d] where d = j - i + K.
    # i ranges from 0 to n.
    # d ranges from 0 to 2*K (since -K <= j-i <= K).
    
    width = 2 * K + 1
    visited = [bytearray(width) for _ in range(n + 1)]
    
    dq = deque()
    
    # Initial state
    dq.append((0, 0, 0))
    visited[0][0 + K] = 1
    
    while dq:
        i, j, cost = dq.popleft()
        
        # Check if we reached the target
        if i == n and j == m:
            print("Yes")
            return
        
        # If current cost already exceeds K, skip
        if cost > K:
            continue
            
        # Transition 1: Advance both pointers (Match or Replace)
        if i < n and j < m:
            if S[i] == T[j]:
                # Match: Cost 0
                new_cost = cost
                ni, nj = i + 1, j + 1
                if abs(ni - nj) <= K:
                    d = nj - ni + K
                    if not visited[ni][d]:
                        visited[ni][d] = 1
                        dq.appendleft((ni, nj, new_cost))
            else:
                # Replace: Cost 1
                new_cost = cost + 1
                ni, nj = i + 1, j + 1
                if abs(ni - nj) <= K:
                    d = nj - ni + K
                    if not visited[ni][d]:
                        visited[ni][d] = 1
                        if new_cost <= K:
                            dq.append((ni, nj, new_cost))
        
        # Transition 2: Delete from S (advance i)
        if i < n:
            ni, nj = i + 1, j
            if abs(ni - nj) <= K:
                d = nj - ni + K
                if not visited[ni][d]:
                    visited[ni][d] = 1
                    if cost + 1 <= K:
                        dq.append((ni, nj, cost + 1))
                        
        # Transition 3: Insert into S (advance j)
        if j < m:
            ni, nj = i, j + 1
            if abs(ni - nj) <= K:
                d = nj - ni + K
                if not visited[ni][d]:
                    visited[ni][d] = 1
                    if cost + 1 <= K:
                        dq.append((ni, nj, cost + 1))
                        
    print("No")

if __name__ == '__main__':
    solve()