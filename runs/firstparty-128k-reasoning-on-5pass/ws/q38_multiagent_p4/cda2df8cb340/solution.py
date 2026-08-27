import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    del data

    total = sum(a)
    max_a = max(a)
    max_sum = max_a * 2

    # V_0 = sum_{i <= j} (A_i + A_j) = (N + 1) * sum(A)
    ans = (n + 1) * total

    # Dense arrays are faster for small moduli.
    LIMIT = 1 << 20
    m = 2

    while m <= max_sum:
        mask = m - 1

        if m <= LIMIT:
            cnt = [0] * m
            sm = [0] * m
            touched = []
            append = touched.append

            for x in a:
                r = x & mask
                c = cnt[r]
                if c:
                    cnt[r] = c + 1
                    sm[r] = sm[r] + x
                else:
                    append(r)
                    cnt[r] = 1
                    sm[r] = x

            vt = 0
            for r in touched:
                cr = cnt[r]
                sr = sm[r]
                s = (-r) & mask

                if s == r:
                    vt += (cr + 1) * sr // m
                elif r < s:
                    cs = cnt[s]
                    if cs:
                        vt += (cr * sm[s] + cs * sr) // m

            ans -= vt

        else:
            cnt = {}
            sm = {}
            cnt_get = cnt.get

            for x in a:
                r = x & mask
                c = cnt_get(r, 0)
                if c:
                    cnt[r] = c + 1
                    sm[r] = sm[r] + x
                else:
                    cnt[r] = 1
                    sm[r] = x

            vt = 0
            for r, cr in cnt.items():
                sr = sm[r]
                s = (-r) & mask

                if s == r:
                    vt += (cr + 1) * sr // m
                elif r < s:
                    cs = cnt_get(s, 0)
                    if cs:
                        vt += (cr * sm[s] + cs * sr) // m

            ans -= vt

        m <<= 1

    print(ans)

if __name__ == "__main__":
    solve()