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
        if mapping[x] != -1 and mapping[x] != y:
            print(-1)
            return
        mapping[x] = y

    edges = sum(
        1
        for x in range(26)
        if mapping[x] != -1 and mapping[x] != x
    )

    state = [0] * 26
    cycles = 0

    def dfs(v: int) -> None:
        nonlocal cycles
        state[v] = 1
        nxt = mapping[v]

        if nxt != -1 and nxt != v:
            if state[nxt] == 0:
                dfs(nxt)
            elif state[nxt] == 1:
                cycles += 1

        state[v] = 2

    for v in range(26):
        if mapping[v] != -1 and mapping[v] != v and state[v] == 0:
            dfs(v)

    all_letters_in_s = len(set(s)) == 26
    targets = {
        mapping[v]
        for v in range(26)
        if mapping[v] != -1
    }
    is_permutation = len(targets) == 26

    if cycles > 0 and all_letters_in_s and is_permutation:
        print(-1)
    else:
        print(edges + cycles)


if __name__ == "__main__":
    solve()