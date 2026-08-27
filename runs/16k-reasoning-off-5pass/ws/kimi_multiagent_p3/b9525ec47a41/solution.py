import sys

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    s = data[1].decode() if isinstance(data[1], bytes) else data[1]

    # ------------------------------------------------------------------
    # Model (verified against brute force):
    #   distinct d-sequences  <=>  distinct (u, sigma) where
    #     u_i = d_i - 1            (u in {-1,0,1} off S, {-1,0,1,2} on S)
    #     sigma = K - d_N = sum h  over a valid lift (t,h):
    #       t_i = u_i - h_i on S (h_i in {0,1}),  t_i = u_i off S,
    #       t arc-valid: all contiguous arc sums in [-1,1]
    #       <=> partial sums P stay in {-1,0,1}, never hitting both -1 and +1,
    #          and P_N = 0.
    #   For each u the achievable sigma form a contiguous interval [lo,hi];
    #   lo/hi are found by greedy lifts (min-greedy prefers h=0, max-greedy
    #   prefers h=1, keeping only completable branches via a suffix table).
    #   answer = sum_u (hi(u) - lo(u) + 1).
    # ------------------------------------------------------------------

    # state index: (p+1)*3 + m, p in {-1,0,1}, m in {0,1,2} (mask sn|sp<<1)
    # precompute for each state and each t in {-1,0,1} the successor state
    # or -1 if window constraint violated (|P|>1 or both signs seen).
    NEG = 1  # bit for having seen P=-1
    POS = 2  # bit for having seen P=+1
    trans = [[-1] * 3 for _ in range(9)]  # trans[state][t+1] -> state or -1
    for p in (-1, 0, 1):
        for m in (0, 1, 2):
            st = (p + 1) * 3 + m
            for t in (-1, 0, 1):
                q = p + t
                if q < -1 or q > 1:
                    continue
                m2 = m
                if q == -1:
                    m2 |= NEG
                elif q == 1:
                    m2 |= POS
                if m2 == 3:
                    continue
                trans[st][t + 1] = (q + 1) * 3 + m2

    # suffix feasibility: suf[i][state] = 1 if positions i..N-1 can complete
    # to P_N = 0 (any t in {-1,0,1} per position is achievable by some u).
    # Store as one flat bytearray of length (N+1)*9.
    suf = bytearray((N + 1) * 9)
    base = N * 9
    suf[base + 3] = 1  # (p=0,m=0)
    suf[base + 4] = 1  # (p=0,m=1)
    suf[base + 5] = 1  # (p=0,m=2)
    for i in range(N - 1, -1, -1):
        row = i * 9
        nxt = (i + 1) * 9
        for st in range(9):
            ok = 0
            for t in (-1, 0, 1):
                st2 = trans[st][t + 1]
                if st2 >= 0 and suf[nxt + st2]:
                    ok = 1
                    break
            suf[row + st] = ok

    # Precompute per (state, onS, prefer_max) the list of outcomes:
    # for each u-option: (next_state, h) of the greedy-chosen branch, or None.
    # u-options: off S: u=-1(t=-1,h=0), u=0(0,0), u=1(1,0)
    # on S: u=-1(-1,0), u=2(1,1), u=0: min[(0,0),(-1,1)] max[(-1,1),(0,0)]
    #       u=1: min[(1,0),(0,1)] max[(0,1),(1,0)]
    # We encode the greedy result as two parallel arrays:
    #   nxtA[pm][onS][st] : list of (st2, h) for chosen branches (<=4 entries)
    # Build lazily inside the loop instead: cheaper to inline.

    def run(prefer_max):
        cnt = [0] * 9
        sm = [0] * 9
        cnt[3] = 1  # state (p=0,m=0)
        s_local = s
        suf_local = suf
        trans_local = trans
        MODL = MOD
        for i in range(N):
            onS = s_local[i] == '1'
            nxt_row = (i + 1) * 9
            ncnt = [0] * 9
            nsm = [0] * 9
            if onS:
                if prefer_max:
                    # u: -1 -> [(-1,0)] ; 0 -> [(-1,1),(0,0)] ;
                    #    1 -> [(0,1),(1,0)] ; 2 -> [(1,1)]
                    opt0 = ((-1, 1), (0, 0))
                    opt1 = ((0, 1), (1, 0))
                else:
                    opt0 = ((0, 0), (-1, 1))
                    opt1 = ((1, 0), (0, 1))
                for st in range(9):
                    c = cnt[st]
                    if not c:
                        continue
                    sv = sm[st]
                    tr = trans_local[st]
                    # u = -1 : (t=-1,h=0)
                    st2 = tr[0]
                    if st2 >= 0 and suf_local[nxt_row + st2]:
                        ncnt[st2] = (ncnt[st2] + c) % MODL
                        nsm[st2] = (nsm[st2] + sv) % MODL
                    # u = 0 : greedy over opt0
                    for (t, h) in opt0:
                        st2 = tr[t + 1]
                        if st2 >= 0 and suf_local[nxt_row + st2]:
                            ncnt[st2] = (ncnt[st2] + c) % MODL
                            nsm[st2] = (nsm[st2] + sv + c * h) % MODL
                            break
                    # u = 1 : greedy over opt1
                    for (t, h) in opt1:
                        st2 = tr[t + 1]
                        if st2 >= 0 and suf_local[nxt_row + st2]:
                            ncnt[st2] = (ncnt[st2] + c) % MODL
                            nsm[st2] = (nsm[st2] + sv + c * h) % MODL
                            break
                    # u = 2 : (t=1,h=1)
                    st2 = tr[2]
                    if st2 >= 0 and suf_local[nxt_row + st2]:
                        ncnt[st2] = (ncnt[st2] + c) % MODL
                        nsm[st2] = (nsm[st2] + sv + c) % MODL
            else:
                for st in range(9):
                    c = cnt[st]
                    if not c:
                        continue
                    sv = sm[st]
                    tr = trans_local[st]
                    for t in (-1, 0, 1):
                        st2 = tr[t + 1]
                        if st2 >= 0 and suf_local[nxt_row + st2]:
                            ncnt[st2] = (ncnt[st2] + c) % MODL
                            nsm[st2] = (nsm[st2] + sv) % MODL
            cnt = ncnt
            sm = nsm
        tot_c = (cnt[3] + cnt[4] + cnt[5]) % MOD
        tot_s = (sm[3] + sm[4] + sm[5]) % MOD
        return tot_c, tot_s

    cnt_min, sum_lo = run(False)
    cnt_max, sum_hi = run(True)
    answer = (sum_hi - sum_lo + cnt_min) % MOD
    print(answer)

solve()