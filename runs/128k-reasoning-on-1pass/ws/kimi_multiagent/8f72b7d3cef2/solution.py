import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    A = [0] * (n + 1)
    for i in range(1, n + 1):
        A[i] = int(data[i])

    # Prefix sums P[i] = A_1 + ... + A_i
    P = [0] * (n + 1)
    s = 0
    for i in range(1, n + 1):
        s += A[i]
        P[i] = s

    size = 1
    while size < n:
        size <<= 1
    base = size - 1
    INF = 10 ** 30

    # Right blocker for current left border l:
    #   A_j >= P[j-1] - P[l-1]  <=>  P[j-1] - A_j <= P[l-1]
    # So store Rkey[j] = P[j-1] - A_j and find first Rkey[j] <= threshold.
    rmin = [INF] * (2 * size)

    # Left blocker for current right border r:
    #   A_i >= P[r] - P[i]  <=>  P[i] + A_i >= P[r]
    # So store Lkey[i] = P[i] + A_i and find last Lkey[i] >= threshold.
    lmax = [-INF] * (2 * size)

    for i in range(1, n + 1):
        ai = A[i]
        rmin[base + i] = P[i - 1] - ai
        lmax[base + i] = P[i] + ai

    for i in range(size - 1, 0, -1):
        x = rmin[i << 1]
        y = rmin[(i << 1) + 1]
        rmin[i] = x if x < y else y
        x = lmax[i << 1]
        y = lmax[(i << 1) + 1]
        lmax[i] = x if x > y else y

    A = None
    data = None

    def first_leq(pos: int, X: int) -> int:
        """First index in [pos, n] with Rkey[index] <= X, or n+1."""
        if pos > n:
            return n + 1
        idx = base + pos
        if rmin[idx] <= X:
            return pos

        # Any index after pos lies in exactly one right sibling on the path
        # from leaf pos to the root. Scan those siblings from near to far.
        while idx > 1:
            if (idx & 1) == 0:  # idx is a left child; idx+1 is entirely after pos
                sib = idx + 1
                if rmin[sib] <= X:
                    node = sib
                    while node < size:
                        node <<= 1
                        if rmin[node] > X:
                            node += 1
                    res = node - base
                    return res if res <= n else n + 1
            idx >>= 1
        return n + 1

    def last_geq(pos: int, Y: int) -> int:
        """Last index in [1, pos] with Lkey[index] >= Y, or 0."""
        if pos < 1:
            return 0
        idx = base + pos
        if lmax[idx] >= Y:
            return pos

        # Symmetric to first_leq: scan left siblings from near to far.
        while idx > 1:
            if idx & 1:  # idx is a right child; idx-1 is entirely before pos
                sib = idx - 1
                if lmax[sib] >= Y:
                    node = sib
                    while node < size:
                        node = (node << 1) + 1
                        if lmax[node] < Y:
                            node -= 1
                    res = node - base
                    return res if res >= 1 else 0
            idx >>= 1
        return 0

    out = []
    append = out.append

    for k in range(1, n + 1):
        l = k
        r = k

        while True:
            old_l = l
            old_r = r

            # Expand right maximally while the left border is fixed.
            b = first_leq(r + 1, P[l - 1])
            nr = b - 1
            if nr > r:
                r = nr

            # Expand left maximally while the right border is fixed.
            a = last_geq(l - 1, P[r])
            nl = a + 1
            if nl < l:
                l = nl

            if l == old_l and r == old_r:
                break
            if l == 1 and r == n:
                break

        append(str(P[r] - P[l - 1]))

    sys.stdout.write(" ".join(out))


if __name__ == "__main__":
    solve()