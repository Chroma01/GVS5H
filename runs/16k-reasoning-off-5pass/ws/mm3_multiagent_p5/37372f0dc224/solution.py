import sys

def z_function(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z

def solve():
    s = sys.stdin.readline().strip()
    n = len(s)
    rev = s[::-1]
    t = rev + "#" + s
    z = z_function(t)
    length = len(t)
    L = 0
    for i in range(n + 1, length):
        if i + z[i] == length and z[i] > L:
            L = z[i]
    ans = s + s[:n - L][::-1]
    print(ans)

solve()