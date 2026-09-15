import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    cnt = Counter(map(int, data[1:1 + n]))
    del data

    items = []
    max_a = 0
    for v, c in cnt.items():
        if v > max_a:
            max_a = v
        items.append((v, c, v * c))
    del cnt

    u = len(items)
    max_sum = max_a * 2
    ans = 0

    # Dense arrays are faster for small/moderate moduli.
    # For very large moduli, use a dictionary over only present residues.
    ARRAY_LIMIT = 1 << 19
    array_threshold = u * 4

    for k in range(max_sum.bit_length()):
        t = 1 << k
        m = t << 1
        mask = m - 1

        if m <= ARRAY_LIMIT and m <= array_threshold:
            counts = [0] * m
            sums = [0] * m
            touched = []
            append = touched.append

            for v, c, cv in items:
                r = v & mask
                if counts[r] == 0:
                    append(r)
                    counts[r] = c
                    sums[r] = cv
                else:
                    counts[r] += c
                    sums[r] += cv

            # Cross residue classes: count each unordered pair once.
            for r in touched:
                comp = (t - r) & mask
                if r < comp:
                    c = counts[r]
                    s = sums[r]
                    c2 = counts[comp]
                    if c2:
                        ans += (c * sums[comp] + c2 * s) >> k

            # Self-complementary residues for k >= 1:
            # 2*r == 2^k (mod 2^{k+1})
            if k:
                half = t >> 1

                c = counts[half]
                if c:
                    ans += ((c + 1) * sums[half]) >> k

                r = half + t
                c = counts[r]
                if c:
                    ans += ((c + 1) * sums[r]) >> k

            del counts, sums, touched, append

        else:
            d = {}
            get = d.get

            for v, c, cv in items:
                r = v & mask
                item = get(r)
                if item is None:
                    d[r] = [c, cv]
                else:
                    item[0] += c
                    item[1] += cv

            get = d.get

            # Cross residue classes.
            for r, item in d.items():
                comp = (t - r) & mask
                if r < comp:
                    item2 = get(comp)
                    if item2 is not None:
                        ans += (item[0] * item2[1] + item2[0] * item[1]) >> k

            # Self-complementary residues for k >= 1.
            if k:
                half = t >> 1

                item = get(half)
                if item is not None:
                    ans += ((item[0] + 1) * item[1]) >> k

                item = get(half + t)
                if item is not None:
                    ans += ((item[0] + 1) * item[1]) >> k

            del d, get

    print(ans)


if __name__ == "__main__":
    main()