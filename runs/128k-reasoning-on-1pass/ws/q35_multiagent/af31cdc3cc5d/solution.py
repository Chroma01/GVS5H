import sys

def solve():
    # Read all input at once for efficiency
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    # Split into O and E based on original index parity
    # O: elements at odd indices (1, 3, 5...) -> 0, 2, 4... in 0-based indexing
    # E: elements at even indices (2, 4, 6...) -> 1, 3, 5... in 0-based indexing
    O = A[0::2]
    E = A[1::2]
    
    # Sort both lists to facilitate optimal pairing
    O.sort()
    E.sort()
    
    m = len(E)
    # len(O) is either m (if N is even) or m+1 (if N is odd)
    
    # Base score: pair O[0...m-1] with E[m-1...0]
    # This corresponds to discarding the largest element of O (if N is odd)
    # or pairing all elements (if N is even)
    current_score = 0
    for i in range(m):
        current_score += abs(O[i] - E[m-1-i])
        
    max_score = current_score
    
    # If N is odd, len(O) = m + 1. We can discard one element from O to maximize score.
    # We start with the assumption that we discarded O[m] (the largest element).
    # We then iteratively try discarding O[m-1], O[m-2], ..., O[0].
    if len(O) > m:
        # Recurrence relation derived from comparing Score(d) and Score(d+1):
        # Score(d) = Score(d+1) - |O[d] - E[m-1-d]| + |O[d+1] - E[m-d-1]|
        # We iterate d from m-1 down to 0.
        
        for d in range(m-1, -1, -1):
            # Calculate the change in score when moving from discarding O[d+1] to discarding O[d]
            term_sub = abs(O[d] - E[m-1-d])
            term_add = abs(O[d+1] - E[m-d-1])
            
            current_score = current_score - term_sub + term_add
            if current_score > max_score:
                max_score = current_score

    print(max_score)

if __name__ == '__main__':
    solve()