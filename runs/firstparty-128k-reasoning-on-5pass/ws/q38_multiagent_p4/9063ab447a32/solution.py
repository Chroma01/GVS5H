import sys, math

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data: return
    n, M = data[0], data[1]
    P = [p for p in data[2:] if p <= M]
    if not P:
        print(0); return
    P.sort()
    p0 = P[0]
    hi = p0 * (2 * math.isqrt(M // p0) + 1)
    s = 0
    for p in P:
        s += p
        if s > M:
            if p < hi: hi = p
            break
    groups = []
    i = 0; L = len(P)
    while i < L:
        p = P[i]
        if p > hi: break
        j = i + 1
        while j < L and P[j] == p: j += 1
        groups.append((p, j - i))
        i = j
    def over(x, groups=groups, M=M):
        t = 0
        for p, cnt in groups:
            if p > x: break
            c = (x // p + 1) >> 1
            t += p * c * c * cnt
            if t > M: return True
        return False
    lo = 0
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if over(mid): hi = mid
        else: lo = mid
    x = hi
    y = x - 1
    total = cost = 0
    for p, cnt in groups:
        if p > y: break
        c = (y // p + 1) >> 1
        total += c * cnt
        cost += p * c * c * cnt
    print(total + (M - cost) // x)

if __name__ == "__main__": main()