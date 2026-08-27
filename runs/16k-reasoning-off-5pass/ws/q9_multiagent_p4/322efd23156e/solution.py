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
    except StopIteration:
        return

    # Separate items by vitamin type
    # Each item is (amount, cost)
    items1 = []
    items2 = []
    items3 = []

    for _ in range(N):
        v = int(next(iterator))
        a = int(next(iterator))
        c = int(next(iterator))
        if v == 1:
            items1.append((a, c))
        elif v == 2:
            items2.append((a, c))
        else:
            items3.append((a, c))

    # Function to find min cost to get at least 'target' amount of vitamin
    # using a list of (amount, cost) items.
    def min_cost_for_target(items, target):
        if target == 0:
            return 0
        
        # dp[i] = min cost to get exactly i amount (capped at target)
        # Initialize with infinity
        INF = float('inf')
        dp = [INF] * (target + 1)
        dp[0] = 0
        
        for amount, cost in items:
            # Iterate backwards to avoid using the same item multiple times for the same state
            # We only care about reaching 'target' or more, so we cap index at 'target'
            for j in range(target, -1, -1):
                if dp[j] == INF:
                    continue
                
                new_val = min(j + amount, target)
                if dp[j] + cost < dp[new_val]:
                    dp[new_val] = dp[j] + cost
        
        return dp[target]

    # Maximum possible k is N // 3 because we need at least k items for each of the 3 types
    max_k = N // 3
    
    # Iterate k from max_k down to 0
    for k in range(max_k, -1, -1):
        cost1 = min_cost_for_target(items1, k)
        cost2 = min_cost_for_target(items2, k)
        cost3 = min_cost_for_target(items3, k)
        
        if cost1 != float('inf') and cost2 != float('inf') and cost3 != float('inf'):
            if cost1 + cost2 + cost3 <= X:
                print(k)
                return

if __name__ == '__main__':
    solve()