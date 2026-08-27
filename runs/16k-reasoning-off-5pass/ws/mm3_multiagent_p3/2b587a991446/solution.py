import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N, M, S, T = map(int, input().split())
    adj = [[] for _ in range(N+1)]
    for _ in range(M):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    if M == N - 1:
        # Tree: impossible
        print(-1)
        return
    
    # Check for cycle: M == N and all degrees 2
    if M == N:
        is_cycle = True
        for i in range(1, N+1):
            if len(adj[i]) != 2:
                is_cycle = False
                break
        if is_cycle:
            # Compute answer for a cycle
            # Find the cyclic order starting from S
            order = []
            visited_cycle = [False]*(N+1)
            cur = S
            prev = -1
            while True:
                visited_cycle[cur] = True
                order.append(cur)
                nxt = -1
                for nb in adj[cur]:
                    if nb != prev:
                        nxt = nb
                        break
                if nxt == S or nxt == -1:
                    break
                prev = cur
                cur = nxt
            pos = {v: i for i, v in enumerate(order)}
            d = (pos[T] - pos[S]) % N
            if N % 2 == 1:
                ans = N
            else:
                ans = N-1 if d % 2 == 1 else N
            print(ans)
            return
    
    # General case: bidirectional BFS on product graph
    # We use a hard limit on visited states to avoid memory/time explosion.
    MAX_STATES = 2000000
    
    # Forward search from (S, T)
    f_visited = {}
    f_visited[S * N + T] = 0
    f_queue = deque()
    f_queue.append((S, T))
    
    # Backward search from (T, S)
    b_visited = {}
    b_visited[T * N + S] = 0
    b_queue = deque()
    b_queue.append((T, S))
    
    # Expand level by level alternating between forward and backward
    while f_queue and b_queue:
        # Expand forward by one level
        for _ in range(len(f_queue)):
            a, b = f_queue.popleft()
            d = f_visited[a * N + b]
            # Move A to a neighbor
            for na in adj[a]:
                if na != b:
                    state = na * N + b
                    if state not in f_visited:
                        if len(f_visited) + len(b_visited) >= MAX_STATES:
                            print(-1)
                            return
                        f_visited[state] = d + 1
                        f_queue.append((na, b))
                        if state in b_visited:
                            print(d + 1 + b_visited[state])
                            return
            # Move B to a neighbor
            for nb in adj[b]:
                if nb != a:
                    state = a * N + nb
                    if state not in f_visited:
                        if len(f_visited) + len(b_visited) >= MAX_STATES:
                            print(-1)
                            return
                        f_visited[state] = d + 1
                        f_queue.append((a, nb))
                        if state in b_visited:
                            print(d + 1 + b_visited[state])
                            return
        
        # Expand backward by one level
        for _ in range(len(b_queue)):
            a, b = b_queue.popleft()
            d = b_visited[a * N + b]
            # Move A (predecessors: any neighbor a' of a with a' != b)
            for na in adj[a]:
                if na != b:
                    state = na * N + b
                    if state not in b_visited:
                        if len(f_visited) + len(b_visited) >= MAX_STATES:
                            print(-1)
                            return
                        b_visited[state] = d + 1
                        b_queue.append((na, b))
                        if state in f_visited:
                            print(f_visited[state] + d + 1)
                            return
            # Move B
            for nb in adj[b]:
                if nb != a:
                    state = a * N + nb
                    if state not in b_visited:
                        if len(f_visited) + len(b_visited) >= MAX_STATES:
                            print(-1)
                            return
                        b_visited[state] = d + 1
                        b_queue.append((a, nb))
                        if state in f_visited:
                            print(f_visited[state] + d + 1)
                            return
    print(-1)

if __name__ == "__main__":
    solve()