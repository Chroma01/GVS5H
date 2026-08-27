import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    if not s:
        return

    n = len(s)
    r = s[::-1]

    # Prefix function for pattern r.
    pi = [0] * n
    j = 0
    for i in range(1, n):
        c = r[i]
        while j and r[j] != c:
            j = pi[j - 1]
        if r[j] == c:
            j += 1
        pi[i] = j

    # KMP scan of s to find the longest prefix of r that is a suffix of s.
    q = 0
    for c in s:
        while q and r[q] != c:
            q = pi[q - 1]
        if r[q] == c:
            q += 1

    k = n - q
    sys.stdout.buffer.write(s + s[:k][::-1] + b"\n")

if __name__ == "__main__":
    main()