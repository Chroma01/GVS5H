
## ideation
```python
import sys

def solve():
    # Read all input from standard input efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    # The first token is N
    n = int(input_data[0])
    
    # The rest of the tokens are the elements of A
    # Since N can be up to 5*10^5, we convert them to integers.
    # A is guaranteed to be sorted in ascending order.
    a = [int(x) for x in input_data[1:]]
    
    # We want to find the maximum number of pairs (top, bottom) such that top <= bottom / 2.
    # Since the array is sorted, we can use a greedy two-pointer approach.
    # The maximum number of pairs is at most N // 2.
    # Therefore, we can restrict the "top" mochi to the first half of the array
    # and the "bottom" mochi to the second half.
    
    left = 0
    right = n // 2
    count = 0
    
    # Iterate while both pointers are within valid ranges.
    # 'left' points to a candidate for the top mochi.
    # 'right' points to a candidate for the bottom mochi.
    while left < n // 2 and right < n:
        # Check the condition: a[left] <= a[right] / 2
        # To avoid floating point issues, we use multiplication: 2 * a[left] <= a[right]
        if 2 * a[left] <= a[right]:
            # Valid pair found
            count += 1
            left += 1
            right += 1
        else:
            # If the current bottom mochi is too small, move the right pointer
            # to try a larger bottom mochi.
            right += 1
            
    print(count)

if __name__ == '__main__':
    solve()
```

## worker: finalize
The problem asks for the maximum number of disjoint pairs $(A, B)$ from a sorted array such that $A \le B/2$. This is a classic greedy matching problem. Since the array is sorted, the optimal strategy is to pair the smallest available candidate for the top with the smallest available valid candidate for the bottom. This preserves larger values for potentially larger tops, maximizing the total count.

We can restrict potential tops to the first $N/2$ elements and potential bottoms to the last $N/2$ elements, as we can form at most $\lfloor N/2 \rfloor$ pairs. Using two pointers `left` (starting at 0) and `right` (starting at $N/2$), we check the condition $2 \cdot A[\text{left}] \le A[\text{right}]$. If true, we form a pair and advance both pointers. If false, $A[\text{right}]$ is too small to support $A[\text{left}]$, so we advance `right` to find a larger bottom. This runs in $O(N)$ time and $O(N)$ space, which is optimal for the given constraints ($N \le 5 \times 10^5$).
