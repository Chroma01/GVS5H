import sys
from collections import Counter

MOD = 998244353

def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    type_id = {}
    type_children = []

    def get_type(children):
        key = tuple(sorted(children))
        if key not in type_id:
            type_id[key] = len(type_children)
            type_children.append(key)
        return type_id[key]

    stack = [[]]

    for ch in s:
        if ch == '(':
            stack.append([])
        else:
            children = stack.pop()
            t = get_type(children)
            stack[-1].append(t)

    root_children = stack[0]
    m = n // 2

    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (m + 1)
    inv_fact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    ways = [0] * len(type_children)

    for tid, children in enumerate(type_children):
        cnt = Counter(children)
        k = len(children)
        value = fact[k]

        for child_type, multiplicity in cnt.items():
            value = value * pow(ways[child_type], multiplicity, MOD) % MOD
            value = value * inv_fact[multiplicity] % MOD

        ways[tid] = value

    cnt_root = Counter(root_children)
    k = len(root_children)
    answer = fact[k]

    for child_type, multiplicity in cnt_root.items():
        answer = answer * pow(ways[child_type], multiplicity, MOD) % MOD
        answer = answer * inv_fact[multiplicity] % MOD

    print(answer)

if __name__ == "__main__":
    solve()