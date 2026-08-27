import sys


def build_gaps(s: bytes):
    """Return (count, first_pos, last_pos, gaps, right_endpoint_parity)."""
    prev = -1
    first = -1
    gaps = []
    par = bytearray()
    cnt = 0

    ga = gaps.append
    pa = par.append

    for i, ch in enumerate(s):
        if ch == 49:  # ord('1')
            if cnt == 0:
                first = i
            else:
                gap = i - prev
                ga(gap)
                pa((i - first) & 1)
            prev = i
            cnt += 1

    return cnt, first, prev, gaps, par


def solve_case(N: int, A: bytes, B: bytes) -> int:
    K, a0, a_last, alpha, S = build_gaps(A)
    L, b0, b_last, beta, R = build_gaps(B)

    if K < L:
        return -1

    spanA = a_last - a0
    spanB = b_last - b0
    if spanA < spanB:
        return -1

    d1 = b0 - a0
    dn = b_last - a_last
    D = spanA - spanB
    E = d1 + dn
    M = (D + (E if E >= 0 else -E)) // 2

    if L == 1:
        return M

    pM = (M + d1) & 1
    Lm1 = L - 1

    def feasible(p: int) -> bool:
        """One-pass greedy subsequence match for phase p."""
        j = 0
        g = beta[0]
        r = R[0] ^ p

        for v, s in zip(alpha, S):
            if v > g or (v == g and s == r):
                j += 1
                if j == Lm1:
                    return True
                g = beta[j]
                r = R[j] ^ p

        return False

    if feasible(pM):
        return M
    if feasible(1 - pM):
        return M + 1
    return -1


def main() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        N = int(data[idx])
        idx += 1
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1
        out.append(str(solve_case(N, A, B)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()