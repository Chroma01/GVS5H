import sys, math

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])

    # integer cube root of N
    D = int(round(N ** (1.0 / 3.0)))
    while D ** 3 > N:
        D -= 1
    while (D + 1) ** 3 <= N:
        D += 1

    for d in range(1, D + 1):
        if N % d:
            continue
        M = N // d
        Delta = 12 * M - 3 * d * d
        if Delta < 0:
            continue
        s = math.isqrt(Delta)
        if s * s != Delta:
            continue
        num = s - 3 * d
        if num > 0 and num % 6 == 0:
            y = num // 6
            x = y + d
            sys.stdout.write(f"{x} {y}\n")
            return
    sys.stdout.write("-1\n")

main()