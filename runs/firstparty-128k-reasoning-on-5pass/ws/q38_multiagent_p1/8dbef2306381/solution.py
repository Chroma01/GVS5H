import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M, A, B = data[0], data[1], data[2], data[3]
    bad = []
    idx = 4
    for _ in range(M):
        L = data[idx]
        R = data[idx + 1]
        idx += 2
        if bad and L <= bad[-1][1] + 1:
            if R > bad[-1][1]:
                bad[-1] = (bad[-1][0], R)
        else:
            bad.append((L, R))

    gaps = []
    cur = 1
    for L, R in bad:
        if R - L + 1 >= B:
            print("No")
            return
        if cur <= L - 1:
            gaps.append((cur, L - 1))
        cur = R + 1
    if cur <= N:
        gaps.append((cur, N))

    G = len(gaps)
    S = [0] * G
    E = [0] * G
    last_start = [0] * G
    last_len = [0] * G
    off = [0] * G
    first_valid = [0] * G
    for i, (s, e) in enumerate(gaps):
        S[i] = s
        E[i] = e
        ln = e - s + 1
        ll = B if ln >= B else ln
        last_len[i] = ll
        ls = e - ll + 1
        last_start[i] = ls
        off[i] = ls - s
        first_valid[i] = (1 << ll) - 1

    if A < B:
        diff = B - A
        K = (A - 1 + diff - 1) // diff
        T = max(1, K * A)
    else:
        T = 0
    LIMIT = max(1000, T + B + 5)
    small = [False] * (LIMIT + 1)
    for d in range(LIMIT + 1):
        if d == 0:
            small[d] = True
        else:
            small[d] = (d + B - 1) // B <= d // A

    bits = [1 << i for i in range(B)]
    entry = [0] * G
    entry[0] = 1 & first_valid[0]
    jump_range = range(A, B + 1)

    for g in range(G):
        em = entry[g] & first_valid[g]
        if em == 0:
            if g == G - 1:
                print("No")
                return
            continue

        ll = last_len[g]
        og = off[g]
        if A < B:
            max_e = em.bit_length() - 1
            if og - max_e >= T:
                exit_mask = (1 << ll) - 1
            else:
                exit_mask = 0
                m = em
                while m:
                    lsb = m & -m
                    eb = lsb.bit_length() - 1
                    m ^= lsb
                    st = eb - og
                    if st < 0:
                        st = 0
                    for t in range(st, ll):
                        D = og + t - eb
                        if D < LIMIT:
                            ok = small[D]
                        else:
                            ok = True
                        if ok:
                            exit_mask |= bits[t]
        else:
            a = A
            exit_mask = 0
            m = em
            while m:
                lsb = m & -m
                eb = lsb.bit_length() - 1
                m ^= lsb
                st = eb - og
                if st < 0:
                    st = 0
                for t in range(st, ll):
                    D = og + t - eb
                    if D < LIMIT:
                        ok = small[D]
                    else:
                        ok = (D % a == 0)
                    if ok:
                        exit_mask |= bits[t]

        if g == G - 1:
            bit = E[g] - last_start[g]
            if (exit_mask >> bit) & 1:
                print("Yes")
            else:
                print("No")
            return

        if exit_mask == 0:
            continue

        Eg = E[g]
        ls = last_start[g]
        jumped = 0
        for d in jump_range:
            jumped |= exit_mask << d
        max_t = exit_mask.bit_length() - 1
        for h in range(g + 1, G):
            Sh = S[h]
            if Sh - Eg > B:
                break
            shift = Sh - ls
            if shift > B + max_t:
                continue
            cand = jumped >> shift
            if cand:
                entry[h] |= cand & first_valid[h]

    print("No")

if __name__ == "__main__":
    solve()