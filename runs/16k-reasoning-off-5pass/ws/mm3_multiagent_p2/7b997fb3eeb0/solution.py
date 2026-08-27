import sys
import threading

def main():
    input = sys.stdin.readline
    N = int(input().strip())
    A = list(map(int, input().split()))
    Q = int(input().strip())
    queries = [tuple(map(int, input().split())) for _ in range(Q)]
    
    # Precompute nxt[i]: smallest j > i such that A[j] >= 2*A[i]
    nxt = [N] * N
    # Use two pointers from right to left to compute nxt efficiently
    j = N - 1
    for i in range(N - 1, -1, -1):
        target = 2 * A[i]
        # Move j to the left until A[j] < target
        while j > i and A[j] >= target:
            j -= 1
        # After loop, A[j] < target (or j == i)
        # The first index with A[idx] >= target is j+1
        if j + 1 < N and A[j + 1] >= target:
            nxt[i] = j + 1
        else:
            nxt[i] = N
        # Actually, we need j > i. If j == i, we need to start from i+1.
        # Let's redo: we want minimal idx > i with A[idx] >= 2*A[i].
        # Standard two-pointer: j starts at N-1, and for each i from N-1 down to 0,
        # we decrease j while A[j] >= 2*A[i]? No, that gives the first index from right.
        # Better: binary search per i is O(N log N) which is fine for N=2e5.
    
    # Let's use binary search to be safe and clear
    nxt = [N] * N
    for i in range(N):
        target = 2 * A[i]
        lo, hi = i + 1, N
        while lo < hi:
            mid = (lo + hi) // 2
            if A[mid] >= target:
                hi = mid
            else:
                lo = mid + 1
        nxt[i] = lo if lo < N else N
    
    # Compute X[i] = nxt[i] - i
    X = [nxt[i] - i for i in range(N)]
    
    # Build Sparse Table for Range Maximum Query on X
    LOG = [0] * (N + 1)
    for i in range(2, N + 1):
        LOG[i] = LOG[i // 2] + 1
    K = LOG[N] + 1
    st = [X[:]]
    for k in range(1, K):
        prev = st[-1]
        size = N - (1 << k) + 1
        if size <= 0:
            break
        curr = [max(prev[i], prev[i + (1 << (k - 1))]) for i in range(size)]
        st.append(curr)
    
    def range_max(l, r):
        # inclusive l, r
        k = LOG[r - l + 1]
        return max(st[k][l], st[k][r - (1 << k) + 1])
    
    # Process queries
    out = []
    for L, R in queries:
        L -= 1
        R -= 1
        length = R - L + 1
        
        lo, hi = 0, length // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # We need to check if max X in [L, L+mid-1] <= length - mid
            if L + mid - 1 > R:
                feasible = False
            else:
                max_x = range_max(L, L + mid - 1)
                feasible = (max_x <= length - mid)
            if feasible:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    threading.Thread(target=main).start()