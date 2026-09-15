import sys
from bisect import bisect_right


def parse_gaps(s: bytes):
    gaps = []
    append = gaps.append
    first = -1
    prev = -1
    cnt = 0
    for i, ch in enumerate(s):
        if ch == 49:  # '1'
            if first < 0:
                first = i
            else:
                append(i - prev)
            prev = i
            cnt += 1
    return cnt, first, prev, gaps


def solve_case(A: bytes, B: bytes):
    M, a0, a1, d = parse_gaps(A)
    Q, b0, b1, f = parse_gaps(B)

    if Q > M:
        return -1

    # Total gap reduction.  It is also (a_last - a_first) - (b_last - b_first).
    S = (a1 - a0) - (b1 - b0)
    if S < 0:
        return -1

    # L = movement of first piece, R = left movement of last piece.
    L = b0 - a0
    R = a1 - b1
    D = L - R

    P = len(d)
    K = len(f)

    # No final gaps: all initial gaps are internal and positive.
    if K == 0:
        return (S + abs(D)) // 2

    INF = P + 1

    # pref[j] = earliest last index after matching first j final gaps
    # using only strict matches d_i > f_j.
    pref = [INF] * (K + 1)
    pref[0] = -1
    j = 0
    for i, dv in enumerate(d):
        if j < K and dv > f[j]:
            j += 1
            pref[j] = i
            if j == K:
                # All gaps can be kept positive.  This is always optimal.
                return (S + abs(D)) // 2

    # Equality positions grouped by value and prefix parity of d.
    dpref = bytearray(P)
    eq = {}
    par = 0
    for i, dv in enumerate(d):
        par ^= (dv & 1)
        dpref[i] = par
        lst = eq.get(dv)
        if lst is None:
            lst = [[], []]
            eq[dv] = lst
        lst[par].append(i)

    # Prefix parity of final gaps.
    fpref = bytearray(K)
    par = 0
    for j, fv in enumerate(f):
        par ^= (fv & 1)
        fpref[j] = par

    ans = 10**30

    # For a zero gap (exact match) at initial index i and final index j,
    # define H = Dpref[i] xor Fpref[j].  All exact matches used must have
    # the same H.  Try both possible H values.
    ps = [0, 1]
    cost_of = {}
    for p in ps:
        q = (S & 1) ^ p
        cost_of[p] = (S + p + q + abs(D + p - q)) // 2
    ps.sort(key=cost_of.get)

    br = bisect_right

    for p in ps:
        cost_p = cost_of[p]
        if cost_p >= ans:
            continue

        # suff[t] = latest possible index of final gap t in a right-greedy
        # matching of suffix t..K-1 using strict matches or exact matches
        # with H == p.  suff[K] = P is the empty-suffix sentinel.
        suff = [-1] * (K + 1)
        suff[K] = P
        need = K - 1

        d_list = d
        f_list = f
        dp = dpref
        fp = fpref
        suff_local = suff

        for i in range(P - 1, -1, -1):
            if need < 0:
                break
            dv = d_list[i]
            fv = f_list[need]
            if dv > fv or (dv == fv and ((dp[i] ^ fp[need]) == p)):
                suff_local[need] = i
                need -= 1
                if need < 0:
                    break

        feasible = False

        # Choose the first exact match (c, j).
        # Prefix 0..j-1 must be strict before c.
        # Suffix j+1..K-1 must be allowed after c.
        for j in range(K):
            left = pref[j]
            if left >= P:
                continue
            limit = suff[j + 1]
            if limit <= left + 1:
                continue

            fv = f[j]
            lst = eq.get(fv)
            if lst is None:
                continue

            # Need Dpref[c] xor Fpref[j] == p.
            arr = lst[p ^ fp[j]]
            pos = br(arr, left)
            if pos < len(arr) and arr[pos] < limit:
                feasible = True
                break

        if feasible:
            ans = cost_p

    return -1 if ans == 10**30 else ans


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    idx = 1
    out = []

    for _ in range(t):
        # N is not needed explicitly.
        idx += 1
        A = data[idx]
        idx += 1
        B = data[idx]
        idx += 1
        out.append(str(solve_case(A, B)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()