import sys
import heapq

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    intervals = []
    for i in range(1, M+1):
        L, R = map(int, input().split())
        intervals.append((L, R, i))
    
    # Sort intervals by L
    intervals.sort(key=lambda x: x[0])
    
    # Initialize heap_type2 with all intervals as (-L_i, i)
    heap_type2 = []
    for L, R, i in intervals:
        heapq.heappush(heap_type2, (-L, i))
    
    # Initialize other heaps
    heap_type1 = []
    heap_finish = []
    
    used = [False] * (M+1)
    ops = [0] * (M+1)
    
    cur = 1
    idx = 0
    cost = 0
    
    while cur <= N:
        # Add intervals with L_i <= cur to appropriate heaps
        while idx < M and intervals[idx][0] <= cur:
            L, R, i = intervals[idx]
            idx += 1
            if used[i]:
                continue
            if L <= cur <= R:
                heapq.heappush(heap_type1, (-R, i))
            elif cur > R:
                heapq.heappush(heap_finish, (R, i))
            # If L > cur, it remains only in heap_type2 for now
        
        # Clean heaps: remove used operations and invalid entries
        while heap_type1:
            negR, i = heap_type1[0]
            if used[i]:
                heapq.heappop(heap_type1)
            else:
                break
        
        while heap_finish:
            R, i = heap_finish[0]
            if used[i]:
                heapq.heappop(heap_finish)
            else:
                break
        
        while heap_type2:
            negL, i = heap_type2[0]
            L_i = -negL
            if used[i] or L_i <= cur:
                heapq.heappop(heap_type2)
            else:
                break
        
        # Decide next action
        if heap_finish:
            # Finish: use type2 on interval with R_i < cur
            R, i = heapq.heappop(heap_finish)
            used[i] = True
            ops[i] = 2
            cost += 1
            cur = N + 1
            break
        elif heap_type1:
            # Use type1: pick interval with max R_i
            negR, i = heapq.heappop(heap_type1)
            R = -negR
            used[i] = True
            ops[i] = 1
            cost += 1
            cur = R + 1
        elif heap_type2:
            # Use type2 jump: pick interval with max L_i
            negL, i = heapq.heappop(heap_type2)
            L = -negL
            used[i] = True
            ops[i] = 2
            cost += 1
            cur = L
        else:
            # No valid operation
            print(-1)
            return
    
    if cur > N:
        print(cost)
        print(' '.join(map(str, ops[1:])))
    else:
        print(-1)

if __name__ == "__main__":
    solve()