import sys
from collections import deque

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    adj = [[] for _ in range(n)]
    idx = 2

    for _ in range(m):
        x = data[idx] - 1
        y = data[idx + 1] - 1
        z = data[idx + 2]
        idx += 3
        adj[x].append((y, z))
        adj[y].append((x, z))

    potential = [-1] * n
    answer = [0] * n

    for start in range(n):
        if potential[start] != -1:
            continue

        potential[start] = 0
        queue = deque([start])
        component = []
        valid = True

        while queue:
            u = queue.popleft()
            component.append(u)

            for v, z in adj[u]:
                expected = potential[u] ^ z
                if potential[v] == -1:
                    potential[v] = expected
                    queue.append(v)
                elif potential[v] != expected:
                    valid = False
                    break

            if not valid:
                break

        if not valid:
            print(-1)
            return

        size = len(component)
        ones = [0] * 30

        for u in component:
            value = potential[u]
            for bit in range(30):
                ones[bit] += (value >> bit) & 1

        offset = 0
        for bit in range(30):
            if ones[bit] > size - ones[bit]:
                offset |= 1 << bit

        for u in component:
            answer[u] = potential[u] ^ offset

    print(*answer)

if __name__ == "__main__":
    solve()