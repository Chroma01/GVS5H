import sys
import heapq


def compute_pref(a):
    """pref[i] (i even) = value of block a[0:i] = sum(top i/2) - sum(bottom i/2).
    a[0:i] is a contiguous even-length block; its optimal score depends only on
    the multiset: give '+' to the largest half and '-' to the smallest half.
    Maintains the smaller half in a max-heap (negated) to get its sum in O(log n).
    """
    n = len(a)
    lo = []          # max-heap (store negatives): the smaller half
    hi = []          # min-heap: the larger half
    sum_lo = 0       # sum of elements currently in lo
    total = 0
    pref = [0] * (n + 1)
    push = heapq.heappush
    pop = heapq.heappop
    for i in range(1, n + 1):
        x = a[i - 1]
        total += x
        if lo and x < -lo[0]:
            push(lo, -x)
            sum_lo += x
        else:
            push(hi, x)
        # invariant: len(lo) - len(hi) in {0,1}
        if len(lo) > len(hi) + 1:
            v = -pop(lo)
            sum_lo -= v
            push(hi, v)
        elif len(hi) > len(lo):
            v = pop(hi)
            push(lo, -v)
            sum_lo += v
        if (i & 1) == 0:
            # even count => len(lo) == i/2 exactly
            pref[i] = total - 2 * sum_lo
    return pref


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    if n % 2 == 0:
        print(compute_pref(a)[n])
    else:
        pref = compute_pref(a)
        prefr = compute_pref(a[::-1])   # prefr[t] = value of the last t elements
        ans = 0
        # unpaired element must be at an odd (1-indexed) position => 0-based even e
        for e in range(0, n, 2):
            v = pref[e] + prefr[n - e - 1]
            if v > ans:
                ans = v
        print(ans)


main()