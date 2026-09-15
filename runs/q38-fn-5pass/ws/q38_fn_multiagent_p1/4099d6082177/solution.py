import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    M = N * K

    if K == 1:
        print("Yes")
        return

    adj = [[] for _ in range(M + 1)]
    idx = 2
    for _ in range(M - 1):
        u = data[idx]
        v = data[idx + 1]
        idx += 2
        adj[u].append(v)
        adj[v].append(u)

    del data

    parent = [0] * (M + 1)
    parent[1] = -1
    order = []
    stack = [1]

    while stack:
        v = stack.pop()
        order.append(v)
        for to in adj[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    state = [0] * (M + 1)

    for v in reversed(order):
        cnt = 0
        a = 0
        b = 0
        bad = False

        for to in adj[v]:
            if parent[to] == v:
                s = state[to]
                if s < 0:
                    bad = True
                    break
                if s > 0:
                    cnt += 1
                    if cnt == 1:
                        a = s
                    elif cnt == 2:
                        b = s
                    else:
                        bad = True
                        break

        if bad:
            state[v] = -1
        elif cnt == 0:
            state[v] = 1
        elif cnt == 1:
            if a + 1 == K:
                state[v] = 0
            elif a + 1 < K:
                state[v] = a + 1
            else:
                state[v] = -1
        elif cnt == 2:
            if a + b + 1 == K:
                state[v] = 0
            else:
                state[v] = -1
        else:
            state[v] = -1

    print("Yes" if state[1] == 0 else "No")

if __name__ == "__main__":
    solve()