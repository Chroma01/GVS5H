import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    M = data[1]
    A = data[2:2 + N]

    bit = [0] * (M + 1)
    S = [0] * M
    inv = 0
    m = M

    for i, x in enumerate(A):
        S[x] += 2 * i - N + 1

        idx = x + 1

        s = 0
        j = idx
        while j:
            s += bit[j]
            j -= j & -j

        inv += i - s

        j = idx
        while j <= m:
            bit[j] += 1
            j += j & -j

    ans = inv
    out = [str(ans)]

    for r in range(M - 1, 0, -1):
        ans += S[r]
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()