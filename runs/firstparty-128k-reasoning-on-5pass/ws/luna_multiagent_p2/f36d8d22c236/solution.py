import sys


def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    mapping = [-1] * 26

    for a, b in zip(s, t):
        x = ord(a) - ord('a')
        y = ord(b) - ord('a')
        if mapping[x] != -1 and mapping[x] != y:
            print(-1)
            return
        mapping[x] = y

    changed = sum(
        1 for x in range(26)
        if mapping[x] != -1 and mapping[x] != x
    )

    state = [0] * 26
    cycles = 0

    def dfs(v):
        nonlocal cycles
        state[v] = 1

        w = mapping[v]
        if w != -1 and w != v:
            if state[w] == 0:
                dfs(w)
            elif state[w] == 1:
                cycles += 1

        state[v] = 2

    for v in range(26):
        if state[v] == 0:
            dfs(v)

    if cycles > 0 and len(set(s)) == 26:
        print(-1)
    else:
        print(changed + cycles)


if __name__ == "__main__":
    solve()