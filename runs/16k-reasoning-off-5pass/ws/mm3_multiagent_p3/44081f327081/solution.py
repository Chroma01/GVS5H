import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    maxA = max(A) if A else 0
    freq = [0] * (maxA + 1)
    for v in A:
        freq[v] += 1

    # cnt[d] = number of array elements divisible by d
    cnt = [0] * (maxA + 1)
    for d in range(1, maxA + 1):
        f = freq[d]
        if f == 0:
            continue
        for m in range(d, maxA + 1, d):
            cnt[m] += f

    out_lines = []
    for val in A:
        best = 1
        d = 1
        while d * d <= val:
            if val % d == 0:
                if cnt[d] >= K and d > best:
                    best = d
                other = val // d
                if other != d and cnt[other] >= K and other > best:
                    best = other
            d += 1
        out_lines.append(str(best))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()