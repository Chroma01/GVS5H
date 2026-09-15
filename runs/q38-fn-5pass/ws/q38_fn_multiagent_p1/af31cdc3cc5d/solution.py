import sys
from heapq import heappush, heappop


def half_values(seq, n):
    """
    For every even length i, res[i] =
    sum(largest i/2 elements) - sum(smallest i/2 elements)
    among the first i elements of seq.
    """
    res = [0] * (n + 1)

    # low: max-heap via negatives, stores the smallest floor(i/2) elements
    # high: min-heap, stores the largest ceil(i/2) elements
    low = []
    high = []
    s_low = 0
    s_high = 0
    low_len = 0
    high_len = 0

    push = heappush
    pop = heappop

    for i, x in enumerate(seq, 1):
        if high_len and x < high[0]:
            push(low, -x)
            s_low += x
            low_len += 1
        else:
            push(high, x)
            s_high += x
            high_len += 1

        # Maintain len(high) == len(low) or len(high) == len(low) + 1.
        if high_len > low_len + 1:
            y = pop(high)
            s_high -= y
            high_len -= 1
            push(low, -y)
            s_low += y
            low_len += 1
        elif low_len > high_len:
            y = -pop(low)
            s_low -= y
            low_len -= 1
            push(high, y)
            s_high += y
            high_len += 1

        if not (i & 1):
            res[i] = s_high - s_low

    return res


def solve():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    a = list(map(int, tokens[1:1 + n]))
    del tokens

    pref = half_values(a, n)

    if n % 2 == 0:
        print(pref[n])
        return

    # suff[j] is the value for the last j elements of the original array.
    suff = half_values(reversed(a), n)

    ans = 0
    # The final survivor must be at a 0-based even index (1-based odd index).
    for p in range(0, n, 2):
        val = pref[p] + suff[n - p - 1]
        if val > ans:
            ans = val

    print(ans)


if __name__ == "__main__":
    solve()