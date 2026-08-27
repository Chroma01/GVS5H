import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, X = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    P = list(map(int, input().split()))
    Q = list(map(int, input().split()))
    
    # Convert to 0-indexed
    X -= 1
    P = [p-1 for p in P]
    Q = [q-1 for q in Q]
    
    # Build inverse permutations
    invP = [0] * N
    for i in range(N):
        invP[P[i]] = i
    invQ = [0] * N
    for i in range(N):
        invQ[Q[i]] = i
    
    # Compute distances in P-cycle containing X
    distP = [-1] * N
    current = X
    d = 0
    while True:
        distP[current] = d
        prev = invP[current]
        if prev == X:
            break
        current = prev
        d += 1
    
    # Compute distances in Q-cycle containing X
    distQ = [-1] * N
    current = X
    d = 0
    while True:
        distQ[current] = d
        prev = invQ[current]
        if prev == X:
            break
        current = prev
        d += 1
    
    # Check for impossibility and compute max distances
    d_red = -1
    d_blue = -1
    total_red = 0
    total_blue = 0
    for i in range(N):
        if A[i] == 1:
            total_red += 1
            if distP[i] == -1:
                print(-1)
                return
            if distP[i] > d_red:
                d_red = distP[i]
        if B[i] == 1:
            total_blue += 1
            if distQ[i] == -1:
                print(-1)
                return
            if distQ[i] > d_blue:
                d_blue = distQ[i]
    
    # If no balls at all, answer is 0
    if total_red == 0 and total_blue == 0:
        print(0)
        return
    
    # Build the union of nodes that are in the red segment or blue segment
    S = set()
    for v in range(N):
        if (d_red != -1 and distP[v] != -1 and distP[v] <= d_red) or (d_blue != -1 and distQ[v] != -1 and distQ[v] <= d_blue):
            S.add(v)
    
    # The answer is the size of the union minus 1 (for X)
    ans = len(S) - 1
    print(ans)

if __name__ == "__main__":
    solve()