import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        T_str = next(iterator)
    except StopIteration:
        return
        
    T = int(T_str)
    results = []
    
    for _ in range(T):
        try:
            R = int(next(iterator))
            B = int(next(iterator))
        except StopIteration:
            break
            
        N = R + B
        
        # Condition 1: R must be even.
        # Reasoning:
        # Let P(i) = (r_i + c_i) % 2.
        # Red move: changes parity (0 -> 1 or 1 -> 0).
        # Blue move: preserves parity (0 -> 0 or 1 -> 1).
        # In a cycle of length N, the sum of parity changes must be 0 mod 2.
        # Total changes = (Number of Red moves) * 1 + (Number of Blue moves) * 0 = R.
        # So R must be even.
        if R % 2 != 0:
            results.append("No")
            continue
            
        # If R is even, a solution always exists.
        # Construction Strategy:
        # 1. Create a base cycle of R Red moves.
        #    Since R is even, we can form a cycle of R Red moves on a 2xK grid.
        #    For R=2: (1,1) -> (1,2) -> (1,1) (2 Red moves).
        #    For R>=4: (1,1)->(1,2)->...->(1,k)->(2,k)->...->(2,1)->(1,1).
        #    This uses 2k = R moves.
        # 2. Insert B Blue moves.
        #    We can replace one Red edge u->w with a path u->v1->v2->...->vk->w
        #    where u->v1 is Blue, v1->v2 is Blue, ..., vk->w is Red.
        #    Specifically, we replace the edge (1,1)->(1,2) with a path of B Blue moves
        #    followed by a Red move to (1,2).
        #    Path: (1,1) -> (2,2) -> (1,3) -> (2,2) -> ... -> (1,3) -> (1,2).
        #    This adds B Blue moves and keeps the number of Red moves constant (the last step is Red).
        #    The total number of pieces becomes R + B.
        
        # Step 1: Construct base cycle points (excluding the first point which is part of the insertion)
        # Actually, we construct the full sequence directly.
        
        # Base cycle points for R Reds:
        # If R == 2: [(1,1), (1,2)]
        # If R >= 4: [(1,1), (1,2), ..., (1,k), (2,k), (2,k-1), ..., (2,1)] where k = R/2
        
        if R == 2:
            base_cycle_points = [(1, 1), (1, 2)]
        else:
            k = R // 2
            base_cycle_points = []
            # Row 1: 1 to k
            for c in range(1, k + 1):
                base_cycle_points.append((1, c))
            # Row 2: k to 1
            for c in range(k, 0, -1):
                base_cycle_points.append((2, c))
        
        # Step 2: Construct the Blue insertion path replacing (1,1)->(1,2)
        # The path starts at (1,1) and ends at (1,2).
        # It contains B Blue moves.
        # Pattern of intermediates: (2,2), (1,3), (2,2), (1,3), ...
        # If B=1: (1,1) -> (2,2) -> (1,2) [1 Blue, 1 Red]
        # If B=2: (1,1) -> (2,2) -> (1,3) -> (1,2) [2 Blue, 1 Red]
        # If B=3: (1,1) -> (2,2) -> (1,3) -> (2,2) -> (1,2) [3 Blue, 1 Red]
        
        blue_path_points = [(1, 1)]
        for i in range(1, B + 1):
            if i % 2 == 1:
                blue_path_points.append((2, 2))
            else:
                blue_path_points.append((1, 3))
        blue_path_points.append((1, 2))
        
        # Step 3: Combine
        # The sequence is the blue_path_points followed by the rest of the base cycle.
        # The base cycle starts with (1,1), (1,2). We replaced these with blue_path_points.
        # So we append base_cycle_points[2:] (skipping the first two points).
        
        full_sequence = blue_path_points + base_cycle_points[2:]
        
        # Step 4: Assign types
        # The first B pieces correspond to the B Blue moves in the path.
        # The remaining R pieces correspond to the R Red moves.
        # Note: The move from the last piece back to the first is Red (from (2,1) or (1,2) to (1,1)).
        # So the last piece must be Red.
        # Pieces 0 to B-1 are Blue.
        # Pieces B to N-1 are Red.
        
        output_lines = []
        for i in range(N):
            r, c = full_sequence[i]
            if i < B:
                p = "B"
            else:
                p = "R"
            output_lines.append(f"{p} {r} {c}")
            
        results.append("Yes")
        results.extend(output_lines)
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()