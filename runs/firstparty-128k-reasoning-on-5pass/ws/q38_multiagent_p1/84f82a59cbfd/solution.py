import sys
import math
import bisect

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    q = int(data[0])
    queries = [int(x) for x in data[1:1 + q]]
    if not queries:
        return

    isqrt = math.isqrt
    max_root = max(isqrt(a) for a in queries)

    # cnt[x] = number of distinct prime factors of x
    cnt = bytearray(max_root + 1)
    for i in range(2, max_root + 1):
        if cnt[i] == 0:  # i is prime
            for j in range(i, max_root + 1, i):
                cnt[j] += 1

    valid = [i for i in range(2, max_root + 1) if cnt[i] == 2]

    bisect_right = bisect.bisect_right
    out = []
    for a in queries:
        r = isqrt(a)
        idx = bisect_right(valid, r) - 1
        m = valid[idx]
        out.append(str(m * m))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()