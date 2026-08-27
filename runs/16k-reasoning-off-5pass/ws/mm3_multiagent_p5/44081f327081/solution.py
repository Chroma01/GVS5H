import sys
import math

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    MAXV = 10**6
    # frequency of each value
    cnt = [0] * (MAXV + 1)
    for x in A:
        cnt[x] += 1
    
    # freq[d] = number of elements in A divisible by d
    freq = [0] * (MAXV + 1)
    # standard divisor sum / multiple counting
    for d in range(1, MAXV + 1):
        # add cnt[m] to freq[d] for all multiples m of d
        # using step loop, total operations ~ MAXV * (1/1 + 1/2 + ...) ~ MAXV log MAXV
        for m in range(d, MAXV + 1, d):
            freq[d] += cnt[m]
    
    out_lines = []
    for x in A:
        # find largest divisor d of x with freq[d] >= K
        ans = 1  # at worst, divisor 1 always works
        # enumerate divisors
        # collect divisors in a list, then sort descending (or just scan from large to small)
        divs = []
        r = int(math.isqrt(x))
        for d in range(1, r + 1):
            if x % d == 0:
                divs.append(d)
                if d != x // d:
                    divs.append(x // d)
        # sort descending
        divs.sort(reverse=True)
        for d in divs:
            if freq[d] >= K:
                ans = d
                break
        out_lines.append(str(ans))
    
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()