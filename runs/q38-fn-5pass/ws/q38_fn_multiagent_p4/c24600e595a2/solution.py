import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    b = data[1 + n:1 + 2 * n]
    c = data[1 + 2 * n:1 + 3 * n]

    off = []          # A=1, B=0: forced flips ending in 0
    on = []           # A=0, B=1: forced flips ending in 1
    matched_one = []  # A=1, B=1: optional off/on pairs

    s0 = 0
    sum_off = 0
    sum_on = 0

    for ai, bi, ci in zip(a, b, c):
        if ai == 1:
            s0 += ci
            if bi == 0:
                off.append(ci)
                sum_off += ci
            else:
                matched_one.append(ci)
        else:
            if bi == 1:
                on.append(ci)
                sum_on += ci

    off.sort()
    on.sort()
    matched_one.sort(reverse=True)

    m = len(off)
    p = len(on)

    # For sorted ascending values, sum of max over all unordered pairs.
    pairmax_off = 0
    for i, v in enumerate(off):
        pairmax_off += v * i

    # For sorted ascending values, sum of min over all unordered pairs.
    pairmin_on = 0
    for i, v in enumerate(on):
        pairmin_on += v * (p - 1 - i)

    pref_off = [0] * (m + 1)
    for i, v in enumerate(off):
        pref_off[i + 1] = pref_off[i] + v

    pref_on = [0] * (p + 1)
    for i, v in enumerate(on):
        pref_on[i + 1] = pref_on[i] + v

    base = m + p

    # k = 0
    ans = (
        base * s0
        - (p + 1) * sum_off
        + sum_on
        - pairmax_off
        + pairmin_on
    )

    sum_x = 0
    pairmax_x = 0
    pairmin_x = 0
    cross_ox = 0
    cross_ix = 0
    k = 0

    # Two pointers because matched_one is scanned in descending order.
    idx_off = m  # number of off values <= current x
    idx_on = p   # number of on values < current x

    for x in matched_one:
        while idx_off > 0 and off[idx_off - 1] > x:
            idx_off -= 1
        cross_ox += x * idx_off + (sum_off - pref_off[idx_off])

        while idx_on > 0 and on[idx_on - 1] >= x:
            idx_on -= 1
        cross_ix += pref_on[idx_on] + x * (p - idx_on)

        # Add x to the selected optional set.
        # Since x is no larger than all previously selected values:
        # new pair maxima are the previous values; new pair minima are x.
        pairmax_x += sum_x
        pairmin_x += x * k
        sum_x += x
        k += 1

        val = (
            (base + 2 * k) * s0
            - (p + k + 1) * (sum_off + sum_x)
            + (sum_on + sum_x)
            - (pairmax_off + pairmax_x + cross_ox)
            + (pairmin_on + pairmin_x + cross_ix)
        )
        if val < ans:
            ans = val

    print(ans)


if __name__ == "__main__":
    solve()