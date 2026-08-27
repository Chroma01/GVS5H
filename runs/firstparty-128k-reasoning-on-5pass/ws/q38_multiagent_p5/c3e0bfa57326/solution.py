import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    s = data[1] if len(data) > 1 else b""

    children = []
    roots = []
    stack = []

    for ch in s:
        if ch == 40:  # '('
            idx = len(children)
            children.append([])
            if stack:
                children[stack[-1]].append(idx)
            else:
                roots.append(idx)
            stack.append(idx)
        else:         # ')'
            stack.pop()

    m = len(children)

    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (m + 1)
    invfact[m] = pow(fact[m], MOD - 2, MOD)
    for i in range(m, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    type_of = [0] * m
    type_id = {}
    ways = []

    def forest_ways(types):
        total = len(types)
        val = fact[total]
        i = 0
        while i < total:
            j = i + 1
            while j < total and types[j] == types[i]:
                j += 1
            k = j - i
            val = val * invfact[k] % MOD
            val = val * pow(ways[types[i]], k, MOD) % MOD
            i = j
        return val

    for idx in range(m - 1, -1, -1):
        cts = [type_of[c] for c in children[idx]]
        cts.sort()
        key = tuple(cts)

        t = type_id.get(key)
        if t is None:
            t = len(ways)
            type_id[key] = t
            ways.append(forest_ways(cts))

        type_of[idx] = t

    root_types = [type_of[r] for r in roots]
    root_types.sort()

    print(forest_ways(root_types) % MOD)

if __name__ == "__main__":
    main()