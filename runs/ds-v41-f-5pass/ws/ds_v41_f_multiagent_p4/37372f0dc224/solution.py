import sys

def main():
    data = sys.stdin.buffer.read().split()
    s = data[0]
    n = len(s)
    rev = s[::-1]
    # combined = reverse(S) + sentinel + S
    combined = rev + b'#' + s
    m = len(combined)
    pi = [0] * m
    j = 0
    for i in range(1, m):
        c = combined[i]
        while j > 0 and c != combined[j]:
            j = pi[j - 1]
        if c == combined[j]:
            j += 1
        pi[i] = j
    k = pi[m - 1]                 # longest palindromic suffix length of S
    out = s + rev[k:]             # rev[k:] == reverse(S[:n-k])
    sys.stdout.buffer.write(out + b'\n')

main()