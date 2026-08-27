import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[0]  # bytes
    n = len(s)
    rev = s[::-1]
    # KMP prefix function over rev + b'#' + s
    # last value = longest prefix of rev matching suffix of s
    #            = longest palindromic suffix of s
    t = rev + b'#' + s
    m = len(t)
    pi = [0] * m
    k = 0
    # start from index 1; t[0] = rev[0], pi[0] = 0
    for i in range(1, m):
        c = t[i]
        while k > 0 and t[k] != c:
            k = pi[k - 1]
        if t[k] == c:
            k += 1
        pi[i] = k
    L = pi[-1]
    out = s + s[:n - L][::-1]
    sys.stdout.buffer.write(out + b'\n')

main()