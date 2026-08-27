import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)
    if n == 0:
        return

    p = s[::-1]

    # Prefix function for p.
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        c = p[i]
        while j > 0 and c != p[j]:
            j = pi[j - 1]
        if c == p[j]:
            j += 1
        pi[i] = j

    # KMP scan of s with pattern p.
    # q is the longest prefix of p that is a suffix of the part of s scanned so far.
    # Do not reset after a full match at the end, because s itself may be a palindrome.
    q = 0
    for c in s:
        while q > 0 and (q == n or p[q] != c):
            q = pi[q - 1]
        if q < n and p[q] == c:
            q += 1

    ans = s + s[:n - q][::-1]
    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()