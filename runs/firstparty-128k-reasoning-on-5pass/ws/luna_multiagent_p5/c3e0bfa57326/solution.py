import sys
from collections import defaultdict

MOD = 998244353


def solve() -> None:
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    # Each open parenthesis creates one node. A node stores its child node IDs.
    children = []
    stack = []
    roots = []

    # Canonical unordered-tree class IDs.
    intern = {}

    # Number of reachable ordered encodings for each canonical class.
    orbit_size = []

    # Factorials and inverse factorials are needed for multinomial factors.
    max_pairs = n // 2
    fact = [1] * (max_pairs + 1)
    for i in range(1, max_pairs + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (max_pairs + 1)
    inv_fact[max_pairs] = pow(fact[max_pairs], MOD - 2, MOD)
    for i in range(max_pairs, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def finish_node(node_children):
        ids = sorted(node_children)
        key = tuple(ids)

        class_id = intern.get(key)
        if class_id is not None:
            return class_id

        total = len(ids)
        ways = fact[total]

        i = 0
        while i < total:
            j = i + 1
            while j < total and ids[j] == ids[i]:
                j += 1

            multiplicity = j - i
            child_class = ids[i]
            ways = ways * inv_fact[multiplicity] % MOD
            ways = ways * pow(orbit_size[child_class], multiplicity, MOD) % MOD
            i = j

        class_id = len(orbit_size)
        intern[key] = class_id
        orbit_size.append(ways)
        return class_id

    for ch in s:
        if ch == '(':
            children.append([])
            stack.append(len(children) - 1)
        else:
            node = stack.pop()
            class_id = finish_node(children[node])
            if stack:
                children[stack[-1]].append(class_id)
            else:
                roots.append(class_id)

    # The complete sequence is an ordered forest, and the same formula applies
    # to its top-level component multiset.
    roots.sort()
    answer = fact[len(roots)] % MOD

    i = 0
    while i < len(roots):
        j = i + 1
        while j < len(roots) and roots[j] == roots[i]:
            j += 1

        multiplicity = j - i
        class_id = roots[i]
        answer = answer * inv_fact[multiplicity] % MOD
        answer = answer * pow(orbit_size[class_id], multiplicity, MOD) % MOD
        i = j

    print(answer)


if __name__ == "__main__":
    solve()