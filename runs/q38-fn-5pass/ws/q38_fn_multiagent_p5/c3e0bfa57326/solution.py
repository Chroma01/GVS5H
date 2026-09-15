import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = ''.join(data[1:])
    if len(s) > n:
        s = s[:n]

    # Build the ordered forest. Node 0 is a dummy root for top-level components.
    children = [[]]
    stack = [0]

    for ch in s:
        if ch == '(':
            children.append([])
            idx = len(children) - 1
            children[stack[-1]].append(idx)
            stack.append(idx)
        else:
            stack.pop()

    # Factorials up to the maximum possible degree.
    max_deg = len(children)
    fact = [1] * (max_deg + 1)
    for i in range(1, max_deg + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (max_deg + 1)
    invfact[max_deg] = pow(fact[max_deg], MOD - 2, MOD)
    for i in range(max_deg, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Canonical unordered tree types.
    # Type 0 is the leaf type, represented by an empty child tuple.
    type_map = {(): 0}
    type_count = [1]

    def get_type(t):
        tid = type_map.get(t)
        if tid is not None:
            return tid

        tid = len(type_count)
        type_map[t] = tid

        deg = len(t)
        val = fact[deg]

        i = 0
        while i < deg:
            c = t[i]
            j = i + 1
            while j < deg and t[j] == c:
                j += 1
            m = j - i

            val = val * invfact[m] % MOD
            val = val * pow(type_count[c], m, MOD) % MOD

            i = j

        type_count.append(val)
        return tid

    # Process nodes bottom-up. Descendants always have larger indices than ancestors.
    type_id = [0] * len(children)

    for u in range(len(children) - 1, 0, -1):
        if children[u]:
            t = tuple(sorted(type_id[v] for v in children[u]))
        else:
            t = ()
        type_id[u] = get_type(t)

    # The dummy root represents the whole top-level forest.
    if children[0]:
        root_t = tuple(sorted(type_id[v] for v in children[0]))
    else:
        root_t = ()

    root_type = get_type(root_t)
    print(type_count[root_type])

if __name__ == "__main__":
    main()