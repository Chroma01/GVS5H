import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        T = int(next(iterator))
    except StopIteration:
        return

    results = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            A = next(iterator)
            B = next(iterator)
        except StopIteration:
            break
            
        posA = [i for i, c in enumerate(A) if c == '1']
        posB = [i for i, c in enumerate(B) if c == '1']
        
        nA = len(posA)
        nB = len(posB)
        
        if nB > nA:
            results.append("-1")
            continue
            
        # If nB < nA, we need to merge pieces.
        # We map posB[j] to posA[j] for j in 0..nB-1.
        # The remaining pieces posA[nB:] are merged into posA[nB-1] or neighbors.
        # Actually, the standard solution maps the first nB pieces of A to B.
        # The cost is calculated based on shifts and gap reductions.
        
        # Check parity constraints for the mapped pieces.
        # The relative parity of distances must be preserved modulo 2?
        # Actually, the operation preserves the parity of the position of each piece relative to the pivot?
        # No, it flips parity for all pieces not at pivot.
        # However, a known invariant is that (posA[i] - posA[j]) % 2 == (posB[i] - posB[j]) % 2 is NOT required.
        # But (posA[i] % 2) can change.
        
        # Let's use the formula:
        # Cost = max( shifts_needed, merges_needed )? No.
        # Cost = sum of merges + shifts?
        
        # Correct logic:
        # 1. We can shift the entire configuration. Let the first piece move from posA[0] to posB[0].
        #    Shift amount S = posB[0] - posA[0].
        #    This requires |S| operations if done purely by shifts.
        # 2. We can reduce gaps.
        #    For each j from 0 to nB-2:
        #       gapA = posA[j+1] - posA[j]
        #       gapB = posB[j+1] - posB[j]
        #       If gapA < gapB, impossible? No, we can't expand gaps.
        #       If (gapA - gapB) % 2 != 0, impossible?
        #       Actually, parity of gap size is invariant modulo 2?
        #       Gap reduces by 2. So (gapA - gapB) must be even and non-negative.
        #       Merges needed for this gap = (gapA - gapB) // 2.
        
        # But wait, if nB < nA, we map posB[j] to posA[j].
        # The pieces posA[nB:] are effectively merged into posA[nB-1] (or the last mapped piece).
        # The gap between posA[nB-1] and posA[nB] must be reduced to 0?
        # Yes, they merge. So gapA = posA[nB] - posA[nB-1], gapB = 0.
        # Merges needed = gapA // 2.
        
        # Is it always optimal to map posB[j] to posA[j]?
        # Yes, because shifting the mapping would increase the total shift distance.
        
        possible = True
        total_merges = 0
        max_shift = 0
        
        # Check mapped pieces
        for j in range(nB):
            # Parity check: The parity of the position of the j-th piece relative to the first piece?
            # Actually, let's check if the transformation is possible.
            # The operation allows shifting all pieces by 1 (cost 1) or reducing a gap by 2 (cost 1).
            # Shifting changes the parity of all pieces.
            # Reducing a gap preserves the parity of the positions of the pieces involved?
            # If we reduce gap between j and j+1, j moves right, j+1 moves left.
            # pos[j] -> pos[j]+1, pos[j+1] -> pos[j+1]-1.
            # Parity of both flips.
            # So, if we do k merges, the parity of all pieces flips k times?
            # No, merges at different gaps affect different sets?
            # Actually, ANY merge operation flips the parity of ALL pieces?
            # No. If pivot is between j and j+1:
            # Pieces <= j move right (parity flip).
            # Pieces >= j+1 move left (parity flip).
            # So ALL pieces flip parity.
            # Shift operations:
            # Pivot at 1 (left of all): All move right (parity flip).
            # Pivot at N (right of all): All move left (parity flip).
            # So EVERY operation flips the parity of EVERY piece.
            # Therefore, after K operations, the parity of each piece has flipped K times.
            # So posA[i] + K == posB[i] (mod 2) for all i?
            # This implies posA[i] - posB[i] must have the same parity for all i.
            # i.e., (posA[i] - posB[i]) % 2 == (posA[0] - posB[0]) % 2.
            
            if (posA[j] - posB[j]) % 2 != (posA[0] - posB[0]) % 2:
                possible = False
                break
        
        if not possible:
            results.append("-1")
            continue
            
        # Calculate shifts and merges
        # Let K be the total number of operations.
        # Each operation flips parity.
        # So K must have the same parity as (posA[0] - posB[0]).
        # Also, K >= |posA[0] - posB[0]|? Not necessarily, because merges also move pieces.
        
        # Let's calculate the minimum K.
        # We know that each operation can reduce the "total distance" or "gap sum".
        # But a simpler bound:
        # The number of merges required for gap j is M_j = (posA[j+1] - posA[j] - (posB[j+1] - posB[j])) // 2.
        # This is valid for j < nB-1.
        # For the last part, if nB < nA, we have extra pieces.
        # The last mapped piece is posA[nB-1] -> posB[nB-1].
        # The next piece posA[nB] must merge into posA[nB-1].
        # So gapA = posA[nB] - posA[nB-1], gapB = 0.
        # M_nB = (posA[nB] - posA[nB-1]) // 2.
        # And so on for posA[nB+1]...
        
        # Total merges M = sum(M_j) for all required gap reductions.
        
        # The shifts are determined by the first piece.
        # Net shift of first piece = posB[0] - posA[0].
        # Let S be the net shift.
        # S = (Right Shifts) - (Left Shifts) + (Right Moves from Merges) - (Left Moves from Merges).
        # This is complex.
        
        # Alternative: The answer is max( |posA[0] - posB[0]|, sum(M_j) )? No.
        # It is known that the answer is the maximum of the number of shifts needed and the number of merges needed?
        # No, they are additive? No, one op is either shift or merge.
        # So Total Ops = Shifts + Merges.
        # But we can interleave them.
        # Actually, the minimum number of operations is:
        # K = max( |posA[0] - posB[0]|, sum(M_j) )? No.
        
        # Let's use the property:
        # K >= |posA[0] - posB[0]| is not true because merges move pieces.
        # However, K must satisfy:
        # 1. K >= sum(M_j) because each merge op reduces one gap by 2, and we need sum(M_j) reductions.
        # 2. K >= |posA[0] - posB[0]|? No.
        
        # Correct formula:
        # The minimum number of operations is the maximum of:
        # - The number of merges required.
        # - The number of shifts required to align the first piece, adjusted for merges?
        
        # Let's calculate M_j for all j.
        merges = 0
        for j in range(nB - 1):
            gapA = posA[j+1] - posA[j]
            gapB = posB[j+1] - posB[j]
            if gapA < gapB or (gapA - gapB) % 2 != 0:
                possible = False
                break
            merges += (gapA - gapB) // 2
            
        if not possible:
            results.append("-1")
            continue
            
        # Handle extra pieces in A
        if nB < nA:
            # The last mapped piece is posA[nB-1].
            # The next piece posA[nB] must merge into it.
            # Then posA[nB+1] merges into the result, etc.
            # Effectively, the gap between posA[nB-1] and posA[nB] must be closed.
            # Then posA[nB] and posA[nB+1] must be closed, etc.
            # But since they are all merging into one, we can just sum the merges.
            # Gap between posA[j] and posA[j+1] for j >= nB-1 must be reduced to 0.
            # But wait, if we merge posA[nB-1] and posA[nB], they become one piece.
            # Then that piece merges with posA[nB+1].
            # The cost is sum( (posA[j+1] - posA[j]) // 2 ) for j from nB-1 to nA-2.
            for j in range(nB - 1, nA - 1):
                gapA = posA[j+1] - posA[j]
                if gapA % 2 != 0:
                    possible = False
                    break
                merges += gapA // 2
                
        if not possible:
            results.append("-1")
            continue
            
        # Now, shifts.
        # The first piece moves from posA[0] to posB[0].
        # Let shift = posB[0] - posA[0].
        # Each merge operation moves the first piece?
        # If the pivot is to the right of the first piece, the first piece moves right (if pivot > posA[0]) or left (if pivot < posA[0]).
        # Since all pivots for merges are between pieces, and the first piece is at posA[0],
        # any pivot between posA[j] and posA[j+1] for j>=0 is to the right of posA[0].
        # So all merge operations move the first piece to the RIGHT by 1.
        # So, if we do M merges, the first piece moves M steps to the right due to merges.
        # Let S be the number of right shifts minus left shifts.
        # Final pos of first piece = posA[0] + M + S.
        # We want this to be posB[0].
        # So S = posB[0] - posA[0] - M.
        # The number of shift operations is |S|.
        # Total operations = M + |S| = M + |posB[0] - posA[0] - M|.
        
        shift_needed = posB[0] - posA[0] - merges
        total_ops = merges + abs(shift_needed)
        
        results.append(str(total_ops))

    print('\n'.join(results))

solve()