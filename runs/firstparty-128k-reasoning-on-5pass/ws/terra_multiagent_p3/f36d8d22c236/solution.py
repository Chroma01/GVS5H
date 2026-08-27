import sys

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    nxt = [-1] * 26

    for a, b in zip(s, t):
        x = ord(a) - 97
        y = ord(b) - 97
        if nxt[x] != -1 and nxt[x] != y:
            print(-1)
            return
        nxt[x] = y

    operations = 0
    for x in range(26):
        if nxt[x] != -1 and nxt[x] != x:
            operations += 1
        else:
            # Identity mappings do not need an operation and must not
            # participate in cycle detection.
            nxt[x] = -1

    state = [0] * 26  # 0: unvisited, 1: visiting, 2: finished
    cycles = 0

    def dfs(v):
        nonlocal cycles
        state[v] = 1
        to = nxt[v]
        if to != -1:
            if state[to] == 0:
                dfs(to)
            elif state[to] == 1:
                cycles += 1
        state[v] = 2

    for v in range(26):
        if state[v] == 0:
            dfs(v)

    if cycles > 0 and len(set(t)) == 26:
        print(-1)
    else:
        print(operations + cycles)

if __name__ == "__main__":
    solve()