import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    iterator = iter(data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = int(next(iterator))
        B = int(next(iterator))
        
        bad_intervals = []
        for _ in range(M):
            L = int(next(iterator))
            R = int(next(iterator))
            bad_intervals.append((L, R))
    except StopIteration:
        return
    
    # Check for impenetrable walls
    for L, R in bad_intervals:
        if R - L + 1 >= B:
            print("No")
            return
        
    # Reachable intervals
    reachable = [(1, 1)]
    
    for L, R in bad_intervals:
        new_reachable = []
        for u, v in reachable:
            if v < L:
                # Fast-forward to get as close to L as possible without crossing it
                # We want max k such that v + k*B < L
                k = (L - v - 1) // B
                if k > 0:
                    u += k * A
                    v += k * B
                # Expand one step
                u += A
                v += B
                if v < L:
                    continue # Discard, cannot reach L or beyond
                # Clip against [L, R]
                if u > R:
                    new_reachable.append((u, v))
                elif v < L:
                    continue
                else:
                    if u < L:
                        new_reachable.append((u, L-1))
                    if v > R:
                        new_reachable.append((R+1, v))
            elif u > R:
                new_reachable.append((u, v))
            else:
                # Overlap with [L, R]
                # This should not happen if we process in order and clip correctly
                pass
        
        reachable = new_reachable
        # Merge intervals
        if not reachable:
            print("No")
            return
        reachable.sort()
        merged = []
        for u, v in reachable:
            if merged and u <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], v))
            else:
                merged.append((u, v))
        reachable = merged
    
    # Check if N is reachable
    for u, v in reachable:
        if u <= N <= v:
            print("Yes")
            return
        if v < N:
            if v - u + 1 >= B:
                # Solid interval, can reach everything to the right
                if N >= u + A:
                    print("Yes")
                    return
            else:
                # Not solid, simulate expansion
                temp_u, temp_v = u, v
                for _ in range(B + 2):
                    temp_u += A
                    temp_v += B
                    if temp_u <= N <= temp_v:
                        print("Yes")
                        return
                    if temp_v - temp_u + 1 >= B:
                        if N >= temp_u + A:
                            print("Yes")
                            return
                        break
    
    print("No")

if __name__ == '__main__':
    solve()