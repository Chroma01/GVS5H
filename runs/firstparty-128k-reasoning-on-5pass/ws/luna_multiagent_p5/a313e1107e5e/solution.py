import sys
from bisect import bisect_right

def solve():
    input = sys.stdin.buffer.readline

    n, q = map(int, input().split())
    a = list(map(int, input().split()))

    values = sorted(set(a))
    m = len(values)
    rank = {v: i + 1 for i, v in enumerate(values)}

    queries = [[] for _ in range(n + 1)]
    for idx in range(q):
        r, x = map(int, input().split())
        queries[r].append((idx, x))

    bit = [0] * (m + 1)
    answer = [0] * q

    def bit_query(i):
        result = 0
        while i > 0:
            if bit[i] > result:
                result = bit[i]
            i -= i & -i
        return result

    def bit_update(i, value):
        while i <= m:
            if value > bit[i]:
                bit[i] = value
            i += i & -i

    for r in range(1, n + 1):
        pos = rank[a[r - 1]]
        dp = bit_query(pos - 1) + 1
        bit_update(pos, dp)

        for idx, x in queries[r]:
            limit = bisect_right(values, x)
            answer[idx] = bit_query(limit)

    sys.stdout.write("\n".join(map(str, answer)))

if __name__ == "__main__":
    solve()