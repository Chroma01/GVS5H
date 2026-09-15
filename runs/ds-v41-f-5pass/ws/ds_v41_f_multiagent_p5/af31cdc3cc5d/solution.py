import sys
import heapq


def even_prefix_values(arr):
    # res[i] = value of arr[0:i] for even i, where value(block) =
    # (sum of its largest half) - (sum of its smallest half).
    # Uses a max-heap `lo` (smaller half) and min-heap `hi` (larger half),
    # kept balanced so that len(lo) == len(hi) at every even index.
    n = len(arr)
    res = [0] * (n + 1)
    lo = []   # max-heap via negation, holds the smaller half
    hi = []   # min-heap, holds the larger half
    sL = 0    # sum of elements in lo
    sH = 0    # sum of elements in hi
    for i in range(1, n + 1):
        x = arr[i - 1]
        heapq.heappush(lo, -x)
        sL += x
        v = -heapq.heappop(lo)
        sL -= v
        heapq.heappush(hi, v)
        sH += v
        if len(hi) > len(lo):
            w = heapq.heappop(hi)
            sH -= w
            heapq.heappush(lo, -w)
            sL += w
        if i % 2 == 0:
            res[i] = sH - sL
    return res


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))

    if n % 2 == 0:
        a.sort()
        m = n // 2
        print(sum(a[m:]) - sum(a[:m]))
        return

    # Odd n: exactly one survivor, which must sit at an odd 1-indexed
    # position p, splitting the array into two independent even blocks.
    pref = even_prefix_values(a)            # pref[p-1] for odd p
    rev = a[::-1]
    suf_rev = even_prefix_values(rev)       # suf_rev[L] = value of last L elements

    ans = 0
    for p in range(1, n + 1, 2):
        left = pref[p - 1]
        length = n - p                       # even, suffix A[p+1..n]
        right = suf_rev[length]
        if left + right > ans:
            ans = left + right
    print(ans)


main()