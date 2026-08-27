import sys

MOD = 998244353

def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

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

    m = len(children) - 1

    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (m + 1)
    invfact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    type_id = {}
    ways = []

    def get_type(child_types):
        key = tuple(sorted(child_types))
        tid = type_id.get(key)
        if tid is not None:
            return tid

        cnt = {}
        for x in key:
            cnt[x] = cnt.get(x, 0) + 1

        value = fact[len(key)]
        for c in cnt.values():
            value = value * invfact[c] % MOD

        for x, c in cnt.items():
            value = value * pow(ways[x], c, MOD) % MOD

        tid = len(ways)
        type_id[key] = tid
        ways.append(value)
        return tid

    node_type = [0] * (m + 1)

    for v in range(m, 0, -1):
        child_types = [node_type[u] for u in children[v]]
        node_type[v] = get_type(child_types)

    root_types = [node_type[v] for v in children[0]]
    answer = get_type(root_types)
    print(ways[answer] % MOD)

if __name__ == "__main__":
    main()