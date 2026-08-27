import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    del data

    total = sum(a)
    max_a = max(a)

    # Maximum possible pair sum is 2 * max_a (self-pair is allowed).
    max_m = (2 * max_a).bit_length() - 1

    # Sum of (A_i + A_j) over all i <= j.
    ans = (n + 1) * total

    # Packed residue aggregate: (sum_of_values << SHIFT) | count.
    # count <= 2e5 < 2^19.
    SHIFT = 19
    MASK = (1 << SHIFT) - 1

    # Dense array only up to 2^20; larger moduli use dictionaries.
    dense_size = 1 << min(max_m, 20)
    arr = [0] * dense_size
    touched = []

    for m in range(1, max_m + 1):
        mod = 1 << m
        mask = mod - 1

        if mod <= dense_size:
            ar = arr
            t_append = touched.append

            for x in a:
                r = x & mask
                add = (x << SHIFT) + 1
                v = ar[r]
                if v:
                    ar[r] = v + add
                else:
                    ar[r] = add
                    t_append(r)

            agg = 0
            for r in touched:
                v = ar[r]
                s = (-r) & mask

                if r < s:
                    w = ar[s]
                    if w:
                        cr = v & MASK
                        sr = v >> SHIFT
                        cs = w & MASK
                        ss = w >> SHIFT
                        agg += cr * ss + cs * sr
                elif r == s:
                    cr = v & MASK
                    sr = v >> SHIFT
                    agg += (cr + 1) * sr

            for r in touched:
                ar[r] = 0
            touched.clear()

            ans -= agg >> m

        else:
            d = {}
            get = d.get

            for x in a:
                r = x & mask
                d[r] = get(r, 0) + (x << SHIFT) + 1

            agg = 0
            get = d.get

            for r, v in d.items():
                s = (-r) & mask

                if r < s:
                    w = get(s, 0)
                    if w:
                        cr = v & MASK
                        sr = v >> SHIFT
                        cs = w & MASK
                        ss = w >> SHIFT
                        agg += cr * ss + cs * sr
                elif r == s:
                    cr = v & MASK
                    sr = v >> SHIFT
                    agg += (cr + 1) * sr

            ans -= agg >> m

    print(ans)

if __name__ == "__main__":
    main()