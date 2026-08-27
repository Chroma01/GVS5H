import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)
    if n == 0:
        return

    r = s[::-1]

    # Prefix function for the pattern r only.
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        c = r[i]
        while j > 0 and c != r[j]:
            j = pi[j - 1]
        if c == r[j]:
            j += 1
        pi[i] = j

    # KMP scan of s with pattern r.
    # q is the length of the longest prefix of r that is a suffix of s.
    q = 0
    for c in s:
        while q > 0 and r[q] != c:
            q = pi[q - 1]
        if r[q] == c:
            q += 1
            if q == n:
                break

    k = n - q
    sys.stdout.buffer.write(s + s[:k][::-1] + b"\n")

if __name__ == "__main__":
    main()