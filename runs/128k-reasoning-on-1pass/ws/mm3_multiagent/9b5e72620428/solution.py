import sys
from collections import Counter

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    B = [int(next(it)) for _ in range(N)]

    fa = []   # fixed A values
    fb = []   # fixed B values
    cntBoth = 0
    cntNone = 0
    C0 = None

    for a, b in zip(A, B):
        if a != -1 and b != -1:
            cntBoth += 1
            fa.append(a)
            fb.append(b)
            s = a + b
            if C0 is None:
                C0 = s
            elif C0 != s:
                print("No")
                return
        elif a != -1:
            fa.append(a)
        elif b != -1:
            fb.append(b)
        else:
            cntNone += 1

    # No position with both numbers fixed -> always possible
    if cntBoth == 0:
        print("Yes")
        return

    # C0 is defined now
    maxA = max(fa) if fa else 0
    maxB = max(fb) if fb else 0
    if C0 < maxA or C0 < maxB:
        print("No")
        return

    need = cntBoth - cntNone
    if need < 0:
        need = 0
    if need == 0:
        print("Yes")
        return

    cntA = Counter(fa)
    cntB = Counter(fb)

    pairs = 0
    for v, ca in cntA.items():
        w = C0 - v
        if w in cntB:
            pairs += min(ca, cntB[w])
            if pairs >= need:
                print("Yes")
                return

    print("No")

if __name__ == "__main__":
    solve()