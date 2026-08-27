import sys
from collections import Counter

def main():
    sys.setrecursionlimit(300000)
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    K = int(next(it))
    total_nodes = N * K
    
    adj = [[] for _ in range(total_nodes + 1)]
    for _ in range(total_nodes - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)
        
    ok = True
    
    def dfs(u, p):
        nonlocal ok
        if not ok:
            return 0
            
        child_vals = []
        for v in adj[u]:
            if v == p:
                continue
            res = dfs(v, u)
            if not ok:
                return 0
            if res < K:
                child_vals.append(res)
                
        if not child_vals:
            return 1
            
        cnt = Counter(child_vals)
        for x in list(cnt.keys()):
            if cnt[x] == 0:
                continue
            y = K - 1 - x
            if y == x:
                p_cnt = cnt[x] // 2
                cnt[x] -= p_cnt * 2
            elif y > x:
                if y in cnt:
                    p_cnt = min(cnt[x], cnt[y])
                    cnt[x] -= p_cnt
                    cnt[y] -= p_cnt
                    
        rem = sum(cnt.values())
        if rem > 1:
            ok = False
            return 0
        elif rem == 1:
            val = next(x for x in cnt if cnt[x] > 0)
            return val + 1
        else:
            return 1

    final_res = dfs(1, 0)
    
    if ok and final_res == K:
        sys.stdout.write("Yes\n")
    else:
        sys.stdout.write("No\n")

if __name__ == "__main__":
    main()