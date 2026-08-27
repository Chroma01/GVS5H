import sys
from bisect import bisect_left, bisect_right

def possible(x, y, m):
    k = len(y)

    if abs(x[0] - y[0]) > m:
        return False

    left = 0
    right = 0

    for i in range(1, len(x)):
        lo = bisect_left(y, x[i] - m)
        hi = bisect_right(y, x[i] + m) - 1

        if lo > hi:
            return False

        new_right = right
        if right + 1 < k and y[right + 1] - y[right] <= x[i] - x[i - 1]:
            new_right += 1

        left = max(left, lo)
        right = min(new_right, hi)

        if left > right:
            return False

    return right == k - 1

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    ptr = 1
    ans = []

    for _ in range(t):
        n = int(data[ptr])
        a = data[ptr + 1]
        b = data[ptr + 2]
        ptr += 3

        x = [i for i, ch in enumerate(a) if ch == 49]
        y = [i for i, ch in enumerate(b) if ch == 49]

        if len(x) < len(y):
            ans.append("-1")
            continue

        low = -1
        high = n

        while high - low > 1:
            mid = (low + high) // 2
            if possible(x, y, mid):
                high = mid
            else:
                low = mid

        ans.append(str(high))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    main()