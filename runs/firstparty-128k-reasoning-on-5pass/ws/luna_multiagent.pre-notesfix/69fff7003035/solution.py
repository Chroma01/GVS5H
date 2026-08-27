import sys

MOD = 998244353


def solve():
    n = int(sys.stdin.readline())

    # Group numbers by their decimal digit length.
    counts = [0] * 7
    sums = [0] * 7
    for x in range(1, n + 1):
        d = len(str(x))
        counts[d] += 1
        sums[d] += x
        if sums[d] >= MOD:
            sums[d] -= MOD

    groups = []
    for d in range(1, 7):
        if counts[d]:
            a = pow(10, d, MOD)
            groups.append((a, counts[d], sums[d]))

    dcnt = len(groups)

    # Q(y) = product over groups (1 + a*y).
    q = [1]
    for a, _, _ in groups:
        nq = [0] * (len(q) + 1)
        for i, v in enumerate(q):
            nq[i] = (nq[i] + v) % MOD
            nq[i + 1] = (nq[i + 1] + v * a) % MOD
        q = nq

    # R(y) = sum over groups c*a * product of (1 + other_a*y).
    r = [0] * dcnt
    for omitted, (a, c, _) in enumerate(groups):
        poly = [1]
        for j, (b, _, _) in enumerate(groups):
            if j == omitted:
                continue
            npoly = [0] * (len(poly) + 1)
            for i, v in enumerate(poly):
                npoly[i] = (npoly[i] + v) % MOD
                npoly[i + 1] = (npoly[i + 1] + v * b) % MOD
            poly = npoly

        multiplier = c * a % MOD
        for i, v in enumerate(poly):
            r[i] = (r[i] + multiplier * v) % MOD

    # F(y) = product over all numbers (1 + 10^digits(x) * y).
    # It satisfies Q(y) F'(y) = R(y) F(y).
    f = [0] * (n + 1)
    f[0] = 1

    inv = [0] * (n + 1)
    if n >= 1:
        inv[1] = 1
        for i in range(2, n + 1):
            inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    for deg in range(1, n + 1):
        rhs = 0
        for j in range(min(dcnt - 1, deg - 1) + 1):
            rhs += r[j] * f[deg - 1 - j]
        rhs %= MOD

        lhs_extra = 0
        for j in range(1, min(dcnt, deg - 1) + 1):
            lhs_extra += q[j] * (deg - j) * f[deg - j]
        lhs_extra %= MOD

        f[deg] = (rhs - lhs_extra) * inv[deg] % MOD

    # Factorials for the number of arrangements before/after a fixed element.
    fac = [1] * (n + 1)
    for i in range(1, n + 1):
        fac[i] = fac[i - 1] * i % MOD

    answer = 0

    # For an element from a group with multiplier a, remove one factor
    # (1 + a*y) from F to obtain the subset generating polynomial.
    for a, _, group_sum in groups:
        prev = 0
        contribution_factor = 0

        for k in range(n):
            cur = (f[k] - a * prev) % MOD
            prev = cur
            contribution_factor += cur * fac[k] % MOD * fac[n - 1 - k] % MOD
            if contribution_factor >= MOD:
                contribution_factor -= MOD

        answer = (answer + group_sum * contribution_factor) % MOD

    print(answer)


if __name__ == "__main__":
    solve()