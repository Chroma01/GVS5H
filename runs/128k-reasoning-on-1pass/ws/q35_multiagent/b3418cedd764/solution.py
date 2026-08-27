import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    N = int(next(iterator))
    M = int(next(iterator))
    
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(iterator))
        
    MOD = 998244353
    
    rev_adj = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)
    
    for i in range(1, N + 1):
        rev_adj[A[i]].append(i)
        in_degree[A[i]] += 1
        
    queue = [i for i in range(1, N + 1) if in_degree[i] == 0]
    
    dp = [None] * (N + 1)
    S = [None] * (N + 1)
    processed = [False] * (N + 1)
    
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        processed[u] = True
        
        dp[u] = [1] * (M + 1)
        for w in rev_adj[u]:
            dp[u] = [(x * s) % MOD for x, s in zip(dp[u], S[w])]
            
        current_sum = 0
        S[u] = [0] * (M + 1)
        for v in range(1, M + 1):
            current_sum = (current_sum + dp[u][v]) % MOD
            S[u][v] = current_sum
            
        v = A[u]
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
            
    ans = 1
    for i in range(1, N + 1):
        if not processed[i]:
            cycle = []
            curr = i
            while not processed[curr]:
                cycle.append(curr)
                processed[curr] = True
                curr = A[curr]
                
            cycle_set = set(cycle)
            
            for c in cycle:
                dp[c] = [1] * (M + 1)
                for w in rev_adj[c]:
                    if w in cycle_set:
                        continue
                    dp[c] = [(x * s) % MOD for x, s in zip(dp[c], S[w])]
                    
            comp_ans = 0
            for v in range(1, M + 1):
                ways = 1
                for c in cycle:
                    ways = (ways * dp[c][v]) % MOD
                comp_ans = (comp_ans + ways) % MOD
                
            ans = (ans * comp_ans) % MOD
            
    print(ans)

if __name__ == '__main__':
    solve()