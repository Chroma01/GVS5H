import sys
from collections import deque

def solve() -> None:
    input = sys.stdin.buffer.readline
    N, M = map(int, input().split())

    adj = [[] for _ in range(N)]
    for _ in range(M):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * N

    active_odd = 0      # odd-sized connected components with at least one edge
    isolated = 0        # components of size 1
    both_odd_even = 0   # even-sized components whose two color classes are both odd

    for s in range(N):
        if color[s] != -1:
            continue

        color[s] = 0
        q = deque([s])
        cnt = [1, 0]
        deg_sum = 0

        while q:
            u = q.popleft()
            deg_sum += len(adj[u])
            cu = color[u]
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = cu ^ 1
                    cnt[color[v]] += 1
                    q.append(v)

        size = cnt[0] + cnt[1]

        if size == 1:
            isolated += 1
        elif size % 2 == 1:
            active_odd += 1
        else:
            if (cnt[0] & 1) and (cnt[1] & 1):
                both_odd_even += 1

    if N % 2 == 1:
        first_wins = (M % 2 == 1)
    else:
        if active_odd >= 3:
            first_wins = (M % 2 == 1)
        elif active_odd >= 1:
            first_wins = True
        else:
            first_wins = ((M + both_odd_even + isolated // 2) % 2 == 1)

    print("Aoki" if first_wins else "Takahashi")

if __name__ == "__main__":
    solve()