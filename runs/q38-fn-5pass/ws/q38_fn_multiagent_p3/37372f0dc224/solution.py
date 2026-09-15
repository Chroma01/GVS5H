import sys

def main():
    s = sys.stdin.buffer.readline().strip()
    n = len(s)

    if n == 0:
        sys.stdout.buffer.write(b"\n")
        return

    r = s[::-1]

    # Prefix function for pattern r = reverse(s).
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        c = r[i]
        while j > 0 and c != r[j]:
            j = pi[j - 1]
        if c == r[j]:
            j += 1
        pi[i] = j

    # KMP state after scanning s:
    # longest prefix of r that is a suffix of s.
    j = 0
    for c in s:
        while j > 0 and (j == n or c != r[j]):
            j = pi[j - 1]
        if j < n and c == r[j]:
            j += 1

    longest_pal_suffix = j
    ans = s + s[:n - longest_pal_suffix][::-1]
    sys.stdout.buffer.write(ans + b"\n")

if __name__ == "__main__":
    main()