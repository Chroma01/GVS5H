import sys

MOD = 998244353


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    if len(data) == 2:
        s = data[1][:N]
    else:
        s = b"".join(data[1:])[:N]

    # Bit for pair (x, y), x,y in {0,1}.
    def bit(x, y):
        return 1 << ((x << 1) | y)

    def mask(pairs):
        m = 0
        for x, y in pairs:
            m |= bit(x, y)
        return m

    # Allowed (a_{i-1}, a_i) pairs for each possible d_i.
    # a_i = 1 means cycle edge i -> i+1.
    rel0 = [
        mask([(0, 1)]),                       # d = 0
        mask([(0, 0), (1, 1)]),               # d = 1
        mask([(1, 0)]),                       # d = 2
    ]
    rel1 = [
        mask([(0, 1)]),                       # d = 0
        mask([(0, 1), (0, 0), (1, 1)]),       # d = 1
        mask([(0, 0), (1, 1), (1, 0)]),       # d = 2
        mask([(1, 0)]),                       # d = 3
    ]

    # A relation is stored as a 4-bit mask.
    # Split it into two row subsets:
    #   u = possible current values starting from 0
    #   v = possible current values starting from 1
    # For a local relation, row_table[S] is the set of next values reachable
    # from any current value in subset S.
    def row_table(rel):
        tab = []
        for S in range(4):
            T = 0
            for y in range(2):
                if S & (1 << y):
                    for z in range(2):
                        if rel & bit(y, z):
                            T |= 1 << z
            tab.append(T)
        return tuple(tab)

    tabs0 = [row_table(r) for r in rel0]
    tabs1 = [row_table(r) for r in rel1]

    # Transition matrices on all 16 relation masks.
    # Transitions to the empty relation are omitted because it is dead.
    mat0 = [[0] * 16 for _ in range(16)]
    mat1 = [[0] * 16 for _ in range(16)]

    for cur in range(16):
        u = cur & 3
        v = (cur >> 2) & 3

        for tab in tabs0:
            nxt = tab[u] | (tab[v] << 2)
            if nxt:
                mat0[cur][nxt] += 1

        for tab in tabs1:
            nxt = tab[u] | (tab[v] << 2)
            if nxt:
                mat1[cur][nxt] += 1

    # Keep only states reachable from the identity relation.
    start = 9  # identity: (0,0) and (1,1)
    reachable = [False] * 16
    reachable[start] = True
    stack = [start]

    while stack:
        st = stack.pop()
        for mat in (mat0, mat1):
            row = mat[st]
            for nxt, w in enumerate(row):
                if w and not reachable[nxt]:
                    reachable[nxt] = True
                    stack.append(nxt)

    old_to_new = [-1] * 16
    states = []
    for i in range(16):
        if reachable[i]:
            old_to_new[i] = len(states)
            states.append(i)

    B = len(states)

    rmat0 = [[0] * B for _ in range(B)]
    rmat1 = [[0] * B for _ in range(B)]

    for old in states:
        i = old_to_new[old]

        for nxt, w in enumerate(mat0[old]):
            if w:
                j = old_to_new[nxt]
                if j != -1:
                    rmat0[i][j] += w

        for nxt, w in enumerate(mat1[old]):
            if w:
                j = old_to_new[nxt]
                if j != -1:
                    rmat1[i][j] += w

    start_idx = old_to_new[start]
    accept_idx = [
        old_to_new[st]
        for st in states
        if (st & 1) or (st & 8)  # contains (0,0) or (1,1)
    ]

    # Generate an unrolled transition function for speed.
    def make_expr(mat):
        exprs = []
        for j in range(B):
            terms = []
            for i in range(B):
                w = mat[i][j]
                if w:
                    if w == 1:
                        terms.append(f"v{i}")
                    else:
                        terms.append(f"v{i}*{w}")

            if not terms:
                exprs.append("0")
            elif len(terms) == 1 and "*" not in terms[0]:
                exprs.append(terms[0])
            else:
                exprs.append("(" + " + ".join(terms) + ") % mod")
        return exprs

    expr0 = make_expr(rmat0)
    expr1 = make_expr(rmat1)

    if B == 1:
        unpack = "v0, = dp"
    else:
        unpack = ", ".join(f"v{i}" for i in range(B)) + " = dp"

    lines = [
        "def run(s, dp):",
        f"    mod = {MOD}",
        "    for ch in s:",
        "        " + unpack,
        "        if ch == 49:",
    ]
    for j, e in enumerate(expr1):
        lines.append(f"            dp[{j}] = {e}")
    lines.append("        else:")
    for j, e in enumerate(expr0):
        lines.append(f"            dp[{j}] = {e}")
    lines.append("    return dp")

    code = "\n".join(lines)

    # Generic fallback, normally not used.
    edges0 = []
    edges1 = []
    for i in range(B):
        for j in range(B):
            if rmat0[i][j]:
                edges0.append((i, j, rmat0[i][j]))
            if rmat1[i][j]:
                edges1.append((i, j, rmat1[i][j]))

    try:
        ns = {}
        exec(code, ns)
        run = ns["run"]
    except Exception:
        def run(s, dp, edges0=edges0, edges1=edges1, B=B, mod=MOD):
            for ch in s:
                ndp = [0] * B
                if ch == 49:
                    for f, t, m in edges1:
                        ndp[t] += dp[f] * m
                else:
                    for f, t, m in edges0:
                        ndp[t] += dp[f] * m
                dp = [x % mod for x in ndp]
            return dp

    dp = [0] * B
    dp[start_idx] = 1
    dp = run(s, dp)

    ans = sum(dp[i] for i in accept_idx) % MOD
    print(ans)


if __name__ == "__main__":
    solve()