import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    invfact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Node 0 is a virtual root representing the top-level forest.
    children = [[]]
    stack = [0]

    for c in s:
        if c == '(':
            v = len(children)
            children.append([])
            children[stack[-1]].append(v)
            stack.append(v)
        else:
            stack.pop()

    type_of_node = [0] * len(children)
    type_id = {}
    ways_for_type = []

    # Parents are created before descendants, so reverse index order is postorder.
    for v in range(len(children) - 1, -1, -1):
        child_types = sorted(type_of_node[u] for u in children[v])
        key = tuple(child_types)

        tid = type_id.get(key)
        if tid is None:
            value = fact[len(child_types)]

            i = 0
            while i < len(child_types):
                j = i + 1
                t = child_types[i]
                while j < len(child_types) and child_types[j] == t:
                    j += 1

                value = value * pow(ways_for_type[t], j - i, MOD) % MOD
                value = value * invfact[j - i] % MOD
                i = j

            tid = len(ways_for_type)
            type_id[key] = tid
            ways_for_type.append(value)

        type_of_node[v] = tid

    print(ways_for_type[type_of_node[0]])

if __name__ == "__main__":
    solve()