import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    bit = [0] * (M + 1)
    delta = [0] * M
    ans = 0

    for idx in range(1, N + 1):
        a = int(data[idx + 1])

        # Count previous elements <= a
        s = 0
        j = a + 1
        while j > 0:
            s += bit[j]
            j -= j & -j

        # Previous elements > a form inversions with current element
        ans += idx - 1 - s

        # Insert current value
        j = a + 1
        while j <= M:
            bit[j] += 1
            j += j & -j

        # Contribution of this position if its value wraps
        delta[a] += 2 * idx - 1 - N

    out = []
    for k in range(M):
        out.append(str(ans))
        if k + 1 < M:
            ans += delta[M - 1 - k]

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()