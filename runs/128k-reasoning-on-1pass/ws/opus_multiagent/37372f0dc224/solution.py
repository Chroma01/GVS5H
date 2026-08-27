import sys

def main():
    data = sys.stdin.buffer.read()
    S = data.strip()
    n = len(S)
    if n == 0:
        sys.stdout.write("\n")
        return

    # P = reverse(S); find longest prefix of P that is a suffix of S
    # (== longest palindromic suffix of S)
    P = S[::-1]

    # KMP prefix function of P
    pi = [0] * n
    k = 0
    Pl = P  # local alias
    pil = pi
    for i, c in enumerate(Pl[1:], 1):
        while k and Pl[k] != c:
            k = pil[k - 1]
        if Pl[k] == c:
            k += 1
        pil[i] = k

    # match S against pattern P
    k = 0
    for c in S:
        while k and Pl[k] != c:
            k = pil[k - 1]
        if Pl[k] == c:
            k += 1
            if k == n:
                break

    L = k  # length of longest palindromic suffix of S
    out = S + S[:n - L][::-1]
    sys.stdout.buffer.write(out + b"\n")

main()