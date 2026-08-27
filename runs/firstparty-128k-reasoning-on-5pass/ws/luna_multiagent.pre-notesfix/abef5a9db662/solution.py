import sys
from array import array

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    contests = [(next(it), next(it)) for _ in range(n)]
    q = next(it)
    queries = [next(it) for _ in range(q)]

    M = 500_000
    size = 1
    while size < M:
        size <<= 1

    INF = 10**9
    mn = array('i', [INF]) * (2 * size)
    mx = array('i', [-INF]) * (2 * size)
    lazy = array('i', [0]) * (2 * size)

    for i in range(M):
        value = i + 1
        mn[size + i] = value
        mx[size + i] = value

    for k in range(size - 1, 0, -1):
        mn[k] = min(mn[k << 1], mn[k << 1 | 1])
        mx[k] = max(mx[k << 1], mx[k << 1 | 1])

    sys.setrecursionlimit(1_000_000)

    def push(k):
        value = lazy[k]
        if value:
            left = k << 1
            right = left | 1
            mn[left] += value
            mx[left] += value
            lazy[left] += value
            mn[right] += value
            mx[right] += value
            lazy[right] += value
            lazy[k] = 0

    def first_ge(k, left, right, target):
        if mx[k] < target:
            return -1
        if right - left == 1:
            return left
        push(k)
        mid = (left + right) >> 1
        result = first_ge(k << 1, left, mid, target)
        if result != -1:
            return result
        return first_ge(k << 1 | 1, mid, right, target)

    def last_le(k, left, right, target):
        if mn[k] > target:
            return -1
        if right - left == 1:
            return left
        push(k)
        mid = (left + right) >> 1
        result = last_le(k << 1 | 1, mid, right, target)
        if result != -1:
            return result
        return last_le(k << 1, left, mid, target)

    def range_add(k, left, right, ql, qr):
        if qr <= left or right <= ql:
            return
        if ql <= left and right <= qr:
            mn[k] += 1
            mx[k] += 1
            lazy[k] += 1
            return

        push(k)
        mid = (left + right) >> 1
        range_add(k << 1, left, mid, ql, qr)
        range_add(k << 1 | 1, mid, right, ql, qr)
        mn[k] = min(mn[k << 1], mn[k << 1 | 1])
        mx[k] = max(mx[k << 1], mx[k << 1 | 1])

    for L, R in contests:
        first = first_ge(1, 0, size, L)
        last = last_le(1, 0, size, R)
        if first != -1 and last != -1 and first <= last:
            range_add(1, 0, size, first, last + 1)

    def get_value(index):
        k = 1
        left = 0
        right = size
        while right - left > 1:
            push(k)
            mid = (left + right) >> 1
            if index < mid:
                k = k << 1
                right = mid
            else:
                k = k << 1 | 1
                left = mid
        return mn[k]

    answers = [str(get_value(x - 1)) for x in queries]
    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    solve()