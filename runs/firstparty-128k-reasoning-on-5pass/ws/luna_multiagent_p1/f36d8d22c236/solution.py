import sys


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()
    t = input().strip()

    mapping = [-1] * 26
    present = [False] * 26

    for a, b in zip(s, t):
        x = ord(a) - ord('a')
        y = ord(b) - ord('a')
        present[x] = True
        if mapping[x] == -1:
            mapping[x] = y
        elif mapping[x] != y:
            print(-1)
            return

    changed = []
    for x in range(26):
        if mapping[x] != -1 and mapping[x] != x:
            changed.append(x)

    changed_count = len(changed)

    color = [0] * 26
    cycle_node = [False] * 26
    cycle_count = 0

    for start in changed:
        if color[start] != 0:
            continue

        path = []
        index = {}
        v = start

        while v in changed and color[v] == 0:
            color[v] = 1
            index[v] = len(path)
            path.append(v)
            v = mapping[v]

        if v in index:
            cycle_count += 1
            for u in path[index[v]:]:
                cycle_node[u] = True

        for u in path:
            color[u] = 2

    cycle_nodes = sum(cycle_node)

    # A cycle needs a temporary letter. If every letter is present initially,
    # a temporary letter can still be created when there is a changed edge
    # outside all cycles. Only a permutation consisting of cycles and fixed
    # points has no way to create such a temporary letter.
    if all(present) and cycle_count > 0 and changed_count == cycle_nodes:
        print(-1)
        return

    print(changed_count + cycle_count)


if __name__ == "__main__":
    solve()