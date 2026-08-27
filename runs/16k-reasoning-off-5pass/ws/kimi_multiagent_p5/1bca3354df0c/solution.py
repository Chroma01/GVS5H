import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)

    # 2-color each connected component (graph is guaranteed bipartite).
    # Rule (verified by exhaustive brute force for N <= 5, random N = 6):
    #   Let x = sum over components of the color-0 side size (any fixed
    #   reference coloring). The game always ends at a complete bipartite
    #   graph K_{x', N-x'} with total moves x'*(N-x') - M, and the outcome
    #   under optimal play equals the parity of x*(N-x) - M.
    color = [-1] * (N + 1)
    x = 0
    for s in range(1, N + 1):
        if color[s] != -1:
            continue
        color[s] = 0
        cnt0 = 1
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if color[w] == -1:
                    color[w] = color[u] ^ 1
                    if color[w] == 0:
                        cnt0 += 1
                    dq.append(w)
        x += cnt0

    T = x * (N - x) - M
    sys.stdout.write("Aoki\n" if (T & 1) else "Takahashi\n")

main()