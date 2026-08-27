import sys
import math
import bisect

def main():
    MAX = 10**6
    is_prime = bytearray(b'\x01') * (MAX + 1)
    is_prime[0] = 1
    is_prime[1] = 1
    omega = bytearray(MAX + 1)
    for i in range(2, MAX + 1):
        if is_prime[i]:
            for j in range(i, MAX + 1, i):
                is_prime[j] = 0
                omega[j] += 1
    candidates = [i for i in range(2, MAX + 1) if omega[i] == 2]
    # candidates is already sorted
    data = sys.stdin.read().split()
    if not data:
        return
    q = int(data[0])
    out_lines = []
    for idx in range(1, q + 1):
        A = int(data[idx])
        s = math.isqrt(A)
        # largest m <= s in candidates
        pos = bisect.bisect_right(candidates, s) - 1
        m = candidates[pos]
        out_lines.append(str(m * m))
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()