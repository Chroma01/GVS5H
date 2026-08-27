import sys
from bisect import insort, bisect_left

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input().strip())
    A = list(map(int, input().split()))
    
    # The problem reduces to pairing each even-indexed element (0-indexed odd)
    # with an odd-indexed element (0-indexed even) in a non-crossing way.
    # The optimal strategy is a greedy algorithm:
    # Process the array left to right. Maintain a sorted list of "available"
    # odd-indexed elements. When we see an even-indexed element, pair it with
    # the odd that gives the maximum absolute difference (the closest in value).
    # This ensures the sum of |A_even - A_odd| is maximized.
    # The non-crossing property is satisfied automatically because we process
    # in order and always pair an even with a previously seen odd.
    
    available_odds = []  # sorted list of values of unmatched odd-indexed elements
    total_score = 0
    
    for i in range(N):
        val = A[i]
        if i % 2 == 0:  # 0-indexed even -> 1-indexed odd
            insort(available_odds, val)
        else:  # 0-indexed odd -> 1-indexed even
            if available_odds:
                # Find the odd that gives the maximum |val - odd|
                pos = bisect_left(available_odds, val)
                best_idx = -1
                best_diff = -1
                # Check the first element >= val
                if pos < len(available_odds):
                    diff = abs(val - available_odds[pos])
                    if diff > best_diff:
                        best_diff = diff
                        best_idx = pos
                # Check the last element < val
                if pos > 0:
                    diff = abs(val - available_odds[pos-1])
                    if diff > best_diff:
                        best_diff = diff
                        best_idx = pos-1
                # Pair with the best odd
                total_score += best_diff
                available_odds.pop(best_idx)
    
    print(total_score)

if __name__ == "__main__":
    solve()