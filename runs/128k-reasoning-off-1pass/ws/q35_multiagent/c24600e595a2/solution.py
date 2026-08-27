import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    N = int(data[0])
    A = list(map(int, data[1:N+1]))
    B = list(map(int, data[N+1:2*N+1]))
    C = list(map(int, data[2*N+1:3*N+1]))
    
    # Calculate initial sum of C_i where A_i == 1
    S = 0
    for i in range(N):
        if A[i] == 1:
            S += C[i]
    
    # Identify indices that need to be flipped
    # D_10: A[i] == 1, B[i] == 0 (need to flip 1 -> 0)
    # D_01: A[i] == 0, B[i] == 1 (need to flip 0 -> 1)
    D_10 = []
    D_01 = []
    
    for i in range(N):
        if A[i] != B[i]:
            if A[i] == 1:
                D_10.append(C[i])
            else:
                D_01.append(C[i])
    
    # If no differences, cost is 0
    if not D_10 and not D_01:
        print(0)
        return
    
    # Sort D_10 in descending order of C_i
    D_10.sort(reverse=True)
    
    # Sort D_01 in ascending order of C_i
    D_01.sort()
    
    total_cost = 0
    
    # Phase 1: Perform all 1->0 flips
    # For each flip in D_10, cost is current S - C_i
    # After flip, S decreases by C_i
    current_S = S
    for c_val in D_10:
        cost = current_S - c_val
        total_cost += cost
        current_S -= c_val
    
    # Phase 2: Perform all 0->1 flips
    # For each flip in D_01, cost is current S + C_i
    # After flip, S increases by C_i
    for c_val in D_01:
        cost = current_S + c_val
        total_cost += cost
        current_S += c_val
    
    print(total_cost)

if __name__ == '__main__':
    solve()