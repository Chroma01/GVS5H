import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    total_subarrays = N * (N + 1) // 2
    
    # Compute cnt_contains[v] = number of subarrays containing at least one v
    cnt_contains = [0] * (N + 1)
    last_occ = [0] * (N + 1)
    sum_D = 0
    for i in range(1, N + 1):
        v = A[i - 1]
        cnt_contains[v] += (i - last_occ[v]) * (N - i + 1)
        last_occ[v] = i
    for v in range(1, N + 1):
        sum_D += cnt_contains[v]
    
    # missing[v] = subarrays not containing v
    missing = [0] * (N + 1)
    for v in range(1, N + 1):
        missing[v] = total_subarrays - cnt_contains[v]
    
    # Compute missing_both[x] for x=1..N-1: subarrays containing neither x nor x+1
    if N == 1:
        # No pairs, answer is just sum_D (which is 1)
        print(sum_D)
        return
        
    last_pair = [0] * (N + 1)  # index 1..N-1 used
    sum_closed = [0] * (N + 1)
    
    for i in range(1, N + 1):
        v = A[i - 1]
        # x = v-1
        x = v - 1
        if 1 <= x <= N - 1:
            L = i - last_pair[x] - 1
            sum_closed[x] += L * (L + 1) // 2
            last_pair[x] = i
        # x = v
        x = v
        if 1 <= x <= N - 1:
            L = i - last_pair[x] - 1
            sum_closed[x] += L * (L + 1) // 2
            last_pair[x] = i
    
    # Close final gaps
    for x in range(1, N):
        L = N - last_pair[x]
        sum_closed[x] += L * (L + 1) // 2
    
    # sum_C = sum over pairs of count_x
    sum_C = 0
    for x in range(1, N):
        count_x = total_subarrays - missing[x] - missing[x + 1] + sum_closed[x]
        sum_C += count_x
    
    ans = sum_D - sum_C
    print(ans)

if __name__ == "__main__":
    solve()