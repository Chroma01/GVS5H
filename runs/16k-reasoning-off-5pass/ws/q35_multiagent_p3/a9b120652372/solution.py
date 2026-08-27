import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        T_str = next(iterator)
    except StopIteration:
        return
        
    T = int(T_str)
    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = next(iterator)
            B = next(iterator)
        except StopIteration:
            break
            
        # Extract positions of pieces in A and targets in B
        # Using 0-based indexing for internal logic
        pieces = [i for i, char in enumerate(A) if char == '1']
        targets = [i for i, char in enumerate(B) if char == '1']
        
        k = len(pieces)
        m = len(targets)
        
        # If fewer pieces than targets, impossible
        if k < m:
            results.append("-1")
            continue
            
        # Binary search for the minimum maximum displacement D
        low = 0
        high = N # Maximum possible displacement is N
        ans = -1
        
        # Pre-calculate lengths for faster access
        # pieces and targets are already lists
        
        while low <= high:
            mid = (low + high) // 2
            D = mid
            
            # Check if D is feasible
            # We need to map each target t_j to a distinct piece p_i
            # such that |p_i - t_j| <= D, and the mapping preserves order.
            # Greedy strategy: for each target in order, pick the earliest available piece that can reach it.
            
            feasible = True
            piece_idx = 0
            
            for t in targets:
                # Find the first piece_idx >= current piece_idx such that |pieces[piece_idx] - t| <= D
                # Since pieces are sorted, we can just advance piece_idx
                
                # Optimization: if piece_idx is already out of bounds, break
                if piece_idx >= k:
                    feasible = False
                    break
                
                # We need to find smallest j >= piece_idx such that pieces[j] is in [t-D, t+D]
                # Since pieces is sorted, we can just scan forward.
                # However, scanning from scratch for each target might be O(N^2) in worst case.
                # But note that piece_idx only increases. So total scan is O(k).
                
                found = False
                while piece_idx < k:
                    p = pieces[piece_idx]
                    if abs(p - t) <= D:
                        found = True
                        piece_idx += 1 # Use this piece, move to next for next target
                        break
                    else:
                        # If p < t - D, this piece is too far left, skip it?
                        # Wait, if p < t - D, then p is too far left to reach t.
                        # Can a later piece reach t? Yes, if it's closer.
                        # If p > t + D, then this piece is too far right.
                        # Since pieces are sorted, all subsequent pieces are also > t + D.
                        # So if we encounter a piece > t + D, we can stop and say not found.
                        if p > t + D:
                            break
                        piece_idx += 1
                
                if not found:
                    feasible = False
                    break
            
            if feasible:
                ans = D
                high = mid - 1
            else:
                low = mid + 1
                
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()