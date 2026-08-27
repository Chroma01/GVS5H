import sys

# Increase recursion depth just in case, though iterative BFS/DFS is preferred for large N
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    # If M is 0, we still need to read the rest of the input if any (though constraints say M lines follow)
    # But usually we just process edges.
    
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Find connected components and check their sizes
    visited = [False] * (N + 1)
    has_odd_component = False
    
    # We can use BFS or DFS. BFS is safer against recursion limits.
    from collections import deque
    
    for i in range(1, N + 1):
        if not visited[i]:
            # Start BFS
            q = deque([i])
            visited[i] = True
            size = 0
            while q:
                u = q.popleft()
                size += 1
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        q.append(v)
            
            if size % 2 != 0:
                has_odd_component = True

    # Logic derived:
    # If N is odd:
    #   Final edges V_final is always even (product of two numbers summing to odd).
    #   Moves = V_final - M = Even - M.
    #   Parity(Moves) = Parity(M).
    #   Aoki wins if Moves is odd => M is odd.
    #
    # If N is even:
    #   V_final = N_A * N_B. Since N_A + N_B = N (even), N_A and N_B have same parity.
    #   If both are even, V_final is even.
    #   If both are odd, V_final is odd.
    #   It turns out V_final is odd if and only if there exists at least one connected component with an odd number of vertices.
    #   (This is because the bipartition sizes of the final graph are determined by merging components. 
    #    If we have an odd component, we can't pair up all vertices to make even partitions in the final graph? 
    #    Actually, the invariant is that the parity of the product of partition sizes is determined by the existence of odd-sized components).
    #
    #   Case 1: All components have even size.
    #     Then V_final is even.
    #     Moves = Even - M. Parity = Parity(M).
    #     Aoki wins if M is odd.
    #
    #   Case 2: At least one component has odd size.
    #     Then V_final is odd.
    #     Moves = Odd - M. Parity = 1 - Parity(M).
    #     Aoki wins if Moves is odd => M is even.

    if N % 2 != 0:
        # N is odd
        if M % 2 != 0:
            print("Aoki")
        else:
            print("Takahashi")
    else:
        # N is even
        if has_odd_component:
            # V_final is odd
            if M % 2 == 0:
                print("Aoki")
            else:
                print("Takahashi")
        else:
            # All components even size => V_final is even
            if M % 2 != 0:
                print("Aoki")
            else:
                print("Takahashi")

if __name__ == '__main__':
    solve()