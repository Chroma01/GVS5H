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
        if mapping[x] == -1:
            mapping[x] = y
        elif mapping[x] != y:
            print(-1)
            return

    edges = sum(1 for x in range(26) if mapping[x] != -1 and mapping[x] != x)

    # Ignore identity mappings when constructing the dependency graph.
    nxt = [-1] * 26
    for x in range(26):
        if mapping[x] != -1 and mapping[x] != x:
            nxt[x] = mapping[x]

    state = [0] * 26
    in_cycle = [False] * 26
    cycles = 0

    for start in range(26):
        if state[start] != 0:
            continue

        path = []
        position = {}
        v = start

        while v != -1 and state[v] == 0 and v not in position:
            position[v] = len(path)
            path.append(v)
            v = nxt[v]

        if v != -1 and v in position:
            cycles += 1
            for u in path[position[v]:]:
                in_cycle[u] = True

        for u in path:
            state[u] = 2

    if cycles:
        present = [False] * 26
        for ch in s:
            present[ord(ch) - ord('a')] = True

        # A temporary character is available if it is initially absent,
        # or if a non-cyclic mapped character can be moved away first.
        temporary_available = (
            any(not present[x] for x in range(26))
            or any(
                nxt[x] != -1 and not in_cycle[x]
                for x in range(26)
            )
        )

        if not temporary_available:
            print(-1)
            return

    print(edges + cycles)


if __name__ == "__main__":
    solve()