import sys


def current_answer(seq):
    n = len(seq)
    if n == 0:
        return 0

    # 1-based run arrays: v[1..m], l[1..m]
    v = [0]
    l = [0]

    prev = seq[0]
    cnt = 1
    for a in seq[1:]:
        if a == prev:
            cnt += 1
        else:
            v.append(prev)
            l.append(cnt)
            prev = a
            cnt = 1

    v.append(prev)
    l.append(cnt)
    m = len(v) - 1

    if m < 4:
        return m

    # F[p]: if a neutral chain is active with current pair (p-2, p),
    # the end index of the final beneficial reduction, or 0.
    F = [0] * (m + 3)
    for p in range(m, 0, -1):
        if (
            p >= 3
            and p + 2 <= m
            and l[p - 2] == 1
            and l[p] == 1
            and l[p + 1] == 1
            and v[p + 1] == v[p - 2]
        ):
            if v[p + 2] == v[p]:
                F[p] = p + 2
            elif l[p + 2] == 1:
                F[p] = F[p + 2]

    # dp[i]: maximum number of net-saving blocks before run i.
    dp = [0] * (m + 3)

    for i in range(1, m + 1):
        di = dp[i]

        # Skip run i.
        if di > dp[i + 1]:
            dp[i + 1] = di

        # Start a block at i: runs i, i+1, i+2 are x, y, x
        # with y and x singleton.
        if (
            i + 3 <= m
            and v[i] == v[i + 2]
            and l[i + 1] == 1
            and l[i + 2] == 1
        ):
            p = i + 3
            if v[p] == v[p - 2]:
                # Direct beneficial pattern x, y, x, y.
                end = p
            elif l[p] == 1:
                # Neutral move, then follow the deterministic chain.
                end = F[p]
            else:
                end = 0

            if end:
                nd = di + 1
                if nd > dp[end]:
                    dp[end] = nd

    return m - dp[m]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        seq = data[idx:idx + n]
        idx += n
        out.append(str(current_answer(seq)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()