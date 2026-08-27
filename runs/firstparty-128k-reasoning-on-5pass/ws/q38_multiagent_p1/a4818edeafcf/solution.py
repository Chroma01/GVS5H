import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]

    # total occurrences of each value
    tot = [0] * (N + 1)
    K = 0
    for i in range(1, N + 1):
        x = data[i]
        if tot[x] == 0:
            K += 1
        tot[x] += 1

    # left cut positions are 1 .. N-2
    M = N - 2
    size = 1 << (M - 1).bit_length()

    NEG = -10**18
    sv = [0] * (2 * size)       # sum of D in the node interval
    bv = [NEG] * (2 * size)     # best prefix-D value in the node interval

    # Activate leaf pos: it becomes active with relative value D[pos].
    def activate(pos, bv=bv, sv=sv, sz=size):
        idx = sz + pos - 1
        bv[idx] = sv[idx]
        idx >>= 1
        while idx:
            lc = idx << 1
            rc = lc + 1
            s = sv[lc]
            sv[idx] = s + sv[rc]
            b = bv[lc]
            r = s + bv[rc]
            if r > b:
                b = r
            bv[idx] = b
            idx >>= 1

    # Point add +1 to an already active D[pos].
    def add(pos, bv=bv, sv=sv, sz=size):
        idx = sz + pos - 1
        sv[idx] += 1
        bv[idx] += 1
        idx >>= 1
        while idx:
            lc = idx << 1
            rc = lc + 1
            s = sv[lc]
            sv[idx] = s + sv[rc]
            b = bv[lc]
            r = s + bv[rc]
            if r > b:
                b = r
            bv[idx] = b
            idx >>= 1

    # Activate leaf pos and also apply D[pos] += 1.
    def add_activate(pos, bv=bv, sv=sv, sz=size):
        idx = sz + pos - 1
        sv[idx] += 1
        bv[idx] = sv[idx]
        idx >>= 1
        while idx:
            lc = idx << 1
            rc = lc + 1
            s = sv[lc]
            sv[idx] = s + sv[rc]
            b = bv[lc]
            r = s + bv[rc]
            if r > b:
                b = r
            bv[idx] = b
            idx >>= 1

    # Online computation of W[j] = #values with 0 < count_so_far < total.
    cnt = [0] * (N + 1)
    last = [0] * (N + 1)

    x1 = data[1]
    cnt[x1] = 1
    active = 1 if tot[x1] > 1 else 0
    last[x1] = 1

    ans = 0

    # Local bindings for speed.
    sv_l = sv
    bv_l = bv
    sz = size
    M_l = M
    tot_l = tot
    cnt_l = cnt
    last_l = last
    data_l = data
    act = activate
    ad = add
    ada = add_activate
    K_l = K

    # Right cut j runs from 2 to N-1.
    for j in range(2, N):
        x = data_l[j]

        # Update W[j] after including A[j].
        c = cnt_l[x]
        t = tot_l[x]
        if c == 0:
            cnt_l[x] = 1
            if t > 1:
                active += 1
        elif c == t - 1:
            cnt_l[x] = t
            active -= 1
        else:
            cnt_l[x] = c + 1

        p = last_l[x]
        i = j - 1

        if p == 0:
            act(i)
        elif p == i:
            ada(i)
            if j <= M_l:
                sv_l[sz + j - 1] -= 1
        else:
            act(i)
            ad(p)
            if j <= M_l:
                sv_l[sz + j - 1] -= 1

        val = K_l + active + bv_l[1]
        if val > ans:
            ans = val

        last_l[x] = j

    print(ans)


if __name__ == "__main__":
    main()