import sys


def solve_case(n, a, b):
    p = [i for i, c in enumerate(a) if c == '1']
    q = [i for i, c in enumerate(b) if c == '1']
    np = len(p)
    nq = len(q)

    if np < nq:
        return -1

    def feasible(k):
        left = [0] * nq
        right = [0] * nq

        lo = 0
        hi = 0
        for j, x in enumerate(q):
            low_value = x - k
            while lo < np and p[lo] < low_value:
                lo += 1
            left[j] = lo

            high_value = x + k
            if hi < lo:
                hi = lo
            while hi + 1 < np and p[hi + 1] <= high_value:
                hi += 1
            while hi < np and p[hi] <= high_value:
                hi += 1
            right[j] = hi - 1

            if left[j] > right[j]:
                return False

        # The first group must contain the first initial piece.
        if left[0] > 0 or right[0] < 0:
            return False

        # prev is the number of initial pieces assigned to groups already fixed.
        prev = 0

        for j in range(nq - 1):
            # Boundary r means pieces [0, r-1] are assigned through q[j],
            # and pieces [r, ...] are assigned from q[j+1] onward.
            lower = max(prev + 1, left[j + 1])
            upper = right[j] + 1

            r = lower
            need_gap = q[j + 1] - q[j]

            while r <= upper and p[r] - p[r - 1] < need_gap:
                r += 1

            if r > upper:
                return False
            prev = r

        # Check the final group.
        if prev >= np:
            return False
        if prev < left[-1] or np - 1 > right[-1]:
            return False

        return True

    low, high = -1, n
    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            high = mid
        else:
            low = mid

    return high


def main():
    input = sys.stdin.buffer.readline
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        a = input().decode().strip()
        b = input().decode().strip()
        ans.append(str(solve_case(n, a, b)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()