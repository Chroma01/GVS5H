import sys
from bisect import bisect_left


def pairmin_asc(arr):
    n = len(arr)
    total = 0
    for i, x in enumerate(arr):
        total += x * (n - 1 - i)
    return total


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    base = 1

    d = []  # A=1, B=0: mandatory off flips
    u = []  # A=0, B=1: mandatory on flips
    o = []  # A=1, B=1: optionally off then on

    for i in range(n):
        ai = data[base + i]
        bi = data[base + n + i]
        ci = data[base + 2 * n + i]

        if ai == 1:
            if bi == 0:
                d.append(ci)
            else:
                o.append(ci)
        else:
            if bi == 1:
                u.append(ci)

    if not d and not u:
        print(0)
        return

    d.sort()
    u.sort()
    o.sort(reverse=True)

    pref_d = [0]
    for x in d:
        pref_d.append(pref_d[-1] + x)

    pref_u = [0]
    for x in u:
        pref_u.append(pref_u[-1] + x)

    pair_d = pairmin_asc(d)
    pair_u = pairmin_asc(u)
    sum_u = pref_u[-1]

    const = pair_d + pair_u + sum_u
    total_o = sum(o)

    len_d = len(d)
    len_u = len(u)
    m = len_d + len_u

    pref_s = 0
    pair_s = 0
    cross_d = 0
    cross_u = 0

    ans = 10**30

    for k in range(len(o) + 1):
        ops = m + 2 * k
        cost = (
            (total_o - pref_s) * ops
            + const
            + 2 * pair_s
            + cross_d
            + cross_u
            + pref_s
        )
        if cost < ans:
            ans = cost

        if k == len(o):
            break

        s = o[k]
        pref_s += s
        pair_s += s * k

        idx = bisect_left(d, s)
        cross_d += s * (len_d - idx) + pref_d[idx]

        idx = bisect_left(u, s)
        cross_u += s * (len_u - idx) + pref_u[idx]

    print(ans)


if __name__ == "__main__":
    main()