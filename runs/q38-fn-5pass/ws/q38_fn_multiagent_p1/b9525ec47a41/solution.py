import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    s = data[1][:N]

    # Row subset types:
    # 0 = empty, 1 = {0}, 2 = {1}, 3 = {0,1}
    #
    # Functions induced by the five possible digit constraints:
    # force 0->1, equality, force 1->0, forbid 1->0, forbid 0->1
    f01 = (0, 2, 0, 2)
    fid = (0, 1, 2, 3)
    f10 = (0, 0, 1, 1)
    g = (0, 3, 2, 3)
    h = (0, 1, 3, 3)

    funcs_all = (f01, fid, f10, g, h)
    funcs0 = (f01, fid, f10)
    funcs1 = (f01, g, h, f10)

    # DFA state is a pair of row-subsets (for start 0 and start 1),
    # encoded as x * 4 + y.
    # Initial state: start 0 can be 0, start 1 can be 1 => (1, 2) => 6.
    seen = [False] * 16
    stack = [6]
    seen[6] = True
    reachable = []

    while stack:
        code = stack.pop()
        reachable.append(code)
        x = code >> 2
        y = code & 3
        for f in funcs_all:
            nc = f[x] * 4 + f[y]
            if not seen[nc]:
                seen[nc] = True
                stack.append(nc)

    reachable.sort()
    M = len(reachable)
    idx = {code: i for i, code in enumerate(reachable)}
    init_idx = idx[6]

    trans0 = [[] for _ in range(M)]
    trans1 = [[] for _ in range(M)]

    for i, code in enumerate(reachable):
        x = code >> 2
        y = code & 3
        for f in funcs0:
            trans0[i].append(idx[f[x] * 4 + f[y]])
        for f in funcs1:
            trans1[i].append(idx[f[x] * 4 + f[y]])

    # Cyclic feasibility: start 0 ends at 0, or start 1 ends at 1.
    accept_idx = [
        i for i, code in enumerate(reachable)
        if ((code >> 2) & 1) or (code & 2)
    ]

    def make_exprs(trans):
        incoming = [[] for _ in range(M)]
        for src, dsts in enumerate(trans):
            for dst in dsts:
                incoming[dst].append(src)

        exprs = []
        for dst in range(M):
            if not incoming[dst]:
                exprs.append("0")
                continue

            cnt = [0] * M
            for src in incoming[dst]:
                cnt[src] += 1

            terms = []
            for src, c in enumerate(cnt):
                if c:
                    if c == 1:
                        terms.append(f"a{src}")
                    else:
                        terms.append(f"{c}*a{src}")
            exprs.append(" + ".join(terms))

        return exprs

    e0 = make_exprs(trans0)
    e1 = make_exprs(trans1)

    var_names = ", ".join(f"a{i}" for i in range(M))
    init_vals = ["0"] * M
    init_vals[init_idx] = "1"

    ans_expr = " + ".join(f"dp[{i}]" for i in accept_idx) if accept_idx else "0"
    mod_exprs = ", ".join(f"dp[{i}] % MOD" for i in range(M))

    # Generate an unrolled transition function for speed.
    lines = [
        "def process(data):",
        "    MOD = 998244353",
        "    dp = [" + ", ".join(init_vals) + "]",
        "    cnt = 0",
        "    for ch in data:",
        "        " + var_names + " = dp",
        "        if ch == 48:",  # ord('0')
        "            dp = [" + ", ".join(e0) + "]",
        "        else:",
        "            dp = [" + ", ".join(e1) + "]",
        "        cnt += 1",
        "        if (cnt & 15) == 0:",
        "            dp = [" + mod_exprs + "]",
        "    return (" + ans_expr + ") % MOD",
    ]

    ns = {}
    exec("\n".join(lines), ns)
    process = ns["process"]

    print(process(s))


if __name__ == "__main__":
    solve()