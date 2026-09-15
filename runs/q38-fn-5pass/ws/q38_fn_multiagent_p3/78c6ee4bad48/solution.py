import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if len(data) < 2:
        return

    n = data[0]
    first = data[1]
    prev = first

    even = []
    odd = []

    for i in range(n - 1):
        cur = data[2 + i]
        gap = cur - prev
        if i & 1:
            odd.append(gap)
        else:
            even.append(gap)
        prev = cur

    even.sort()
    odd.sort()

    ans = n * first

    for t, gap in enumerate(even):
        ans += gap * (n - 1 - 2 * t)

    for t, gap in enumerate(odd):
        ans += gap * (n - 2 - 2 * t)

    print(ans)

if __name__ == "__main__":
    solve()