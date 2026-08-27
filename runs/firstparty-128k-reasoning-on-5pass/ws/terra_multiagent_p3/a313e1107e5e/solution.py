import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.buffer.readline

    N, Q = map(int, input().split())
    A = list(map(int, input().split()))

    queries = []
    for i in range(Q):
        r, x = map(int, input().split())
        queries.append((r, x, i))
    queries.sort()

    values = sorted(set(A))
    m = len(values)

    bit = [0] * (m + 1)

    def update(i, value):
        while i <= m:
            if value > bit[i]:
                bit[i] = value
            i += i & -i

    def query(i):
        result = 0
        while i > 0:
            if bit[i] > result:
                result = bit[i]
            i -= i & -i
        return result

    answers = [0] * Q
    pos = 0

    for r, x, qi in queries:
        while pos < r:
            a = A[pos]
            idx = bisect_right(values, a)
            dp = query(idx - 1) + 1
            update(idx, dp)
            pos += 1

        limit = bisect_right(values, x)
        answers[qi] = query(limit)

    print("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()