import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    last = [0] * (n + 2)

    sum_last = 0
    sum_adj = 0
    ans = 0

    for r in range(1, n + 1):
        v = data[r]
        old = last[v]

        sum_last += r - old

        if v > 1:
            u = last[v - 1]
            sum_adj -= u if u < old else old
        if v < n:
            u = last[v + 1]
            sum_adj -= u if u < old else old

        last[v] = r

        if v > 1:
            sum_adj += last[v - 1]
        if v < n:
            sum_adj += last[v + 1]

        ans += sum_last - sum_adj

    print(ans)

if __name__ == "__main__":
    solve()