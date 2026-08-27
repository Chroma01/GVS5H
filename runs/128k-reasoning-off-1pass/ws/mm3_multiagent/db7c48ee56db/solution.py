import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    if K == 1:
        print(max(A))
        return
    if K == N:
        xor_all = 0
        for a in A:
            xor_all ^= a
        print(xor_all)
        return
    
    comb = list(range(K))
    max_xor = 0
    while True:
        cur_xor = 0
        for idx in comb:
            cur_xor ^= A[idx]
        if cur_xor > max_xor:
            max_xor = cur_xor
        # Generate next combination
        i = K - 1
        while i >= 0 and comb[i] == N - K + i:
            i -= 1
        if i < 0:
            break
        comb[i] += 1
        for j in range(i + 1, K):
            comb[j] = comb[j-1] + 1
            
    print(max_xor)

if __name__ == "__main__":
    solve()