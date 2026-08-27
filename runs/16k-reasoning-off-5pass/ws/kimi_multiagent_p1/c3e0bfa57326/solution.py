import sys
sys.setrecursionlimit(100000)

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()

    # Parse into ordered rooted forest.
    children = []   # children[i] = list of node ids
    def new_node():
        children.append([])
        return len(children) - 1

    roots = []
    stack = []
    for ch in S:
        if ch == '(':
            u = new_node()
            if stack:
                children[stack[-1]].append(u)
            else:
                roots.append(u)
            stack.append(u)
        else:
            stack.pop()

    # Canonical ids for shape and mirror-shape.
    # shape(node) = tuple of child shapes in order.
    # mirror(node) = tuple of child mirror-shapes in reverse order.
    shape_id = {}
    mirror_id = {}
    def get_shape(key):
        if key in shape_id:
            return shape_id[key]
        i = len(shape_id)
        shape_id[key] = i
        return i
    def get_mirror(key):
        if key in mirror_id:
            return mirror_id[key]
        i = len(mirror_id)
        mirror_id[key] = i
        return i

    n = len(children)
    shp = [0]*n
    mir = [0]*n
    # parent id < child id (ids assigned on '('), so decreasing id order works.
    for u in range(n-1, -1, -1):
        cs = children[u]
        skey = tuple(shp[v] for v in cs)
        mkey = tuple(mir[v] for v in reversed(cs))
        shp[u] = get_shape(skey)
        mir[u] = get_mirror(mkey)

    # Mirror-class: unordered pair {shp, mir}; symmetric iff shp == mir.
    class_id = {}
    def get_class(key):
        if key in class_id:
            return class_id[key]
        i = len(class_id)
        class_id[key] = i
        return i

    cls = [0]*n
    sym = [False]*n
    for u in range(n):
        a, b = shp[u], mir[u]
        sym[u] = (a == b)
        if a > b:
            a, b = b, a
        cls[u] = get_class((a, b))

    # factorials / inverse factorials
    fact = [1]*(N+2)
    for i in range(1, N+2):
        fact[i] = fact[i-1]*i % MOD
    invfact = [1]*(N+2)
    invfact[N+1] = pow(fact[N+1], MOD-2, MOD)
    for i in range(N+1, 0, -1):
        invfact[i-1] = invfact[i]*i % MOD

    def multinomial(total, counts):
        res = fact[total]
        for c in counts:
            res = res * invfact[c] % MOD
        return res

    def factor_for(kids):
        groups = {}
        for v in kids:
            groups.setdefault(cls[v], []).append(v)
        m = len(kids)
        res = multinomial(m, [len(g) for g in groups.values()])
        for g in groups.values():
            if not sym[g[0]]:
                res = res * pow(2, len(g), MOD) % MOD
        return res

    ans = 1
    ans = ans * factor_for(roots) % MOD
    for u in range(n):
        if children[u]:
            ans = ans * factor_for(children[u]) % MOD

    print(ans % MOD)

main()