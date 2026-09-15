import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    A = data[1:1 + n]
    del data

    if n == 0:
        print(0)
        return

    max_a = max(A)
    limit = max_a << 1
    K = limit.bit_length()

    # Maximum modulus actually used is 2^K.
    max_m = 1 << K

    # Use direct arrays for small moduli, dictionary for larger ones.
    SMALL = min(1 << 18, max_m)
    cnt = [0] * (SMALL + 1)
    sm = [0] * (SMALL + 1)

    ans = 0
    arr = A

    for k in range(K):
        half = 1 << k
        m = half << 1
        mask = m - 1

        if m <= SMALL:
            touched = []
            cnt_l = cnt
            sm_l = sm
            mask_l = mask
            append = touched.append

            for x in arr:
                r = x & mask_l
                if cnt_l[r] == 0:
                    append(r)
                    cnt_l[r] = 1
                    sm_l[r] = x
                else:
                    cnt_l[r] += 1
                    sm_l[r] += x

            for r in touched:
                cr = cnt_l[r]
                sr = sm_l[r]
                c = (half - r) & mask_l

                if r < c:
                    cc = cnt_l[c]
                    if cc:
                        ans += (cr * sm_l[c] + cc * sr) >> k
                elif r == c:
                    ans += ((cr + 1) * sr) >> k

            for r in touched:
                cnt_l[r] = 0
                sm_l[r] = 0

        else:
            d = {}
            get = d.get

            for x in arr:
                r = x & mask
                v = get(r)
                if v is None:
                    d[r] = [1, x]
                else:
                    v[0] += 1
                    v[1] += x

            for r, v in d.items():
                cr = v[0]
                sr = v[1]
                c = (half - r) & mask

                if r < c:
                    w = get(c)
                    if w is not None:
                        ans += (cr * w[1] + w[0] * sr) >> k
                elif r == c:
                    ans += ((cr + 1) * sr) >> k

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()