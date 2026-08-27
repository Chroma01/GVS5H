import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
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
            P.append(int(next(iterator)))
            
        Q = []
        for _ in range(N):
            Q.append(int(next(iterator)))
            
    except StopIteration:
        return

    # Convert to 0-indexed
    X -= 1
    P = [p - 1 for p in P]
    Q = [q - 1 for q in Q]

    # Find the red cycle containing X
    red_cycle_nodes = set()
    curr = X
    while curr not in red_cycle_nodes:
        red_cycle_nodes.add(curr)
        curr = P[curr]
    
    # Find the blue cycle containing X
    blue_cycle_nodes = set()
    curr = X
    while curr not in blue_cycle_nodes:
        blue_cycle_nodes.add(curr)
        curr = Q[curr]

    # Check feasibility:
    # 1. All red balls must be in the red cycle of X
    # 2. All blue balls must be in the blue cycle of X
    
    # Check red balls
    for i in range(N):
        if A[i] > 0:
            if i not in red_cycle_nodes:
                print(-1)
                return

    # Check blue balls
    for i in range(N):
        if B[i] > 0:
            if i not in blue_cycle_nodes:
                print(-1)
                return

    # Calculate minimum operations
    # Set of boxes to operate on for red balls: red_cycle_nodes - {X}
    # Set of boxes to operate on for blue balls: blue_cycle_nodes - {X}
    # We need the union of these sets.
    
    boxes_to_operate = set()
    
    # If there is any red ball in the red cycle, we must operate on all non-X nodes in that cycle
    has_red_ball_in_cycle = False
    for i in red_cycle_nodes:
        if A[i] > 0:
            has_red_ball_in_cycle = True
            break
            
    if has_red_ball_in_cycle:
        for i in red_cycle_nodes:
            if i != X:
                boxes_to_operate.add(i)
                
    # If there is any blue ball in the blue cycle, we must operate on all non-X nodes in that cycle
    has_blue_ball_in_cycle = False
    for i in blue_cycle_nodes:
        if B[i] > 0:
            has_blue_ball_in_cycle = True
            break
            
    if has_blue_ball_in_cycle:
        for i in blue_cycle_nodes:
            if i != X:
                boxes_to_operate.add(i)
                
    print(len(boxes_to_operate))

if __name__ == '__main__':
    solve()