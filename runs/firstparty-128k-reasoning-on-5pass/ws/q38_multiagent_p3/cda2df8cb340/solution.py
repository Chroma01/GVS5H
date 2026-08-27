import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    del data

    if n == 0:
        print(0)
        return

    max_a = max(A)
    limit = 2 * max_a
    ans = 0

    # We only need t with 2^t <= 2*maxA.
    max_t = limit.bit_length() - 1

    # Hybrid aggregation:
    # - small moduli: reusable arrays
    # - large moduli: dictionary
    ARRAY_BITS = 20
    array_bits = min(ARRAY_BITS, max_t + 1)
    array_max_m = 1 << array_bits

    cnt = [0] * array_max_m
    sm = [0] * array_max_m

    half = 1
    while half <= limit:
        M = half << 1
        mask = M - 1

        if M <= array_max_m:
            used = []
            append = used.append
            cnt_l = cnt
            sm_l = sm

            for a in A:
                r = a & mask
                if cnt_l[r]:
                    cnt_l[r] += 1
                    sm_l[r] += a
                else:
                    append(r)
                    cnt_l[r] = 1
                    sm_l[r] = a

            add = 0
            for r in used:
                c = cnt_l[r]
                s = sm_l[r]
                sr = (half - r) & mask

                if sr == r:
                    add += s * (c + 1)
                elif r < sr:
                    add += cnt_l[sr] * s + c * sm_l[sr]

            ans += add // half

            for r in used:
                cnt_l[r] = 0
                sm_l[r] = 0

        else:
            d = {}
            get = d.get

            for a in A:
                r = a & mask
                v = get(r)
                if v is None:
                    d[r] = [1, a]
                else:
                    v[0] += 1
                    v[1] += a

            add = 0
            for r, v in d.items():
                c = v[0]
                s = v[1]
                sr = (half - r) & mask

                if sr == r:
                    add += s * (c + 1)
                elif r < sr:
                    w = get(sr)
                    if w is not None:
                        add += w[0] * s + c * w[1]

            ans += add // half

        half <<= 1

    print(ans)

if __name__ == "__main__":
    solve()