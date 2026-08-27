import sys
import bisect

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    Q = int(data[0])
    A_list = list(map(int, data[1:]))

    MAX_M = 10 ** 6  # because (10^6)^2 = 10^12

    # ---------- 1. linear sieve: count distinct prime factors ----------
    cnt = [0] * (MAX_M + 1)  # cnt[x] = ω(x)
    primes = []

    for i in range(2, MAX_M + 1):
        if cnt[i] == 0:  # i is prime
            cnt[i] = 1
            primes.append(i)

        for p in primes:
            ip = i * p
            if ip > MAX_M:
                break
            if i % p == 0:
                cnt[ip] = cnt[i]
                break
            else:
                cnt[ip] = cnt[i] + 1

    # ---------- 2. build list of all 400 numbers ----------
    ans = []
    for m in range(2, MAX_M + 1):
        if cnt[m] == 2:  # exactly two distinct primes
            ans.append(m * m)  # N = m²

    # ---------- 3. answer the queries ----------
    out_lines = []
    for A in A_list:
        idx = bisect.bisect_right(ans, A) - 1
        out_lines.append(str(ans[idx]))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()