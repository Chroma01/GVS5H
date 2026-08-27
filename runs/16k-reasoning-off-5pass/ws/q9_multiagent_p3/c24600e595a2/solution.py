import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
        B = [int(next(iterator)) for _ in range(N)]
        C = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Calculate initial sum S0 = sum(A[i] * C[i])
    S0 = sum(a * c for a, c in zip(A, C))
    
    # Identify mismatches
    # D: costs where A[i] == 1 and B[i] == 0 (need to flip 1->0, delta = -C)
    # Z: costs where A[i] == 0 and B[i] == 1 (need to flip 0->1, delta = +C)
    D = []
    Z = []
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                D.append(C[i])
            else:
                Z.append(C[i])
    
    m = len(D) + len(Z)
    
    if m == 0:
        print(0)
        return

    # To minimize Total Cost = m*S0 + sum(weight * delta):
    # We want large negative deltas (from D) to have large weights (early in sequence).
    # We want small positive deltas (from Z) to have small weights (late in sequence).
    # Strategy:
    # 1. Process all D first (delta < 0). Sort D descending (largest C first -> largest negative delta).
    # 2. Process all Z second (delta > 0). Sort Z ascending (smallest C first -> smallest positive delta).
    #    This pairs the largest weights (which are at the start of the sequence) with the most negative deltas.
    #    And pairs the smallest weights (at the end of the sequence) with the largest positive deltas.
    
    D.sort(reverse=True)
    Z.sort()
    
    # Construct deltas: D (negative) then Z (positive)
    # D sorted desc -> deltas: -9, -6 (if D={6,9})
    # Z sorted asc -> deltas: 4 (if Z={4})
    # Sequence: -9, -6, 4.
    deltas = [-c for c in D] + [c for c in Z]
    
    total_cost = m * S0
    
    for k, delta in enumerate(deltas):
        # k is 0-based index. Operation index is k+1.
        # Weight is m - (k+1) + 1 = m - k.
        weight = m - k
        total_cost += weight * delta
        
    print(total_cost)

if __name__ == '__main__':
    solve()