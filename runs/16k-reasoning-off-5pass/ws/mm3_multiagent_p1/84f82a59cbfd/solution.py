import sys
import bisect

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    Q = int(data[0])
    A_list = [int(x) for x in data[1:1+Q]]
    
    # max A is 1e12, sqrt is 1e6
    MAX = 10**6 + 5
    omega = [0] * (MAX + 1)
    # sieve: for each prime p, add 1 to all multiples of p
    # to count distinct prime factors
    for i in range(2, MAX + 1):
        if omega[i] == 0:  # i is prime
            for j in range(i, MAX + 1, i):
                omega[j] += 1
    
    # collect numbers with exactly 2 distinct prime factors
    good = [i for i in range(2, MAX + 1) if omega[i] == 2]
    
    out_lines = []
    for A in A_list:
        # find largest m <= sqrt(A)
        s = int(A**0.5)
        # correct for floating point errors
        while (s+1)**2 <= A:
            s += 1
        while s*s > A:
            s -= 1
        # binary search in good for the largest element <= s
        idx = bisect.bisect_right(good, s) - 1
        m = good[idx]
        out_lines.append(str(m * m))
    
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()