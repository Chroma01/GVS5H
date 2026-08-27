import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)
    if n == 0:
        return

    r = s[::-1]

    # Prefix function for the pattern r.
    pi = [0] * n
    j = 0
    for i in range(1, n):
        c = r[i]
        while j > 0 and c != r[j]:
            j = pi[j - 1]
        if c == r[j]:
            j += 1
        pi[i] = j

    # KMP scan of s against pattern r.
    # q is the longest prefix of r that is a suffix of the scanned part of s.
    # Do not reset q when q == n; a full match can only occur at the end.
    q = 0
    for c in s:
        while q > 0 and c != r[q]:
            q = pi[q - 1]
        if c == r[q]:
            q += 1

    l = q
    ans = s + s[:n - l][::-1]
    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()