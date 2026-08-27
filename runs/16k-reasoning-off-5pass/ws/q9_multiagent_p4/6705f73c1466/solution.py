import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]

    # Collect indices of all '1's (0-indexed)
    ones_indices = [i for i, char in enumerate(s) if char == '1']
    
    # If there are no 1s, cost is 0 (though problem guarantees at least one 1)
    if not ones_indices:
        print(0)
        return

    # Calculate the transformed list: diffs[i] = ones_indices[i] - i
    # This transforms the problem to finding a target position 'l' that minimizes sum(|diffs[i] - l|)
    # The i-th '1' (in sorted order) will move to position l + i.
    # The cost is |ones_indices[i] - (l + i)| = |(ones_indices[i] - i) - l|.
    diffs = [ones_indices[i] - i for i in range(len(ones_indices))]
    
    # The optimal 'l' is the median of the diffs array.
    # Sorting takes O(K log K) where K is the number of 1s.
    diffs.sort()
    k = len(diffs)
    median = diffs[k // 2]
    
    # Calculate the total cost (sum of absolute differences from the median)
    total_ops = sum(abs(x - median) for x in diffs)
    
    print(total_ops)

if __name__ == '__main__':
    solve()