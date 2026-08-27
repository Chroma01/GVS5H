import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = data[2:2 + N]

    cnt = [0] * M
    sumpos = [0] * M
    bit = [0] * (M + 1)

    inv = 0

    for i, x in enumerate(A):
        # Count previous elements <= x
        s = 0
        j = x + 1
        while j > 0:
            s += bit[j]
            j -= j & -j

        # Previous elements greater than x
        inv += i - s

        # Add current value
        j = x + 1
        while j <= M:
            bit[j] += 1
            j += j & -j

        cnt[x] += 1
        sumpos[x] += i + 1  # 1-based position

    ans = inv
    n1 = N + 1
    out = []

    for k in range(M):
        out.append(str(ans))
        if k != M - 1:
            v = M - 1 - k
            ans += 2 * sumpos[v] - n1 * cnt[v]

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()