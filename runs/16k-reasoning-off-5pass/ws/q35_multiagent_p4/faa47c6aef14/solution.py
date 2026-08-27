import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    iterator = iter(data)
    N = int(next(iterator))
    X = int(next(iterator))
    
    A = [int(next(iterator)) for _ in range(N)]
    B = [int(next(iterator)) for _ in range(N)]
    P = [int(next(iterator)) for _ in range(N)]
    Q = [int(next(iterator)) for _ in range(N)]
    
    # Convert to 0-indexed internally for boxes 0 to N-1
    # X is given as 1-indexed, convert to 0-indexed
    X0 = X - 1
    
    # If no balls at all, answer is 0
    if all(a == 0 for a in A) and all(b == 0 for b in B):
        print(0)
        return
    
    # Build reverse graphs for red and blue
    # rev_red[i] contains list of j such that P[j] == i+1 (in 1-indexed) -> in 0-indexed: P[j] == i
    rev_red = [[] for _ in range(N)]
    for i in range(N):
        p_val = P[i] - 1  # 0-indexed target
        rev_red[p_val].append(i)
        
    rev_blue = [[] for _ in range(N)]
    for i in range(N):
        q_val = Q[i] - 1  # 0-indexed target
        rev_blue[q_val].append(i)
        
    # BFS from X0 in rev_red to get R_set: all nodes that can reach X0 in red graph
    R_set = set()
    queue = deque([X0])
    R_set.add(X0)
    while queue:
        node = queue.popleft()
        for neighbor in rev_red[node]:
            if neighbor not in R_set:
                R_set.add(neighbor)
                queue.append(neighbor)
                
    # BFS from X0 in rev_blue to get B_set
    B_set = set()
    queue = deque([X0])
    B_set.add(X0)
    while queue:
        node = queue.popleft()
        for neighbor in rev_blue[node]:
            if neighbor not in B_set:
                B_set.add(neighbor)
                queue.append(neighbor)
                
    # Check if all initial red balls can reach X0
    for i in range(N):
        if A[i] == 1:
            if i not in R_set:
                print(-1)
                return
                
    # Check if all initial blue balls can reach X0
    for i in range(N):
        if B[i] == 1:
            if i not in B_set:
                print(-1)
                return
                
    # Now, collect all boxes that need to be operated on (excluding X0)
    S = set()
    
    # For red balls
    for i in range(N):
        if A[i] == 1:
            j = i
            while j != X0:
                if j in S:
                    break
                S.add(j)
                j = P[j] - 1  # move to next box in red path (0-indexed)
                
    # For blue balls
    for i in range(N):
        if B[i] == 1:
            j = i
            while j != X0:
                if j in S:
                    break
                S.add(j)
                j = Q[j] - 1  # move to next box in blue path (0-indexed)
                
    print(len(S))

if __name__ == '__main__':
    main()