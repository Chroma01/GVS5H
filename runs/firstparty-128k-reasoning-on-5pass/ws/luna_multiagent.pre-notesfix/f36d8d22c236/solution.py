import sys


def solve() -> None:
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    mapping = [-1] * 26

    for a, b in zip(s, t):
        x = ord(a) - ord('a')
        y = ord(b) - ord('a')
        if mapping[x] == -1:
            mapping[x] = y
        elif mapping[x] != y:
            print(-1)
            return

    non_identity = 0
    nxt = [-1] * 26

    for i in range(26):
        if mapping[i] != -1 and mapping[i] != i:
            non_identity += 1
            nxt[i] = mapping[i]

    state = [0] * 26
    cycles = 0

    for start in range(26):
        if state[start] != 0:
            continue

        path = []
        u = start

        while u != -1 and state[u] == 0:
            state[u] = 1
            path.append(u)
            u = nxt[u]

        if u != -1 and state[u] == 1:
            cycles += 1

        for v in path:
            state[v] = 2

    if cycles > 0:
        present_in_t = [False] * 26
        for ch in t:
            present_in_t[ord(ch) - ord('a')] = True

        if all(present_in_t):
            print(-1)
            return

    print(non_identity + cycles)


if __name__ == "__main__":
    solve()