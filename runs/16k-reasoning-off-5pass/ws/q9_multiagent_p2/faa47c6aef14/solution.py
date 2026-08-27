import sys

# Increase recursion depth just in case, though we will use iterative approaches
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
            
        P = []
        for _ in range(N):
            P.append(int(next(iterator)) - 1) # Convert to 0-indexed
            
        Q = []
        for _ in range(N):
            Q.append(int(next(iterator)) - 1) # Convert to 0-indexed
    except StopIteration:
        return

    # Identify the cycle containing X in P
    # Since P is a permutation, the graph is a collection of disjoint cycles.
    # A ball at i can reach X if and only if i is in the same cycle as X.
    cycle_P = set()
    curr = X
    while curr not in cycle_P:
        cycle_P.add(curr)
        curr = P[curr]
    
    # Identify the cycle containing X in Q
    cycle_Q = set()
    curr = X
    while curr not in cycle_Q:
        cycle_Q.add(curr)
        curr = Q[curr]
        
    # Check feasibility
    # All boxes with red balls (A[i] == 1) must be in cycle_P
    # All boxes with blue balls (B[i] == 1) must be in cycle_Q
    for i in range(N):
        if A[i] == 1 and i not in cycle_P:
            print("-1")
            return
        if B[i] == 1 and i not in cycle_Q:
            print("-1")
            return
            
    # If no balls at all, answer is 0
    has_balls = False
    for i in range(N):
        if A[i] == 1 or B[i] == 1:
            has_balls = True
            break
            
    if not has_balls:
        print("0")
        return

    # We need to find the set of boxes that will ever contain a ball (excluding X).
    # A box i needs to be operated on if it contains a ball.
    # Operating on i moves red ball to P[i] and blue ball to Q[i].
    # If P[i] != X, then P[i] will contain a red ball and must be operated on.
    # This propagates.
    # The set of boxes to operate on for red balls is the set of nodes reachable 
    # from initial red sources via edges u -> P[u], excluding X.
    # Similarly for blue balls and Q.
    
    # BFS for Red balls
    visited_red = set()
    queue_red = []
    
    # Initial sources for red balls
    for i in range(N):
        if A[i] == 1:
            if i != X:
                visited_red.add(i)
                queue_red.append(i)
            # If i == X, it's already at destination, no operation needed on X to move it out.
            
    # Process queue
    head = 0
    while head < len(queue_red):
        u = queue_red[head]
        head += 1
        
        v = P[u]
        if v != X and v not in visited_red:
            visited_red.add(v)
            queue_red.append(v)
            
    # BFS for Blue balls
    visited_blue = set()
    queue_blue = []
    
    for i in range(N):
        if B[i] == 1:
            if i != X:
                visited_blue.add(i)
                queue_blue.append(i)
                
    head = 0
    while head < len(queue_blue):
        u = queue_blue[head]
        head += 1
        
        v = Q[u]
        if v != X and v not in visited_blue:
            visited_blue.add(v)
            queue_blue.append(v)
            
    # The answer is the size of the union of visited_red and visited_blue
    # Because if a box is in either set, it must be operated on at least once.
    # Each box is operated on exactly once if it ever contains a ball (and is not X).
    
    ans = len(visited_red | visited_blue)
    print(ans)

if __name__ == '__main__':
    solve()