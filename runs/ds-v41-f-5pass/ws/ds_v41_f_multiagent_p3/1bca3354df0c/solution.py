import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it)); M = int(next(it))
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (N + 1)
    K = 0          # number of odd-sized connected components
    P = 0          # parity of total size of color-0 side

    for s in range(1, N + 1):
        if color[s] != -1:
            continue
        color[s] = 0
        dq = deque([s])
        c0 = 0
        size = 0
        while dq:
            u = dq.popleft()
            size += 1
            if color[u] == 0:
                c0 += 1
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    dq.append(v)
        if size & 1:
            K += 1
        P += c0
    P &= 1

    if N & 1:
        ans = "Aoki" if (M & 1) else "Takahashi"
    else:
        if K == 0:
            ans = "Aoki" if ((P + M) & 1) else "Takahashi"
        elif K == 2:
            ans = "Aoki"
        else:  # K >= 4 (K is always even when N is even)
            ans = "Aoki" if (M & 1) else "Takahashi"

    sys.stdout.write(ans + "\n")

main()