import sys
from heapq import heappush, heappop


def even_scores(seq):
    # low: max-heap (stored negated) for the smaller half
    # high: min-heap for the larger half
    low = []
    high = []
    total = 0
    sum_low = 0
    res = [0]
    append = res.append
    push = heappush
    pop = heappop

    it = iter(seq)
    try:
        x = next(it)
    except StopIteration:
        return res

    total = x
    push(low, -x)
    sum_low = x

    for i, x in enumerate(it, 2):
        total += x

        if x <= -low[0]:
            push(low, -x)
            sum_low += x
        else:
            push(high, x)

        if len(low) > len(high) + 1:
            v = -pop(low)
            sum_low -= v
            push(high, v)
        elif len(high) > len(low) + 1:
            v = pop(high)
            push(low, -v)
            sum_low += v

        if not (i & 1):
            append(total - 2 * sum_low)

    return res


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    del data

    if n % 2 == 0:
        ans = even_scores(a)[n // 2]
    else:
        m = n // 2
        pref = even_scores(a)
        suff = even_scores(reversed(a))

        ans = 0
        for p, s in zip(pref, reversed(suff)):
            v = p + s
            if v > ans:
                ans = v

    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()