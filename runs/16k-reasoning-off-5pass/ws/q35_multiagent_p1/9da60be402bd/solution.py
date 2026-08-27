import sys
from collections import deque

def solve():
    # Increase recursion depth just in case, though we use iterative BFS
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    N = int(data[0])
    grid = data[1:]
    
    # Precompute adjacency lists grouped by character
    # out_edges[u][c] = list of v such that u -> v with label c
    # in_edges[v][c] = list of u such that u -> v with label c (i.e., v <- u)
    # We use a dictionary for sparse character storage, or list of size 26
    
    # Map 'a'-'z' to 0-25
    char_to_idx = {chr(ord('a') + i): i for i in range(26)}
    
    out_edges = [[[] for _ in range(26)] for _ in range(N + 1)]
    in_edges = [[[] for _ in range(26)] for _ in range(N + 1)]
    
    # Also store direct edges for odd-length palindrome check
    # direct_edges[u][v] = True if edge u->v exists
    # We can use a set or a 2D boolean array
    has_edge = [[False] * (N + 1) for _ in range(N + 1)]
    
    for r in range(N):
        row_str = grid[r]
        u = r + 1
        for c_idx in range(N):
            ch = row_str[c_idx]
            if ch != '-':
                v = c_idx + 1
                idx = char_to_idx[ch]
                out_edges[u][idx].append(v)
                in_edges[v][idx].append(u)
                has_edge[u][v] = True

    # Initialize answer matrix with -1
    # ans[i][j] will store the shortest palindrome path length from i to j
    ans = [[-1] * (N + 1) for _ in range(N + 1)]
    
    # For each pair (i, j), run BFS
    # State: (u, v) meaning we have matched a prefix of length k from i to u
    # and a suffix of length k from j to v (reversed).
    # Distance k is stored in dist[u][v]
    
    # To optimize, we can reuse the dist array and queue
    # But since N is small (100), we can allocate new ones per pair if needed.
    # However, allocating N*N arrays N*N times is O(N^4) memory ops, which is fine.
    
    # We will use a 2D array for distances for the current BFS
    # dist[u][v] = k, or infinity if not visited
    
    INF = 10**9
    
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            # BFS initialization
            # dist[u][v] stores the minimum k such that there is a path i->...->u
            # and j->...->v (reversed) of length k with matching labels.
            
            # We use a list of lists for dist
            dist = [[INF] * (N + 1) for _ in range(N + 1)]
            queue = deque()
            
            # Base case: k=0
            # Path from i to i and j to j (empty) match.
            # But wait, the state (i, j) means we are at i from start and j from end.
            # If i == j, we have a palindrome of length 0.
            
            dist[i][j] = 0
            queue.append((i, j))
            
            # We also need to track the minimum palindrome length found so far for (i, j)
            min_pal_len = INF
            
            # If i == j, empty path is a palindrome of length 0
            if i == j:
                min_pal_len = 0
            
            # Check for odd length palindromes of length 1: edge i->j
            if has_edge[i][j]:
                min_pal_len = 1
            
            while queue:
                u, v = queue.popleft()
                k = dist[u][v]
                
                # If we have already found a palindrome shorter than what we could possibly find
                # by extending further, we can stop? 
                # Not exactly, because we might find a shorter one later in the BFS?
                # No, BFS finds shortest paths. The first time we see a meeting state (u,u) or an odd case,
                # it is the shortest for that specific meeting.
                # However, we want the global minimum for (i,j).
                # Since BFS expands by k=0, 1, 2..., the first time we find ANY palindrome, it is minimal?
                # Not necessarily. We might find an odd palindrome of length 2k+1 at step k,
                # but there might be an even palindrome of length 2k' with k' < k+1?
                # Actually, we process states in increasing order of k.
                # At state (u, v) with distance k, we can form:
                # 1. Even palindrome of length 2k if u == v.
                # 2. Odd palindrome of length 2k+1 if edge u->v exists.
                # 3. Extend to states with distance k+1.
                
                # Since we process in increasing k, the first time we encounter a valid palindrome
                # (either u==v or edge u->v), it is the shortest?
                # Yes, because any other palindrome would require a state with distance >= k.
                # If we find one at distance k, it is minimal.
                
                if min_pal_len != INF:
                    # We already found a palindrome. Since BFS is by layers,
                    # any future palindrome will have length >= current min_pal_len?
                    # Not necessarily. We might find a length 2k at layer k,
                    # but there could be a length 2k-1 at layer k-1 that we missed?
                    # No, we check at each layer.
                    # Actually, we should just break if we found a palindrome?
                    # Let's verify:
                    # Layer 0: k=0. Check u==v (len 0), check edge u->v (len 1).
                    # Layer 1: k=1. Check u==v (len 2), check edge u->v (len 3).
                    # So yes, the first time we find a valid palindrome, it is the shortest.
                    break
                
                # Check for even length palindrome
                if u == v:
                    min_pal_len = 2 * k
                    # We can break here because any other palindrome found later will be longer
                    break
                
                # Check for odd length palindrome
                if has_edge[u][v]:
                    min_pal_len = 2 * k + 1
                    break
                
                # Extend to next layer
                # We need to find all (u', v') such that there is an edge u->u' with label c1
                # and an edge v'->v with label c2, and c1 == c2.
                # New distance k+1.
                
                next_k = k + 1
                
                # Iterate over all characters
                for c in range(26):
                    # Get neighbors from u forward
                    if not out_edges[u][c]:
                        continue
                    
                    # Get neighbors from v backward (incoming to v)
                    if not in_edges[v][c]:
                        continue
                        
                    # For each pair (u', v')
                    for u_next in out_edges[u][c]:
                        for v_next in in_edges[v][c]:
                            if dist[u_next][v_next] == INF:
                                dist[u_next][v_next] = next_k
                                queue.append((u_next, v_next))
            
            ans[i][j] = min_pal_len

    # Print the answer
    for i in range(1, N + 1):
        print(" ".join(map(str, ans[i][1:])))

solve()