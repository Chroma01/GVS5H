import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[0]
    n = len(s)
    rev = s[::-1]
    a = rev + b'#' + s
    m = len(a)
    pi = [0] * m
    k = 0
    for i in range(1, m):
        c = a[i]
        while k and a[k] != c:
            k = pi[k - 1]
        if a[k] == c:
            k += 1
        pi[i] = k
    q = pi[-1]  # length of longest palindromic suffix of s
    out = s + s[:n - q][::-1]
    sys.stdout.buffer.write(out + b'\n')

main()