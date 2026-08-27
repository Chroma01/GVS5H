```python
import sys
import heapq

def prefix_half_diff(arr):
    n = len(arr)
    res = [0] * (n + 1)
    lo = []  # max-heap via negatives, smaller half
    hi = []  # min-heap, larger half
    sum_lo = 0
    sum_hi = 0

    for i, x in enumerate(arr, 1):
        heapq.heappush(lo, -x)
        sum_lo += x
        y = -heapq.heappop(lo)
        sum_lo -= y
        heapq.heappush(hi, y)
        sum_hi += y

        if len(lo) < len(hi):
            y = heapq.heappop(hi)
            sum_hi -= y
            heapq.heappush(lo, -y)
            sum_lo += y

        if i % 2 == 0:
            res[i] = sum_hi - sum_lo
    return res

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:]

    pref = prefix_half_diff(a)

    if n % 2 == 0:
        print(pref[n])
        return

    rev = prefix_half_diff(a[::-1])
    suff = [0] * (n + 2)
    for i in range(1, n + 1):
        length = n - i + 1
        if length % 2 == 0:
            suff[i] = rev[length]

    ans = 0
    for s in range(1, n + 1, 2):  # only odd positions can remain
        ans = max(ans, pref[s - 1] + suff[s + 1])
    print(ans)

if __name__ == "__main__":
    main()
```