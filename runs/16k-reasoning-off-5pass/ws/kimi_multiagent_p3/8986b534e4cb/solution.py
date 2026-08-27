import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0
    N, M, Q = data[pos], data[pos+1], data[pos+2]; pos += 3
    L = [0]*(M+1); R = [0]*(M+1); sg = [0]*(M+1)
    for i in range(1, M+1):
        S, T = data[pos], data[pos+1]; pos += 2
        if S < T:
            L[i], R[i], sg[i] = S, T, 1
        else:
            L[i], R[i], sg[i] = T, S, -1

    INF = N + 5
    size = 1
    while size < N + 2:
        size <<= 1
    # seg1: over left endpoints, min right endpoint among active + intervals
    seg1 = [INF]*(2*size)
    # seg2: over right endpoints, max left endpoint among active + intervals
    seg2 = [-INF]*(2*size)
    # seg3: over left endpoints, max right endpoint among active - intervals
    seg3 = [-INF]*(2*size)
    # seg4: over right endpoints, min left endpoint among active - intervals
    seg4 = [INF]*(2*size)

    cntL = [0]*(N+2)   # active intervals with left endpoint x
    cntR = [0]*(N+2)   # active intervals with right endpoint x
    minR = [INF]*(N+2)
    maxL = [-INF]*(N+2)
    maxR = [-INF]*(N+2)
    minL = [INF]*(N+2)

    def upd_min(seg, idx, val):
        i = idx + size; seg[i] = val; i >>= 1
        while i:
            a = seg[2*i]; b = seg[2*i+1]
            seg[i] = a if a < b else b
            i >>= 1

    def upd_max(seg, idx, val):
        i = idx + size; seg[i] = val; i >>= 1
        while i:
            a = seg[2*i]; b = seg[2*i+1]
            seg[i] = a if a > b else b
            i >>= 1

    def qmin(seg, l, r):  # inclusive [l, r]
        l += size; r += size
        res = INF
        while l <= r:
            if l & 1:
                if seg[l] < res: res = seg[l]
                l += 1
            if not (r & 1):
                if seg[r] < res: res = seg[r]
                r -= 1
            l >>= 1; r >>= 1
        return res

    def qmax(seg, l, r):
        l += size; r += size
        res = -INF
        while l <= r:
            if l & 1:
                if seg[l] > res: res = seg[l]
                l += 1
            if not (r & 1):
                if seg[r] > res: res = seg[r]
                r -= 1
            l >>= 1; r >>= 1
        return res

    def conflict(a, b, s):
        # (1) shared endpoint: active interval with left endpoint a
        #     (extends right, nested with [a,b]) or right endpoint b
        #     (extends left, nested). Touching ([c,a] or [b,d]) is fine.
        if cntL[a] > 0 or cntR[b] > 0:
            return True
        # (2) same-sign crossing: existing [c,d] same sign with
        #     a < c < b < d  or  c < a < d < b.
        if s == 1:
            if qmin(seg1, a+1, b-1) < b: return True
            if qmax(seg2, a+1, b-1) > a: return True
        else:
            if qmax(seg3, a+1, b-1) > b: return True
            if qmin(seg4, a+1, b-1) < a: return True
        return False

    def add(i):
        a, b, s = L[i], R[i], sg[i]
        cntL[a] += 1; cntR[b] += 1
        if s == 1:
            if b < minR[a]:
                minR[a] = b; upd_min(seg1, a, b)
            if a > maxL[b]:
                maxL[b] = a; upd_max(seg2, b, a)
        else:
            if b > maxR[a]:
                maxR[a] = b; upd_max(seg3, a, b)
            if a < minL[b]:
                minL[b] = a; upd_min(seg4, b, a)

    def remove(i):
        a, b, s = L[i], R[i], sg[i]
        cntL[a] -= 1; cntR[b] -= 1
        if s == 1:
            if minR[a] == b:
                minR[a] = INF; upd_min(seg1, a, INF)
            if maxL[b] == a:
                maxL[b] = -INF; upd_max(seg2, b, -INF)
        else:
            if maxR[a] == b:
                maxR[a] = -INF; upd_max(seg3, a, -INF)
            if minL[b] == a:
                minL[b] = INF; upd_min(seg4, b, INF)

    f = [0]*(M+2)
    r = 0
    for l in range(1, M+1):
        while r + 1 <= M and not conflict(L[r+1], R[r+1], sg[r+1]):
            r += 1
            add(r)
        f[l] = r
        if r >= l:
            remove(l)
        else:
            r = l  # safety; a single interval never self-conflicts

    out = []
    for k in range(Q):
        Lk, Rk = data[pos], data[pos+1]; pos += 2
        out.append("Yes" if Rk <= f[Lk] else "No")
    sys.stdout.write("\n".join(out) + "\n")

main()