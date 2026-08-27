import sys

def solve():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = data[1].strip()
    L = len(A)
    # dp0[i], dp1[i] for each node in current layer
    # Start with leaves
    dp0 = []
    dp1 = []
    for ch in A:
        if ch == '0':
            dp0.append(0)
            dp1.append(1)
        else:
            dp0.append(1)
            dp1.append(0)
    
    # Build up layer by layer
    while len(dp0) > 1:
        new_dp0 = []
        new_dp1 = []
        for i in range(0, len(dp0), 3):
            c0 = [dp0[i], dp0[i+1], dp0[i+2]]
            c1 = [dp1[i], dp1[i+1], dp1[i+2]]
            # For node = 0: sum of cost_to_0 minus max(cost_to_0 - cost_to_1)
            sum0 = c0[0] + c0[1] + c0[2]
            diff0 = [c0[j] - c1[j] for j in range(3)]
            node0 = sum0 - max(diff0)
            # For node = 1: sum of cost_to_1 minus max(cost_to_1 - cost_to_0)
            sum1 = c1[0] + c1[1] + c1[2]
            diff1 = [c1[j] - c0[j] for j in range(3)]
            node1 = sum1 - max(diff1)
            new_dp0.append(node0)
            new_dp1.append(node1)
        dp0 = new_dp0
        dp1 = new_dp1
    
    # Determine current root value
    # The current root value is the one with cost 0
    if dp0[0] == 0:
        current = 0
    else:
        current = 1
    
    if current == 0:
        print(dp1[0])
    else:
        print(dp0[0])

solve()