import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [0] * (N + 1)  # 1-indexed
    for i in range(1, N + 1):
        A[i] = int(next(it))
    
    # left[i] = number of distinct values in A[1..i], for i=1..N-1
    left = [0] * (N + 2)
    seen = [False] * (N + 1)
    distinct = 0
    for i in range(1, N):
        v = A[i]
        if not seen[v]:
            seen[v] = True
            distinct += 1
        left[i] = distinct
    
    # right[k] = number of distinct values in A[k..N], for k=1..N+1
    right = [0] * (N + 3)
    seen = [False] * (N + 1)
    distinct = 0
    for k in range(N, 0, -1):
        v = A[k]
        if not seen[v]:
            seen[v] = True
            distinct += 1
        right[k] = distinct
    right[N + 1] = 0
    
    ans = 0
    freq = [0] * (N + 1)  # frequency of each value in current middle window
    mid_distinct = 0
    
    R = 1  # right end of the middle window (inclusive)
    # Iterate left cut i from 1 to N-2
    for i in range(1, N - 1):
        # Ensure window start is at i+1 and window is non-empty
        if R < i + 1:
            R = i + 1
            v = A[R]
            freq[v] += 1
            if freq[v] == 1:
                mid_distinct += 1
        
        # Current best value for this i
        best_val = left[i] + mid_distinct + right[R + 1]
        
        # Expand R to find a better split point
        while R < N - 1:
            R += 1
            v = A[R]
            freq[v] += 1
            if freq[v] == 1:
                mid_distinct += 1
            new_val = left[i] + mid_distinct + right[R + 1]
            if new_val > best_val:
                best_val = new_val
            else:
                # S(j) = mid_distinct + right[j+1] is unimodal:
                # mid_distinct non-decreasing, right[j+1] non-increasing.
                break
        
        if best_val > ans:
            ans = best_val
        
        # Remove the leftmost element of the middle window for the next i
        v = A[i + 1]
        freq[v] -= 1
        if freq[v] == 0:
            mid_distinct -= 1
    
    print(ans)

if __name__ == "__main__":
    solve()