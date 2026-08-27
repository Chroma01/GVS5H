import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    to = [-1] * 26

    for a, b in zip(s, t):
        x = ord(a) - 97
        y = ord(b) - 97
        if to[x] != -1 and to[x] != y:
            print(-1)
            return
        to[x] = y

    edges = 0
    for x in range(26):
        if to[x] != -1 and to[x] != x:
            edges += 1

    # If all 26 letters occur in T, no temporary letter can be used.
    # Any non-identity transformation would reduce the number of distinct
    # currently present letters and can never restore it to 26.
    if edges > 0 and len(set(t)) == 26:
        print(-1)
        return

    state = [0] * 26  # 0: unvisited, 1: visiting, 2: finished
    cycles = 0

    def dfs(v):
        nonlocal cycles
        state[v] = 1

        nxt = to[v]
        if nxt != -1 and nxt != v:
            if state[nxt] == 0:
                dfs(nxt)
            elif state[nxt] == 1:
                cycles += 1

        state[v] = 2

    for v in range(26):
        if to[v] != -1 and to[v] != v and state[v] == 0:
            dfs(v)

    print(edges + cycles)

if __name__ == "__main__":
    main()