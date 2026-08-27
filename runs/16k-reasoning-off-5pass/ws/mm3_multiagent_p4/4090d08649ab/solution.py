import sys
sys.setrecursionlimit(1 << 25)

def solve():
    input = sys.stdin.readline
    N = int(input())
    A = [0] + list(map(int, input().split()))  # 1-indexed
    
    # Precompute sum of distinct over all subarrays
    last = [0] * (N + 2)
    sum_distinct = 0
    for i in range(1, N + 1):
        v = A[i]
        prev = last[v]
        sum_distinct += i - prev
        last[v] = i
    
    sum_adj = 0  # total sum of adj over all subarrays
    
    def dc(l, r):
        nonlocal sum_adj
        if l == r:
            return
        mid = (l + r) // 2
        dc(l, mid)
        dc(mid + 1, r)
        
        left_cnt = [0] * (N + 2)
        last_pos = [0] * (N + 2)
        for i in range(mid, l - 1, -1):
            v = A[i]
            if last_pos[v] == 0:
                last_pos[v] = i
                left_cnt[v] = i - l + 1
        
        right_cnt = [0] * (N + 2)
        first_pos = [0] * (N + 2)
        for i in range(mid + 1, r + 1):
            v = A[i]
            if first_pos[v] == 0:
                first_pos[v] = i
                right_cnt[v] = r - i + 1
        
        cross = 0
        for v in range(1, N + 1):
            a = left_cnt[v]
            c = right_cnt[v]
            d = right_cnt[v+1] if v+1 <= N else 0
            b = left_cnt[v+1] if v+1 <= N else 0
            cross += a * d + b * c
        sum_adj += cross
    
    dc(1, N)
    
    ans = sum_distinct - sum_adj
    print(ans)

if __name__ == "__main__":
    solve()