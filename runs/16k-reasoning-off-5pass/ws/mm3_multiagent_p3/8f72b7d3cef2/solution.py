import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # inc[i]: length of longest strictly increasing subarray ending at i
    inc = [0] * N
    for i in range(N):
        if i == 0:
            inc[i] = 1
        else:
            if A[i-1] < A[i]:
                inc[i] = inc[i-1] + 1
            else:
                inc[i] = 1
    
    # right[i]: length of longest strictly increasing subarray starting at i
    right = [0] * N
    for i in range(N-1, -1, -1):
        if i == N-1:
            right[i] = 1
        else:
            if A[i] < A[i+1]:
                right[i] = right[i+1] + 1
            else:
                right[i] = 1
    
    # prefix sums
    prefix = [0] * (N+1)
    for i in range(N):
        prefix[i+1] = prefix[i] + A[i]
    
    res = [0] * N
    for k in range(N):
        L = k - inc[k] + 1
        R = k + right[k] - 1
        total = prefix[R+1] - prefix[L]
        res[k] = total
    
    print(' '.join(map(str, res)))

if __name__ == "__main__":
    solve()