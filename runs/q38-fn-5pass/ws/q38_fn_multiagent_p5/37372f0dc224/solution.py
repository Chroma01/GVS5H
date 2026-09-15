import sys

def solve():
    s = sys.stdin.buffer.read().strip()
    n = len(s)

    r = s[::-1]
    t = r + b'#' + s
    m = len(t)

    pi = [0] * m
    j = 0

    for i in range(1, m):
        c = t[i]
        while j and c != t[j]:
            j = pi[j - 1]
        if c == t[j]:
            j += 1
        pi[i] = j

    L = pi[-1]

    out = sys.stdout.buffer
    out.write(s)
    out.write(r[L:])
    out.write(b'\n')

if __name__ == "__main__":
    solve()