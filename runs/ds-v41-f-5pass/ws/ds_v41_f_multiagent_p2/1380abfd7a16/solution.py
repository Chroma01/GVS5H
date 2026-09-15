import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    # revP[j] = P_{n-j}: the insertion positions in reverse order.
    revP = [int(x) for x in data[n:0:-1]]
    del data

    # m = smallest power of two >= n; the Fenwick tree is padded with zeros
    # in positions n+1..m so the k-th-one search needs no bounds check.
    m = 1
    while m < n:
        m <<= 1

    # Fenwick tree of free slots: 1 at positions 1..n, 0 at n+1..m.
    # tr[i] = number of ones in the block (i - lowbit(i), i].
    tr = [0] * (m + 1)
    tr[1:n + 1] = [i & (-i) for i in range(1, n + 1)]
    if m > n:
        # i - (i & -i) == i & (i - 1)
        tr[n + 1:m + 1] = [
            n - (i & (i - 1)) if (i & (i - 1)) < n else 0
            for i in range(n + 1, m + 1)
        ]

    # Next node on the Fenwick update path.
    up = [0] + [i + (i & (-i)) for i in range(1, m + 1)]

    # Descending powers of two (largest power of two <= n, down to 1).
    bits = []
    b = 1 << (n.bit_length() - 1)
    while b:
        bits.append(b)
        b >>= 1

    ans = [0] * n

    # Emit an unrolled version of the k-th-free-slot search to remove the
    # per-probe loop bookkeeping.  All names are locals inside `run`.
    lines = [
        "def run(N, revP, tr, up, M, ans):",
        "    i = N",
        "    for k in revP:",
        "        pos = 0",
    ]
    for bit in bits:
        sb = str(bit)
        lines.append("        v = tr[pos + " + sb + "]")
        lines.append("        if v < k:")
        lines.append("            pos += " + sb)
        lines.append("            k -= v")
    lines += [
        "        idx = pos + 1",          # 1-indexed free slot for value i
        "        ans[idx - 1] = i",
        "        i -= 1",
        "        while idx <= M:",
        "            tr[idx] -= 1",
        "            idx = up[idx]",
    ]

    ns = {}
    exec("\n".join(lines), ns)
    ns["run"](n, revP, tr, up, m, ans)

    sys.stdout.write(' '.join(map(str, ans)) + '\n')


main()