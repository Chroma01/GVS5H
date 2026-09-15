import sys

MOD = 998244353
INV2 = (MOD + 1) // 2


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    s = data[1].strip()
    if len(s) > N:
        s = s[:N]

    # Relations on {0,1} are stored as 4-bit masks.
    # bit 0: 0->0, bit 1: 0->1, bit 2: 1->0, bit 3: 1->1.
    # comp[r][t] = r followed by t.
    comp = [[0] * 16 for _ in range(16)]
    for r in range(16):
        for t in range(16):
            res = 0
            if r & 1:  # 0->0
                if t & 1:
                    res |= 1
                if t & 2:
                    res |= 2
            if r & 2:  # 0->1
                if t & 4:
                    res |= 1
                if t & 8:
                    res |= 2
            if r & 4:  # 1->0
                if t & 1:
                    res |= 4
                if t & 2:
                    res |= 8
            if r & 8:  # 1->1
                if t & 4:
                    res |= 4
                if t & 8:
                    res |= 8
            comp[r][t] = res

    # Transition relation for one vertex, indexed by d_i.
    # s_i = 0: d=0,1,2 only.
    T0 = [2, 9, 4, 0]
    # s_i = 1: d=0,1,2,3.
    T1 = [2, 11, 13, 4]
    T = (T0, T1)
    allowed = ((0, 1, 2), (0, 1, 2, 3))

    # Swap states 0 <-> 1.
    swap = [0] * 16
    for r in range(16):
        swap[r] = ((r & 1) << 3) | ((r & 2) << 1) | ((r & 4) >> 1) | ((r & 8) >> 3)

    canon = [r if r < swap[r] else swap[r] for r in range(16)]

    # Live orbits under state-swap symmetry, excluding the empty relation.
    start = 9  # identity relation: 0->0 and 1->1
    start_c = canon[start]
    seen = {start_c}
    stack = [start_c]

    while stack:
        c = stack.pop()
        members = (c,) if swap[c] == c else (c, swap[c])
        for b in (0, 1):
            for d in allowed[b]:
                for r in members:
                    r2 = comp[r][T[b][d]]
                    if r2:
                        nc = canon[r2]
                        if nc not in seen:
                            seen.add(nc)
                            stack.append(nc)

    reps = sorted(seen)
    oid = {c: i for i, c in enumerate(reps)}
    S = len(reps)
    init = oid[start_c]

    # Orbit sizes and final acceptance weights.
    inv_sizes = [0] * S
    weights = [0] * S
    for i, c in enumerate(reps):
        if swap[c] == c:
            members = (c,)
            inv = 1
        else:
            members = (c, swap[c])
            inv = INV2
        inv_sizes[i] = inv

        acc = 0
        for r in members:
            if (r & 1) or (r & 8):  # has (0,0) or (1,1)
                acc += 1
        weights[i] = acc * inv % MOD

    # One-step aggregated transitions.
    # For an orbit, transition multiplicity is averaged over its members.
    single_edges = [[], []]
    for b in (0, 1):
        edges = []
        for src, c in enumerate(reps):
            if swap[c] == c:
                members = (c,)
                inv = 1
            else:
                members = (c, swap[c])
                inv = INV2

            counts = [0] * S
            for r in members:
                for d in allowed[b]:
                    r2 = comp[r][T[b][d]]
                    if r2:
                        counts[oid[canon[r2]]] += 1

            for dst, val in enumerate(counts):
                if val:
                    coeff = val * inv % MOD
                    if coeff:
                        edges.append((src, dst, coeff))

        single_edges[b] = tuple(edges)

    # Precompute transitions for all 10-bit blocks of s.
    B = 10
    block_edges = [()] * (1 << B)
    se = single_edges
    mod = MOD

    for p in range(1 << B):
        edges = []
        for src in range(S):
            vec = [0] * S
            vec[src] = 1

            # Input blocks are built most-significant-bit first.
            for pos in range(B - 1, -1, -1):
                b = (p >> pos) & 1
                new = [0] * S
                for sr, dst, m in se[b]:
                    vs = vec[sr]
                    if vs:
                        new[dst] = (new[dst] + vs * m) % mod
                vec = new

            for dst, val in enumerate(vec):
                if val:
                    edges.append((src, dst, val))

        block_edges[p] = tuple(edges)

    # Process the string in 10-bit blocks.
    dp = [0] * S
    dp[init] = 1

    idx = 0
    cnt = 0
    be = block_edges

    for ch in s:
        idx = (idx << 1) | (ch & 1)
        cnt += 1
        if cnt == B:
            ndp = [0] * S
            for sr, dst, m in be[idx]:
                ndp[dst] += dp[sr] * m
            dp = [x % mod for x in ndp]
            idx = 0
            cnt = 0

    # Remaining fewer than B characters.
    if cnt:
        for ch in s[-cnt:]:
            edges = se[1] if (ch & 1) else se[0]
            ndp = [0] * S
            for sr, dst, m in edges:
                ndp[dst] += dp[sr] * m
            dp = [x % mod for x in ndp]

    ans = 0
    for val, w in zip(dp, weights):
        ans = (ans + val * w) % mod

    print(ans)


if __name__ == "__main__":
    solve()