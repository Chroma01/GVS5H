import sys
input = sys.stdin.readline

def solve():
    import sys
    sys.setrecursionlimit(1 << 25)
    N = int(input())
    W = list(map(int, input().split()))
    L = [0]*N
    R = [0]*N
    for i in range(N):
        l, r = map(int, input().split())
        L[i] = l
        R[i] = r
    Q = int(input())
    queries = []
    for _ in range(Q):
        s, t = map(int, input().split())
        queries.append((s-1, t-1))
    
    # Coordinate compression: endpoints up to 2N
    # We will sort intervals by L, and for each, find the nearest disjoint interval to the left and right.
    # The graph G is the comparability graph of the "left of" poset.
    # We claim that the minimum weight path between any two connected vertices has length at most 2.
    # Proof sketch: In the comparability graph of an interval order, if i and j are connected,
    # there exists a path of length at most 2. This is because the interval order is a suborder of a linear order,
    # and the comparability graph of a poset with dimension 1 (total order) is a complete graph.
    # For intervals, if i and j are not directly connected (i.e., they overlap), they must overlap.
    # Then there exists some interval k that is either left of both or right of both, because the intervals are on a line.
    # Actually, if i and j overlap, then either there is an interval completely to the left of both, or to the right of both,
    # or they are part of a "clique" that blocks all sides. But in the latter case, they are not connected.
    # So for connected i and j, there exists a common neighbor k (an interval disjoint from both).
    # Thus any connected pair has a path of length 2 (or 1 if directly connected).
    # Hence the minimum weight path is simply min( W[s] + W[t] if edge exists, min_{k} (W[s] + W[k] + W[t]) otherwise ).
    # So we only need to check if s and t are adjacent, or if there exists a k that is disjoint from both.
    # If adjacent, answer is W[s]+W[t]. Otherwise, if there is a k disjoint from both, answer is min_{k} (W[s]+W[k]+W[t]) = W[s]+W[t] + min_{k disjoint from both} W[k].
    # If no such k, then not connected, answer -1.
    # So the problem reduces to: for each query (s,t), determine if there exists a vertex k that is disjoint from both s and t.
    # If not, check if s and t are directly disjoint (edge). If neither, -1.
    # If yes (either direct or via k), compute the minimum weight path (length 1 or 2).
    
    # Preprocess: for each interval, we need to know if there is any interval to the left of it (disjoint) and any to the right.
    # Actually, we need to know, for a pair (s,t), if there exists a k disjoint from both.
    # This is equivalent to: is there a gap that separates both s and t from k?
    # More precisely, s and t are both on one side of k? If k is to the left of both, then R_k < min(L_s, L_t).
    # If k is to the right of both, then L_k > max(R_s, R_t).
    # So we need to know the minimum R among intervals that are to the left of s, and the maximum L among intervals to the right of s, etc.
    # Actually, we can precompute for each interval i:
    #   min_L_right[i] = the minimum L_j among intervals j with R_j < L_i? Not exactly.
    # We need to answer: does there exist an interval k such that R_k < min(L_s, L_t) OR L_k > max(R_s, R_t).
    # Let left_bound = min(L_s, L_t). If there is any interval with R < left_bound, then that interval is left of both s and t.
    # Let right_bound = max(R_s, R_t). If there is any interval with L > right_bound, then that interval is right of both.
    # So we just need to know the minimum R among all intervals, and the maximum L among all intervals.
    # But careful: k must be a vertex (interval). So we just need to check if there exists an interval entirely to the left of both s and t, or entirely to the right.
    # However, s and t themselves might be such intervals? But k must be a vertex, and s != t, so k can be any other vertex.
    # So if there is any interval with R < min(L_s, L_t), then we can use that as k, provided it's not s or t? But it could be s or t only if s or t is that interval. But if s has R_s < L_t, then s and t are already adjacent. So in that case, we don't need k. So we can just check the global minimum R and global maximum L.
    # But wait: what if the only interval to the left is s itself? Then s and t are adjacent if R_s < L_t. If they overlap, then L_t <= R_s, so min(L_s, L_t) = L_t, and R_s >= L_t, so R_s is not < L_t. So s is not to the left of both.
    # So the existence of any interval (including s or t) with R < min(L_s, L_t) is exactly the condition that there is an interval left of both, unless that interval is s or t and they are not adjacent? But if s has R_s < L_t, they are adjacent, so we already have a direct edge. So we can just check the global minimum R and global maximum L.
    # However, there is a catch: what if the interval to the left is exactly s or t, but s and t are not adjacent? That would mean R_s < L_t? But that's exactly adjacency. So if they are not adjacent, then no interval can be both to the left of s and t and be s or t. So any interval to the left of both is a different vertex.
    # Similarly for the right.
    # So the condition for connectivity (excluding direct edge) is: (global_min_R < min(L_s, L_t)) OR (global_max_L > max(R_s, R_t)).
    # But we also need the direct edge condition: s and t are disjoint iff R_s < L_t or R_t < L_s.
    # So overall, s and t are connected iff:
    #   (R_s < L_t) or (R_t < L_s)  [direct edge]
    #   or (global_min_R < min(L_s, L_t))  [there is some interval left of both]
    #   or (global_max_L > max(R_s, R_t))  [there is some interval right of both]
    # If connected, the minimum weight path is:
    #   If direct edge: W[s] + W[t]
    #   Else: W[s] + W[t] + min( W[k] for k that is left of both or right of both )
    # But we need the minimum W[k] among all such k.
    # So we need to precompute for each possible "left bound" and "right bound" the minimum weight of an interval that is to the left of that bound or to the right of that bound.
    # Specifically, let A = min(L_s, L_t). The set of intervals left of both is those with R < A. We need the minimum W among those.
    # Let B = max(R_s, R_t). The set of intervals right of both is those with L > B. We need the minimum W among those.
    # So we can precompute:
    #   For each possible left_bound x (1..2N), min_W_left[x] = minimum W_i such that R_i < x.
    #   For each possible right_bound x (1..2N), min_W_right[x] = minimum W_i such that L_i > x.
    # Then for a query (s,t):
    #   A = min(L_s, L_t)
    #   B = max(R_s, R_t)
    #   If direct edge: answer = W[s] + W[t]
    #   Else if min_W_left[A] exists or min_W_right[B] exists:
    #       best_k = min( min_W_left[A] if exists, min_W_right[B] if exists )
    #       answer = W[s] + W[t] + best_k
    #   Else: answer = -1
    
    # Let's verify with sample 1:
    # N=5, W: 5,1,4,2,2
    # L,R:
    # 0: [2,4]
    # 1: [1,2]
    # 2: [7,8]
    # 3: [4,5]
    # 4: [2,7]
    # global_min_R = min(4,2,8,5,7) = 2 (interval 1)
    # global_max_L = max(2,1,7,4,2) = 7 (interval 2)
    # Query 1: s=0(1), t=3(4)
    #   L_s=2, R_s=4; L_t=4, R_t=5. min(L)=2, max(R)=5.
    #   Direct? R_s=4 < L_t=4? No (4<4 false). R_t=5 < L_s=2? No.
    #   min_W_left[2]: R<2? None (min R is 2). So no left.
    #   min_W_right[5]: L>5? Yes, interval 2: L=7, W=1. So best_k=1. Answer = W[0]+W[3]+1 = 5+2+1=8? But expected 11. That's wrong because path is 1->3->4 (vertices 0,2,3). Vertex 2 has W=4, not 1. Our best_k was 1, but that path would be 1->2->4? But interval 2 is [7,8], is it disjoint from 1 and 4? 1:[2,4] and 2:[7,8] disjoint yes. 2:[7,8] and 4:[4,5] disjoint? 7>5 yes. So 1-2-4 is a path! Weight = 5+1+2=8. But sample says 11. Why is 8 not the answer? Because in G, is there an edge between 1 and 2? Interval 1 [2,4] and 2 [7,8] are disjoint, so yes edge. Between 2 and 4? [7,8] and [4,5] disjoint, yes. So path 1-2-4 exists. Weight = 5+1+2=8. But sample output says 11. So my assumption that length 2 path is always optimal is false! There is a path of length 2 with weight 8, which is less than 11. But the sample says the minimum is 11. So either I miscalculated, or the path 1-2-4 is not valid in G. Let's check: vertices are 1,2,3,4,5. Edges in G: 1-3, 2-3, 2-4, 3-4. Wait, sample says G has edges: {1,3}, {2,3}, {2,4}, {3,4}. That is vertices 1-3, 2-3, 2-4, 3-4. There is NO edge 1-2! Because [2,4] and [1,2] share 2, so they overlap. So 1 and 2 are not adjacent. So the path 1-2-4 uses vertices 1 and 2, but 1 and 2 are not connected. So 1-2 is not an edge. So my condition for edge: R_1=4, L_2=1, so 4<1 false. R_2=2, L_1=2, 2<2 false. So they are not disjoint. So no edge. So the path 1-2-4 is invalid because 1-2 is not an edge. So we need a path where every consecutive pair is disjoint. In my earlier analysis, I said if there is an interval k that is disjoint from both s and t, then s-k-t is a path. But that requires k to be disjoint from s AND disjoint from t. In this case, k=2 is disjoint from s=1? [2,4] and [7,8] are disjoint, yes. k=2 is disjoint from t=4? [7,8] and [4,5] are disjoint, yes. So k=2 is disjoint from both 1 and 4. So 1-2 and 2-4 should be edges. But 1-2 is not an edge because [2,4] and [1,2] are not disjoint! Wait, k=2 is vertex 2, which corresponds to interval 2: [1,2]. s=1 is interval 1: [2,4]. Are [2,4] and [1,2] disjoint? No, they share 2. So k=2 is NOT disjoint from s=1. I confused vertex indices. Let's correct: s=1 (vertex 1) has interval [2,4]. t=4 (vertex 4) has interval [4,5]. k=2 (vertex 2) has interval [1,2]. Is [2,4] disjoint from [1,2]? No, they share 2. So k=2 is not disjoint from s. So the path 1-2-4 is invalid. So my claim that any k with R_k < min(L_s, L_t) works is false because k might overlap with s even if it's left of t. For k to be left of both, we need R_k < L_s and R_k < L_t. So R_k < min(L_s, L_t). In this case, min(L_s, L_t) = min(2,4) = 2. So we need R_k < 2. But R_2 = 2, not < 2. So k=2 does not satisfy R_k < 2. So no left k. For right k, we need L_k > max(R_s, R_t) = max(4,5) = 5. L_2 = 1, not >5. L_3 = 7 >5, so k=3 (vertex 3) is right of both. Check: 3:[7,8] disjoint from 1:[2,4] yes, disjoint from 4:[4,5] yes. So k=3 is a valid intermediate. Weight of 3 is 4. So path 1-3-4 weight = 5+4+2=11. That matches.
    # So the condition for existence of a common neighbor k is: exists k with (R_k < min(L_s, L_t)) OR (L_k > max(R_s, R_t)).
    # And then the best k is the one with minimum W among those.
    # So my earlier condition was correct: min_W_left[A] where A = min(L_s, L_t), and min_W_right[B] where B = max(R_s, R_t).
    # But I must ensure that k is not s or t. However, if s itself has R_s < min(L_s, L_t), then R_s < L_t, so s and t are adjacent. So in the case we are looking for a length-2 path, s and t are not adjacent, so no such issue.
    # So the algorithm is:
    #   Precompute for each x from 1 to 2N+1:
    #     min_W_left[x] = min W_i such that R_i < x.
    #     min_W_right[x] = min W_i such that L_i > x.
    #   For each query (s,t):
    #     if R_s < L_t or R_t < L_s: ans = W[s] + W[t]
    #     else:
    #         A = min(L_s, L_t)
    #         B = max(R_s, R_t)
    #         best = inf
    #         if min_W_left[A] exists: best = min(best, min_W_left[A])
    #         if min_W_right[B] exists: best = min(best, min_W_right[B])
    #         if best == inf: ans = -1
    #         else: ans = W[s] + W[t] + best
    # But wait: what if the best k is s or t? That would mean we are using s or t as intermediate, but then the path would have length 1 (direct edge) which we already checked is not present. So if s and t are not adjacent, then R_s >= L_t and R_t >= L_s. So R_s < min(L_s, L_t) would imply R_s < L_t, contradiction. So s cannot be in the left set. Similarly for right.
    # So this works.
    # Let's test with sample 2 quickly mentally? Probably fine.
    # Complexity: O(N + Q) after O(N log N) for sorting? Actually we don't need sorting. We can compute min_W_left and min_W_right by iterating over all intervals.
    # Since R_i <= 2N, we can create arrays of size 2N+2.
    # Initialize min_W_left = [inf]*(2N+2), min_W_right = [inf]*(2N+2)
    # For each interval i:
    #   min_W_left[R_i+1] = min(min_W_left[R_i+1], W_i)  # because R_i < x means x > R_i, so smallest x is R_i+1
    #   min_W_right[L_i] = min(min_W_right[L_i], W_i)  # because L_i > x means x < L_i, so we can think of min_W_right[x] for x < L_i.
    # Actually, for min_W_right[x] = min W_i such that L_i > x, we can for each i, set min_W_right[x] for all x < L_i. But that's O(N^2). Instead, we can compute suffix/prefix mins.
    # Let's do:
    #   For min_W_left: for each i, let pos = R_i+1. min_W_left[pos] = min(min_W_left[pos], W_i). Then compute prefix min: for x from 1 to 2N+1: min_W_left[x] = min(min_W_left[x], min_W_left[x-1]).
    #   For min_W_right: for each i, let pos = L_i. min_W_right[pos] = min(min_W_right[pos], W_i). Then compute suffix min: for x from 2N down to 0: min_W_right[x] = min(min_W_right[x], min_W_right[x+1]).
    # Then min_W_left[x] gives min W_i with R_i < x. min_W_right[x] gives min W_i with L_i > x.
    # For query, A = min(L_s, L_t). We need min_W_left[A]. That gives min W_i with R_i < A. But A could be 1. min_W_left[1] means R_i < 1, i.e., R_i <=0, impossible. So careful with indices.
    # Let's set arrays of size 2N+3.
    # Coordinates are 1-indexed. R_i can be 2N. So R_i+1 can be 2N+1. L_i >=1.
    # So min_W_left: for x from 1 to 2N+1, min_W_left[x] = min_{i: R_i < x} W_i.
    # min_W_right: for x from 0 to 2N, min_W_right[x] = min_{i: L_i > x} W_i.
    # So for A = min(L_s, L_t), we need min_W_left[A].
    # For B = max(R_s, R_t), we need min_W_right[B].
    # But note: B can be up to 2N. min_W_right[2N] means L_i > 2N, which is impossible since L_i <= 2N. So min_W_right[2N] = inf. That's fine.
    # Also, A can be 1. min_W_left[1] means R_i < 1, impossible. So inf.
    # So this works.
    # Let's verify with sample 1:
    # 2N=10, arrays size 12.
    # Intervals:
    # 0: [2,4], W=5 -> R+1=5, min_W_left[5]=5; L=2, min_W_right[2]=5
    # 1: [1,2], W=1 -> R+1=3, min_W_left[3]=1; L=1, min_W_right[1]=1
    # 2: [7,8], W=4 -> R+1=9, min_W_left[9]=4; L=7, min_W_right[7]=4
    # 3: [4,5], W=2 -> R+1=6, min_W_left[6]=2; L=4, min_W_right[4]=2
    # 4: [2,7], W=2 -> R+1=8, min_W_left[8]=2; L=2, min_W_right[2]=min(5,2)=2
    # Compute prefix min for left:
    # min_W_left[1]=inf, 2=inf, 3=1, 4=1, 5=1 (min of 1 and 5), 6=1 (min of 1,2), 7=1, 8=1 (min of 1,2), 9=1, 10=1, 11=1
    # Actually, we need to be careful: prefix min should propagate smaller values. For x=4, min_W_left[4] should be min of original min_W_left[4] and min_W_left[3]=1. So min_W_left[4]=1. So min_W_left[x] for x>=3 is 1 until we see a smaller W? There is no smaller than 1. So min_W_left[3..11] = 1.
    # Compute suffix min for right:
    # min_W_right[10]=inf, 9=inf, 8=inf, 7=4, 6=2 (min of 2 and 4), 5=2, 4=2, 3=2, 2=1 (min of 2,1), 1=1, 0=1.
    # So min_W_right[7]=4, min_W_right[4]=2, min_W_right[5]=2, etc.
    # Query 1: s=0(2,4), t=3(4,5). A=min(2,4)=2. min_W_left[2]=inf. B=max(4,5)=5. min_W_right[5]=2. So best=2. ans=5+2+2=9? But expected 11. Wait, min_W_right[5]=2. That means there is an interval with L > 5 and W=2. Which one? Interval 4: [2,7] has L=2 not >5. Interval 0: [2,4] L=2. Interval 1: [1,2] L=1. Interval 3: [4,5] L=4 not >5. Interval 2: [7,8] L=7 >5, W=4. So min_W_right[5] should be 4, not 2. Why did I get 2? Because interval 4 has L=2, which is not >5. So my min_W_right[5] should be inf? Let's recalc min_W_right carefully.
    # min_W_right[x] = min_{i: L_i > x} W_i.
    # For x=5, we need L_i > 5. Only interval 2 has L=7. So min should be 4. Why did I get 2? Because I did suffix min incorrectly. Let's recompute:
    # Initialize min_W_right with inf.
    # For each i, we set min_W_right[L_i] = min(..., W_i). So:
    # i=0: L=2 -> min_W_right[2] = min(inf,5)=5
    # i=1: L=1 -> min_W_right[1] = min(inf,1)=1
    # i=2: L=7 -> min_W_right[7] = min(inf,4)=4
    # i=3: L=4 -> min_W_right[4] = min(inf,2)=2
    # i=4: L=2 -> min_W_right[2] = min(5,2)=2
    # So min_W_right: [inf, 1, 2, inf, 2, inf, inf, 4, inf, inf, inf, ...]
    # Now suffix min: for x from 2N down to 0: min_W_right[x] = min(min_W_right[x], min_W_right[x+1])
    # Start from x=10: min_W_right[10]=inf
    # 9: min(inf, inf)=inf
    # 8: min(inf, inf)=inf
    # 7: min(4, inf)=4
    # 6: min(inf, 4)=4
    # 5: min(inf, 4)=4
    # 4: min(2, 4)=2  (this is min for L>4: interval 2 has L=7, W=4; interval 3 has L=4 not >4, so not included. But wait, L>4 means L>=5. So interval 3 with L=4 is not >4. So min_W_right[4] should be 4. Why did I get 2? Because min_W_right[4] was set to 2 from interval 3, but interval 3 has L=4, which is not >4. So we should not have set min_W_right[4] for interval 3. The condition is L_i > x. So for x=4, we need L_i >=5. So we should set min_W_right[L_i] for x < L_i, i.e., for all x from 0 to L_i-1. That's why we need to set it for all x < L_i, not at L_i. So the correct way: for each interval i, for all x in [0, L_i-1], min_W_right[x] = min(min_W_right[x], W_i). That's O(N^2). Instead, we can set min_W_right[L_i-1] and then do suffix min? Actually, if we set min_W_right[x] for x = L_i-1, then suffix min will propagate to all smaller x. So we can do: for each i, let pos = L_i - 1. min_W_right[pos] = min(min_W_right[pos], W_i). Then suffix min from 2N down to 0.
    # Similarly for min_W_left: we need R_i < x. So for each i, set min_W_left[R_i+1] = min(..., W_i). Then prefix min.
    # Let's redo with this correction.
    # For min_W_left: R_i < x. For i, R_i=4 -> x>4, so smallest x=5. So set min_W_left[5]=5. i=1: R=2 -> set min_W_left[3]=1. i=2: R=8 -> set min_W_left[9]=4. i=3: R=5 -> set min_W_left[6]=2. i=4: R=7 -> set min_W_left[8]=2.
    # Then prefix min: min_W_left[1]=inf, 2=inf, 3=1, 4=1, 5=min(5,1)=1, 6=min(2,1)=1, 7=1, 8=min(2,1)=1, 9=min(4,1)=1, 10=1, 11=1.
    # So min_W_left[2]=inf, min_W_left[4]=1? Wait, for query 1, A=min(L_s, L_t)=min(2,4)=2. min_W_left[2]=inf. So no left k.
    # For min_W_right: L_i > x. For i, L=2 -> x<2, so largest x=1. So set min_W_right[1]=min(inf,5)=5. i=1: L=1 -> set min_W_right[0]=1. i=2: L=7 -> set min_W_right[6]=4. i=3: L=4 -> set min_W_right[3]=2. i=4: L=2 -> set min_W_right[1]=min(5,2)=2.
    # Then suffix min: start from 2N=10 down to 0.
    # min_W_right[10]=inf, 9=inf, 8=inf, 7=inf, 6=4, 5=4, 4=min(inf,4)=4, 3=min(2,4)=2, 2=min(inf,2)=2, 1=min(2,2)=2, 0=min(1,2)=1.
    # So min_W_right[5]=4. For query 1, B=max(R_s, R_t)=max(4,5)=5. min_W_right[5]=4. best=4. ans=5+2+4=11. Correct.
    # Query 2: s=3(4,5), t=2(7,8). A=min(4,7)=4. min_W_left[4]=1? Wait, min_W_left[4]=1 (from prefix min: 1). That means there is an interval with R < 4. Which one? Interval 1: R=2, W=1. Is interval 1 disjoint from both 3 and 2? 3:[4,5], 1:[1,2] -> R=2 < L=4, yes. 2:[7,8], 1:[1,2] -> R=2 < L=7, yes. So k=1 is valid. So best=1. Direct edge? R_3=5 < L_2=7? Yes, 5<7, so they are adjacent! So direct edge weight = W[3]+W[2]=2+4=6. min_W_left gives 1, so length-2 path would be 2+1+4=7, but direct is 6. So we take min. So we need to consider direct edge first. In my algorithm, I check direct edge first, so ans=6. Correct.
    # Query 3: s=4(2,7), t=1(1,2). A=min(2,1)=1. min_W_left[1]=inf. B=max(7,2)=7. min_W_right[7]=inf? min_W_right[7] is inf because suffix min at 7 is inf. So no k. Direct edge? R_4=7 < L_1=1? No. R_1=2 < L_4=2? No. So not connected, ans=-1. Correct.
    # So the algorithm works for sample 1.
    # Let's test sample 2 briefly? Probably works.
    # Edge cases: what if s and t are the same? Not allowed.
    # What if min_W_left[A] is inf and min_W_right[B] is inf? Then not connected.
    # Complexity: O(N + Q).
    # We just need to handle large INF.
    
    INF = 10**18
    size = 2*N + 3
    min_W_left = [INF] * size
    min_W_right = [INF] * size
    for i in range(N):
        l = L[i]
        r = R[i]
        w = W[i]
        # For min_W_left: R_i < x. Set at r+1.
        pos = r + 1
        if pos < size:
            if w < min_W_left[pos]:
                min_W_left[pos] = w
        # For min_W_right: L_i > x. Set at l-1.
        pos = l - 1
        if pos >= 0:
            if w < min_W_right[pos]:
                min_W_right[pos] = w
    # Prefix min for left
    for x in range(1, size):
        if min_W_left[x-1] < min_W_left[x]:
            min_W_left[x] = min_W_left[x-1]
    # Suffix min for right
    for x in range(size-2, -1, -1):
        if min_W_right[x+1] < min_W_right[x]:
            min_W_right[x] = min_W_right[x+1]
    
    out_lines = []
    for s, t in queries:
        ls = L[s]; rs = R[s]
        lt = L[t]; rt = R[t]
        # Direct edge?
        if rs < lt or rt < ls:
            out_lines.append(str(W[s] + W[t]))
            continue
        A = ls if ls < lt else lt
        B = rs if rs > rt else rt
        best = INF
        if min_W_left[A] < best:
            best = min_W_left[A]
        if min_W_right[B] < best:
            best = min_W_right[B]
        if best == INF:
            out_lines.append("-1")
        else:
            out_lines.append(str(W[s] + W[t] + best))
    
    sys.stdout.write("\n".join(out_lines))

solve()