import sys

def solve():
    input = sys.stdin.readline
    N, X = map(int, input().split())
    A = [0] + list(map(int, input().split()))
    B = [0] + list(map(int, input().split()))
    P = [0] + list(map(int, input().split()))
    Q = [0] + list(map(int, input().split()))
    
    needed = [False] * (N + 1)
    
    # Process red balls
    # Find cycle containing X in permutation P
    cycle_red = []
    cur = X
    while True:
        cycle_red.append(cur)
        cur = P[cur]
        if cur == X:
            break
    in_cycle_red = set(cycle_red)
    
    # Check if all red balls are in the cycle containing X
    for i in range(1, N + 1):
        if A[i] == 1 and i not in in_cycle_red:
            print(-1)
            return
    
    # Build inverse permutation for P
    P_inv = [0] * (N + 1)
    for i in range(1, N + 1):
        P_inv[P[i]] = i
    
    # Traverse cycle in reverse direction (against the permutation)
    # and find the farthest box with a red ball
    reverse_red = [X]
    cur = X
    max_step = 0
    while True:
        cur = P_inv[cur]
        if cur == X:
            break
        reverse_red.append(cur)
        if A[cur] == 1:
            max_step = len(reverse_red) - 1  # 1-indexed position in reverse list
    
    # Mark boxes that must be picked for red
    for i in range(1, max_step + 1):
        needed[reverse_red[i]] = True
    
    # Process blue balls (same logic with Q and B)
    cycle_blue = []
    cur = X
    while True:
        cycle_blue.append(cur)
        cur = Q[cur]
        if cur == X:
            break
    in_cycle_blue = set(cycle_blue)
    
    for i in range(1, N + 1):
        if B[i] == 1 and i not in in_cycle_blue:
            print(-1)
            return
    
    Q_inv = [0] * (N + 1)
    for i in range(1, N + 1):
        Q_inv[Q[i]] = i
    
    reverse_blue = [X]
    cur = X
    max_step = 0
    while True:
        cur = Q_inv[cur]
        if cur == X:
            break
        reverse_blue.append(cur)
        if B[cur] == 1:
            max_step = len(reverse_blue) - 1
    
    for i in range(1, max_step + 1):
        needed[reverse_blue[i]] = True
    
    # Count distinct boxes that need to be picked (excluding X)
    ans = sum(needed[i] for i in range(1, N + 1) if i != X)
    print(ans)

if __name__ == "__main__":
    solve()