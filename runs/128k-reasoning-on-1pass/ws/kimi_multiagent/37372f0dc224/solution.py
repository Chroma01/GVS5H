import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    s = data[0]
    n = len(s)
    r = s[::-1]

    # KMP failure function for pattern r = reverse(s)
    lps = [0] * n
    k = 0
    for i in range(1, n):
        c = r[i]
        while k and r[k] != c:
            k = lps[k - 1]
        if r[k] == c:
            k += 1
        lps[i] = k

    # Stream s through the KMP automaton for pattern r.
    # Final q = longest prefix of r that is a suffix of s
    #         = longest palindromic suffix of s.
    q = 0
    for c in s:
        while q and (q == n or r[q] != c):
            q = lps[q - 1]
        if q < n and r[q] == c:
            q += 1

    ans = s + s[:n - q][::-1]
    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()