import sys
from heapq import heappush, heappop


def prefix_scores(a):
    n = len(a)
    scores = [0] * (n + 1)

    # low: max-heap (store negatives), contains the smallest ceil(length/2) values
    # high: min-heap, contains the largest floor(length/2) values
    low = []
    high = []
    sum_low = 0
    sum_high = 0

    push = heappush
    pop = heappop

    for i, x in enumerate(a, 1):
        if not low or x <= -low[0]:
            push(low, -x)
            sum_low += x
        else:
            push(high, x)
            sum_high += x

        if len(low) > len(high) + 1:
            v = -pop(low)
            sum_low -= v
            push(high, v)
            sum_high += v
        elif len(high) > len(low):
            v = pop(high)
            sum_high -= v
            push(low, -v)
            sum_low += v

        if i % 2 == 0:
            scores[i] = sum_high - sum_low

    return scores


def suffix_scores(a):
    n = len(a)
    scores = [0] * (n + 1)

    low = []
    high = []
    sum_low = 0
    sum_high = 0

    push = heappush
    pop = heappop

    length = 0
    for idx in range(n - 1, -1, -1):
        x = a[idx]

        if not low or x <= -low[0]:
            push(low, -x)
            sum_low += x
        else:
            push(high, x)
            sum_high += x

        if len(low) > len(high) + 1:
            v = -pop(low)
            sum_low -= v
            push(high, v)
            sum_high += v
        elif len(high) > len(low):
            v = pop(high)
            sum_high -= v
            push(low, -v)
            sum_low += v

        length += 1
        if length % 2 == 0:
            scores[idx] = sum_high - sum_low

    return scores


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]
    del data

    pref = prefix_scores(a)

    if n % 2 == 0:
        print(pref[n])
        return

    suff = suffix_scores(a)

    ans = 0
    # For odd N, the final survivor must be at an even 0-based index.
    for k in range(0, n, 2):
        val = pref[k] + suff[k + 1]
        if val > ans:
            ans = val

    print(ans)


if __name__ == "__main__":
    main()