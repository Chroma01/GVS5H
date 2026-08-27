import sys


def minimum_operations(n, a_str, b_str):
    a = [i for i, c in enumerate(a_str) if c == 49]  # bytes: b'1'
    b = [i for i, c in enumerate(b_str) if c == 49]

    m = len(a)
    q = len(b)

    if q > m:
        return -1

    def feasible(k):
        # For every target b[t], source positions that may map to it form
        # the index interval [left[t], right[t]].
        left = [0] * q
        right = [0] * q

        l = 0
        r = 0
        for t, y in enumerate(b):
            lo = y - k
            hi = y + k

            while l < m and a[l] < lo:
                l += 1
            if r < l:
                r = l
            while r < m and a[r] <= hi:
                r += 1

            left[t] = l
            right[t] = r - 1

            if left[t] > right[t]:
                return False

        # The first source must belong to the first target group.
        if left[0] != 0:
            return False

        # s is the first source index of the current target group.
        s = 0

        for t in range(1, q):
            # Choose the earliest possible boundary s between targets t-1,t.
            # It must leave at least one source in the preceding group,
            # start inside the valid interval for target t, and be at a
            # sufficiently large source gap to realize the target gap.
            candidate = max(s + 1, left[t])
            required_gap = b[t] - b[t - 1]

            while candidate < m and a[candidate] - a[candidate - 1] < required_gap:
                candidate += 1

            # Previous group ends at candidate - 1.
            if candidate >= m:
                return False
            if candidate > right[t - 1] + 1:
                return False
            if candidate > right[t]:
                return False

            s = candidate

        # All remaining sources must be assigned to the final target.
        return s >= left[-1] and m - 1 <= right[-1]

    if not feasible(n):
        return -1

    lo = -1
    hi = n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid

    return hi


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    t = int(data[0])
    p = 1
    ans = []

    for _ in range(t):
        n = int(data[p])
        a = data[p + 1]
        b = data[p + 2]
        p += 3
        ans.append(str(minimum_operations(n, a, b)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    solve()