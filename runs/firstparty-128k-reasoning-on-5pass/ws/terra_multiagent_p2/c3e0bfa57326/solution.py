import sys
from collections import Counter

MOD = 998244353


def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    # Node 0 is a virtual root for the whole forest.
    children = [[]]
    stack = [0]

    for ch in s:
        if ch == '(':
            v = len(children)
            children.append([])
            children[stack[-1]].append(v)
            stack.append(v)
        else:
            stack.pop()

    m = len(children)

    fact = [1] * (m + 1)
    invfact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Canonical IDs of unordered rooted subtree types.
    type_id = [0] * m
    intern = {}
    next_id = 0

    ans = 1

    # Parents are created before children, so reverse order is postorder.
    for v in range(m - 1, -1, -1):
        ids = [type_id[u] for u in children[v]]
        ids.sort()

        key = tuple(ids)
        if key not in intern:
            intern[key] = next_id
            next_id += 1
        type_id[v] = intern[key]

        d = len(ids)
        ans = ans * fact[d] % MOD

        cnt = Counter(ids)
        for c in cnt.values():
            ans = ans * invfact[c] % MOD

    print(ans)


if __name__ == "__main__":
    main()