import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    s = data[0]
    n = len(s)
    r = s[::-1]

    # Prefix function for the pattern r = reverse(s)
    pi = [0] * n
    j = 0
    for i in range(1, n):
        c = r[i]
        while j and r[j] != c:
            j = pi[j - 1]
        if r[j] == c:
            j += 1
        pi[i] = j

    # KMP scan of s with pattern r.
    # Final q is the longest prefix of r that is a suffix of s,
    # i.e. the length of the longest palindromic suffix of s.
    q = 0
    for c in s:
        while q and (q == n or r[q] != c):
            q = pi[q - 1]
        if q < n and r[q] == c:
            q += 1

    # Append reverse(s[:n-q]), which is r[q:].
    sys.stdout.buffer.write(s + r[q:] + b"\n")


if __name__ == "__main__":
    main()