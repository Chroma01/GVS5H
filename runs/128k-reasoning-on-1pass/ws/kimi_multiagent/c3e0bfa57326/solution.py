import sys
from collections import Counter

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1]

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Map the sorted tuple of child class IDs to this tree's unordered class ID.
    class_id = {}
    # ways[c] = number of ordered Dyck words realizing unordered tree class c.
    ways = []

    def count_from_children(children):
        k = len(children)
        result = fact[k]
        for cid, multiplicity in Counter(children).items():
            result = result * invfact[multiplicity] % MOD
            result = result * pow(ways[cid], multiplicity, MOD) % MOD
        return result

    sys.setrecursionlimit(1000000)
    pos = 0

    def parse_forest():
        nonlocal pos
        ids = []

        while pos < n and s[pos] != ')':
            # Parse one tree: '(' forest ')'.
            pos += 1
            children = parse_forest()
            pos += 1

            key = tuple(sorted(children))
            cid = class_id.get(key)
            if cid is None:
                cid = len(ways)
                class_id[key] = cid
                ways.append(count_from_children(children))

            ids.append(cid)

        return ids

    top_level = parse_forest()
    print(count_from_children(top_level))


if __name__ == "__main__":
    main()