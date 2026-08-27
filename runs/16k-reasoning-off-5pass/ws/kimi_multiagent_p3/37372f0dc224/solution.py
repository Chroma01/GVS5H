import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[0].decode()
    n = len(s)
    t = s + '#' + s[::-1]
    m = len(t)
    pi = [0] * m
    k = 0
    # KMP prefix function; pi[-1] = length of longest prefix of s
    # that is also a suffix of reverse(s), i.e. longest palindromic prefix.
    for i in range(1, m):
        c = t[i]
        while k > 0 and t[k] != c:
            k = pi[k - 1]
        if t[k] == c:
            k += 1
        pi[i] = k
    L = pi[-1]
    sys.stdout.write(s + s[:n - L][::-1])

solve()