import sys
import bisect

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    Q = int(data[0])
    queries = [int(x) for x in data[1:1+Q]]

    # Precompute smallest prime factor up to 10^6
    MAX_R = 10**6
    spf = list(range(MAX_R + 1))
    for i in range(2, int(MAX_R**0.5) + 1):
        if spf[i] == i:  # i is prime
            for j in range(i*i, MAX_R + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # Enumerate all R with exactly two distinct prime factors
    four_hundred_numbers = []
    for r in range(2, MAX_R + 1):
        # Count distinct prime factors
        x = r
        first = spf[x]
        count = 1
        x //= first
        while x > 1:
            p = spf[x]
            if p != first:
                count += 1
                if count > 2:
                    break
                first = p
            x //= p
        if count == 2:
            four_hundred_numbers.append(r * r)

    four_hundred_numbers.sort()

    out_lines = []
    for a in queries:
        idx = bisect.bisect_right(four_hundred_numbers, a) - 1
        out_lines.append(str(four_hundred_numbers[idx]))

    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    solve()