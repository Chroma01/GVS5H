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
            
        # Extract positions of '1's (0-indexed)
        posA = [i for i, c in enumerate(A) if c == '1']
        posB = [i for i, c in enumerate(B) if c == '1']
        
        countA = len(posA)
        countB = len(posB)
        
        # Condition 1: We must have at least as many pieces in A as in B
        # because each '1' in B requires at least one piece.
        if countA < countB:
            results.append("-1")
            continue
        
        # Condition 2: Check if the relative order allows mapping.
        # Since pieces are indistinguishable but order is preserved, 
        # the k-th piece in A must map to the k-th piece in B for k=1..countB.
        # The extra pieces (if any) can be placed in the gaps of B.
        # The minimum operations is determined by the maximum distance 
        # any of the first countB pieces need to travel.
        
        max_ops = 0
        possible = True
        
        # We map the first countB pieces of A to the pieces of B.
        # The remaining countA - countB pieces of A must end up in the gaps of B.
        # Since we can compress gaps arbitrarily (by choosing pivots between pieces),
        # the only constraint is that the "shape" of the first countB pieces 
        # must be compressible to the shape of B.
        # However, the problem statement implies we just need to reach a configuration 
        # where the set of occupied squares is exactly the set of indices where B has '1'.
        # This means the first countB pieces of A must end up at positions posB[0], posB[1], ..., posB[countB-1]
        # (possibly with some extra pieces inserted in between, but the "outer" pieces must align).
        # Actually, the optimal strategy is to align the k-th piece of A to the k-th piece of B.
        # The cost is the maximum number of steps any piece needs to move.
        # Since one operation moves all pieces towards a center, we can move pieces left and right simultaneously.
        # Thus, the number of operations is the maximum distance any piece needs to travel.
        
        for i in range(countB):
            dist = abs(posA[i] - posB[i])
            if dist > max_ops:
                max_ops = dist
        
        # Is it possible that we need more operations due to the extra pieces?
        # The extra pieces can be moved into the gaps. Since we can compress gaps,
        # we can always move extra pieces into the gaps without increasing the operations
        # beyond what is needed for the main pieces, provided the gaps are large enough.
        # But wait, if the gaps in A are smaller than in B, we cannot expand them.
        # However, the target B has specific gaps. We need to ensure that the gaps in A
        # are at least as large as the gaps in B?
        # No, the target configuration allows multiple pieces in one square.
        # The condition is just that the set of occupied squares is Q = {posB}.
        # This means we need to fit countA pieces into countB slots such that no slot is empty.
        # This is possible if countA >= countB.
        # The relative order of the pieces in A must be preserved.
        # So the k-th piece of A must end up at some slot j_k such that j_1 <= j_2 <= ... <= j_countA.
        # And the set {j_1, ..., j_countA} must be exactly Q.
        # This implies j_k = posB[k-1] for k=1..countB? No.
        # It implies that the first piece of A must be at posB[0], the last at posB[countB-1],
        # and the intermediate pieces must be distributed.
        # Actually, the minimal moves is determined by the "bounding box" of the first countB pieces.
        # The first piece of A must move to posB[0] (or earlier? No, must be at posB[0] to cover it).
        # Wait, if the first piece of A moves to posB[0], and the second to posB[1], etc.
        # Then the set of occupied squares is covered.
        # The extra pieces can be placed anywhere in the intervals [posB[i], posB[i+1]].
        # So the condition is simply that we can move the first countB pieces to posB[0]...posB[countB-1].
        # The cost is max(|posA[i] - posB[i]|).
        
        results.append(str(max_ops))

    print('\n'.join(results))

if __name__ == '__main__':
    solve()