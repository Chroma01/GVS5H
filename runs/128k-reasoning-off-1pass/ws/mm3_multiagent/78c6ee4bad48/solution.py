import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N = int(input())
    X = list(map(int, input().split()))
    
    total = sum(X)
    
    # Find initial violations: indices i where X[i] + X[i+3] < X[i+1] + X[i+2]
    violated = deque()
    for i in range(N - 3):
        if X[i] + X[i+3] < X[i+1] + X[i+2]:
            violated.append(i)
    
    # Process violations. Each operation at index i:
    # - Replaces X[i+1], X[i+2] with X[i]+X[i+3]-X[i+2], X[i]+X[i+3]-X[i+1]
    # - Changes total sum by 2*(X[i]+X[i+3]-X[i+1]-X[i+2]) < 0
    # - May create violations at i-1 and i+1
    
    max_ops = 5 * N + 100  # Safety bound; actual ops are O(N)
    ops = 0
    
    while violated and ops < max_ops:
        ops += 1
        i = violated.popleft()
        
        if i < 0 or i > N - 4:
            continue
        
        a, b, c, d = X[i], X[i+1], X[i+2], X[i+3]
        if a + d >= b + c:
            continue  # No longer a violation
        
        # Apply the operation
        new_b = a + d - c
        new_c = a + d - b
        total += 2 * (a + d - b - c)
        X[i+1] = new_b
        X[i+2] = new_c
        
        # Check left neighbor i-1: involves X[i-1], X[i], X[i+1], X[i+2]
        if i - 1 >= 0:
            if X[i-1] + X[i+2] < X[i] + X[i+1]:
                violated.append(i - 1)
        
        # Check right neighbor i+1: involves X[i+1], X[i+2], X[i+3], X[i+4]
        if i + 1 <= N - 4:
            if X[i+1] + X[i+4] < X[i+2] + X[i+3]:
                violated.append(i + 1)
    
    print(total)

solve()