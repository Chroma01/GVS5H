import sys

MOD = 998244353

def solve(S):
    n = len(S)
    d = 0
    dp = {0: 1}
    for i, ch in enumerate(S, start=1):
        if ch == 'W':
            d += 1
            ndp = {}
            for v, val in dp.items():
                ndp[v] = (ndp.get(v, 0) + val) % MOD
                if v >= 1:
                    ndp[v - 1] = (ndp.get(v - 1, 0) + val * v) % MOD
            dp = ndp
        else:
            d -= 1
            ndp = {}
            for v, val in dp.items():
                u = v + d + 1
                if u > 0:
                    ndp[v] = (ndp.get(v, 0) + val * u) % MOD
                ndp[v + 1] = (ndp.get(v + 1, 0) + val) % MOD
            dp = ndp
        if i < n and d >= 0:
            dp = {v: val for v, val in dp.items() if v >= 1}
        if not dp:
            break
    return dp.get(0, 0) % MOD

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()
    print(solve(S))

if __name__ == '__main__':
    main()