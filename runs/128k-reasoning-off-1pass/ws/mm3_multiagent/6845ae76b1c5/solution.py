import sys
sys.setrecursionlimit(1 << 25)

class WaveletTree:
    def __init__(self, data, lo, hi):
        self.lo = lo
        self.hi = hi
        if lo == hi or not data:
            self.b = [0]
            self.s = [0]
            self.left = None
            self.right = None
            return
        mid = (lo + hi) // 2
        self.b = [0]
        self.s = [0]
        left_data = []
        right_data = []
        for x in data:
            if x <= mid:
                left_data.append(x)
            else:
                right_data.append(x)
            self.b.append(self.b[-1] + (1 if x <= mid else 0))
            self.s.append(self.s[-1] + (x if x <= mid else 0))
        self.left = WaveletTree(left_data, lo, mid)
        self.right = WaveletTree(right_data, mid+1, hi)

    def query(self, X, L, R):
        if X == 0 or L > self.hi or R < self.lo:
            return 0, 0
        if L <= self.lo and self.hi <= R:
            return self.b[X], self.s[X]
        mid = (self.lo + self.hi) // 2
        left_count, left_sum = 0, 0
        right_count, right_sum = 0, 0
        if L <= mid:
            lX = self.b[X]
            left_count, left_sum = self.left.query(lX, L, R)
        if R > mid:
            rX = X - self.b[X]
            right_count, right_sum = self.right.query(rX, L, R)
        return left_count + right_count, left_sum + right_sum

def solve(X, Y, L, R, wtA, wtB, sumA, sumB):
    if L == R or X == 0 or Y == 0:
        return 0
    mid = (L + R) // 2
    cA_L, sA_L = wtA.query(X, L, mid)
    cA_R = X - cA_L
    sA_R = sumA[X] - sA_L
    cB_L, sB_L = wtB.query(Y, L, mid)
    cB_R = Y - cB_L
    sB_R = sumB[Y] - sB_L
    cross = cA_L * sB_R - cB_R * sA_L + cA_R * sB_L - cB_L * sA_R
    left = solve(X, Y, L, mid, wtA, wtB, sumA, sumB)
    right = solve(X, Y, mid+1, R, wtA, wtB, sumA, sumB)
    return cross + left + right

def main():
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    queries = []
    for _ in range(K):
        x, y = map(int, input().split())
        queries.append((x, y))
    
    all_vals = sorted(set(A + B))
    val_to_idx = {v: i for i, v in enumerate(all_vals)}
    M = len(all_vals)
    A_comp = [val_to_idx[v] for v in A]
    B_comp = [val_to_idx[v] for v in B]
    
    sumA = [0] * (N + 1)
    sumB = [0] * (N + 1)
    for i in range(N):
        sumA[i+1] = sumA[i] + A[i]
        sumB[i+1] = sumB[i] + B[i]
    
    wtA = WaveletTree(A_comp, 0, M-1)
    wtB = WaveletTree(B_comp, 0, M-1)
    
    out = []
    for X, Y in queries:
        s = solve(X, Y, 0, M-1, wtA, wtB, sumA, sumB)
        total = Y * sumA[X] + X * sumB[Y] - 2 * s
        out.append(total)
    
    sys.stdout.write('\n'.join(map(str, out)) + '\n')

if __name__ == "__main__":
    main()