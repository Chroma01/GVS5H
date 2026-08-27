import sys

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return

    N = int(data[0])
    S = data[1] if len(data) > 1 else ""

    maxf = max(N, len(S), 1)
    fact = [1] * (maxf + 1)
    for i in range(1, maxf + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact = [1] * (maxf + 1)
    invfact[maxf] = pow(fact[maxf], MOD - 2, MOD)
    for i in range(maxf, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    # Parse the parenthesis sequence into a rooted ordered forest.
    children = []
    stack = []
    top = []

    for ch in S:
        if ch == '(':
            idx = len(children)
            children.append([])
            stack.append(idx)
        else:
            node = stack.pop()
            if stack:
                children[stack[-1]].append(node)
            else:
                top.append(node)

    node_type = [0] * len(children)
    type_id = {}
    type_val = []

    def compute_value(tup):
        d = len(tup)
        val = fact[d]
        i = 0
        while i < d:
            j = i + 1
            while j < d and tup[j] == tup[i]:
                j += 1
            c = j - i
            val = val * invfact[c] % MOD
            val = val * pow(type_val[tup[i]], c, MOD) % MOD
            i = j
        return val

    def get_type(tup):
        tid = type_id.get(tup)
        if tid is not None:
            return tid
        tid = len(type_val)
        type_id[tup] = tid
        val = compute_value(tup)
        type_val.append(val)
        return tid

    # Children always have larger ids than their parent, so reverse order is bottom-up.
    for node in range(len(children) - 1, -1, -1):
        if children[node]:
            ct = [node_type[c] for c in children[node]]
            ct.sort()
            tup = tuple(ct)
        else:
            tup = ()
        node_type[node] = get_type(tup)

    # Virtual root: top-level components.
    top_t = [node_type[t] for t in top]
    top_t.sort()
    ans = compute_value(tuple(top_t))
    print(ans % MOD)

if __name__ == "__main__":
    main()