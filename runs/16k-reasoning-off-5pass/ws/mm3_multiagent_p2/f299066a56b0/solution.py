import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    l, r = 0, n - 1
    ans = 0
    while l < r:
        if a[l] * 2 <= a[r]:
            ans += 1
            l += 1
            r -= 1
        else:
            r -= 1
    print(ans)

solve()