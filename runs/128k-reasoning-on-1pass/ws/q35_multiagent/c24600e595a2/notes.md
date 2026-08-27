
## ideation
```python
import sys

def solve():
    # Read all input from stdin efficiently
    # The input format is:
    # N
    # A_1 ... A_N
    # B_1 ... B_N
    # C_1 ... C_N
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

    # Calculate initial weight of A
    # The cost of an operation is the sum of C_k for all k where A_k is 1.
    # Let's call this sum the "current weight".
    current_weight = 0
    for i in range(N):
        if A[i] == 1:
            current_weight += C[i]
    
    # Identify required flips to transform A to B.
    # We only need to flip bits where A[i] != B[i].
    # list1: costs for flipping 1 -> 0 (indices where A[i]=1, B[i]=0)
    # list0: costs for flipping 0 -> 1 (indices where A[i]=0, B[i]=1)
    list1 = []
    list0 = []
    
    for i in range(N):
        if A[i] == 1 and B[i] == 0:
            list1.append(C[i])
        elif A[i] == 0 and B[i] == 1:
            list0.append(C[i])
    
    # Strategy to minimize total cost:
    # The cost of an operation is the weight of the state AFTER the flip.
    # Flipping 1 -> 0 reduces the weight by C[i].
    # Flipping 0 -> 1 increases the weight by C[i].
    # To minimize the sum of weights (costs), we want the weight to be as low as possible
    # during the operations.
    # 1. We should perform all 1 -> 0 flips before any 0 -> 1 flips. 
    #    This is because 1 -> 0 flips reduce the weight, lowering the cost for subsequent operations.
    #    0 -> 1 flips increase the weight, raising the cost.
    # 2. Among 1 -> 0 flips, we should perform larger reductions first.
    #    This is because reducing the weight early keeps the weight low for more subsequent steps.
    #    So, sort list1 in descending order.
    # 3. Among 0 -> 1 flips, we should perform smaller increases first.
    #    This is because we want to increase the weight as slowly as possible after it has been minimized.
    #    So, sort list0 in ascending order.
    
    list1.sort(reverse=True)
    list0.sort()
    
    total_cost = 0
    
    # Perform 1 -> 0 flips
    # Each flip reduces current_weight by C[i]
    # Cost incurred is the new current_weight
    for cost in list1:
        current_weight -= cost
        total_cost += current_weight
        
    # Perform 0 -> 1 flips
    # Each flip increases current_weight by C[i]
    # Cost incurred is the new current_weight
    for cost in list0:
        current_weight += cost
        total_cost += current_weight
        
    print(total_cost)

if __name__ == '__main__':
    solve()
```
