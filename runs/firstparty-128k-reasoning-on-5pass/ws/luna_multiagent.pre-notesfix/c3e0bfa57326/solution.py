import sys
from collections import Counter

MOD = 998244353


def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    children = []
    roots = []
    stack = []

    for ch in s:
        if ch == '(':
            v = len(children)
            children.append([])
            if stack:
                children[stack[-1]].append(v)
            else:
                roots.append(v)
            stack.append(v)
        else:
            stack.pop()

    m = len(children)
    factorial = [1] * (m + 1)
    for i in range(1, m + 1):
        factorial[i] = factorial[i - 1] * i % MOD

    type_id = [0] * m
    ways = [1] * m
    type_map = {}
    next_type = 0

    # Parents are created before descendants, so reverse order is bottom-up.
    for v in range(m - 1, -1, -1):
        child_types = tuple(sorted(type_id[c] for c in children[v]))

        if child_types not in type_map:
            type_map[child_types] = next_type
            next_type += 1
        type_id[v] = type_map[child_types]

        k = len(children[v])
        result = factorial[k]
        counts = Counter(child_types)

        for c in children[v]:
            result = result * ways[c] % MOD
        for cnt in counts.values():
            result = result * pow(factorial[cnt], MOD - 2, MOD) % MOD

        ways[v] = result

    root_types = tuple(sorted(type_id[r] for r in roots))
    answer = factorial[len(roots)]

    for r in roots:
        answer = answer * ways[r] % MOD

    for cnt in Counter(root_types).values():
        answer = answer * pow(factorial[cnt], MOD - 2, MOD) % MOD

    print(answer)


if __name__ == "__main__":
    solve()