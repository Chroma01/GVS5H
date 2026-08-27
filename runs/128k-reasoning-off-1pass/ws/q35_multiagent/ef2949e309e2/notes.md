
## ideation
The core difficulty lies in efficiently counting valid subsequences where a specific element is the unique middle mode. A brute-force approach checking all O(n^5) subsequences is infeasible. Instead, we iterate over each index `i` considering `nums[i]` as the middle element (index 2 of the subsequence). For each `i`, we need to choose 2 elements from the left (indices < i) and 2 from the right (indices > i).

The key insight is that for `nums[i]` to be the unique mode, its total frequency in the subsequence (1 + count_left + count_right) must be strictly greater than the frequency of any other element. Let `L` be the multiset of elements to the left and `R` be the multiset of elements to the right. We pick two elements from L and two from R.

A direct combinatorial counting is complex because the "other" elements' frequencies depend on what is picked. However, note that the maximum frequency of any other element in the subsequence can be at most 2 (since we only pick 2 from left and 2 from right, and an element can appear at most twice in the left part and twice in the right part, but actually, if an element x != nums[i] is picked, it can appear at most 2 times total in the subsequence: e.g., twice from left, or twice from right, or once from each).

Actually, the frequency of any element x != nums[i] in the subsequence is:
- count_left(x) + count_right(x), where count_left(x) is the number of times x appears in the chosen 2 left elements, and similarly for right.
Since we choose exactly 2 elements from left and 2 from right, the sum of frequencies of all other elements is 4. The frequency of nums[i] is 1 + a + b, where a is the count of nums[i] in the left 2, and b is the count of nums[i] in the right 2. a can be 0, 1, or 2; similarly for b.

For nums[i] to be the unique mode, we need:
1 + a + b > freq(x) for all x != nums[i].

Since the maximum possible freq(x) for x != nums[i] is 2 (because we only pick 2 elements from left and 2 from right, and if x appears in both left and right, it can appear at most once in each, so max 2; if it appears twice in left, then it can't appear in right if we are picking distinct indices? No, we are picking a subsequence, so indices are distinct, but values can repeat. Actually, if we pick two elements from left, they can be the same value. So freq(x) for x != nums[i] can be 2 (if both left picks are x, or both right picks are x, or one left and one right). It cannot be 3 or 4 because we only pick 2 from left and 2 from right.

So the condition simplifies to: 1 + a + b > 2, i.e., a + b >= 2.
Because if a + b >= 2, then freq(middle) >= 3, which is strictly greater than any other element's frequency (which is at most 2).

Therefore, the problem reduces to: for each index i (as middle), count the number of ways to choose 2 elements from left and 2 from right such that the number of times nums[i] appears in the chosen left 2 plus the number of times it appears in the chosen right 2 is at least 2.

Let:
- total_left = i (number of elements to the left)
- total_right = n - 1 - i (number of elements to the right)
- cL = frequency of nums[i] in nums[0:i]
- cR = frequency of nums[i] in nums[i+1:n]

We need to choose 2 from left and 2 from right. Let a be the number of nums[i] in the left 2, and b be the number of nums[i] in the right 2. We need a + b >= 2.

The total ways to choose 2 from left is C(total_left, 2). Similarly for right. But we need to break down by a and b.

For the left part:
- a = 0: choose 2 from the (total_left - cL) non-matching elements: C(total_left - cL, 2)
- a = 1: choose 1 from cL and 1 from (total_left - cL): cL * (total_left - cL)
- a = 2: choose 2 from cL: C(cL, 2)

Similarly for the right part with cR and total_right.

Then, the valid combinations are:
- a=2, b=0: ways_left[2] * ways_right[0]
- a=2, b=1: ways_left[2] * ways_right[1]
- a=2, b=2: ways_left[2] * ways_right[2]
- a=1, b=2: ways_left[1] * ways_right[2]
- a=0, b=2: ways_left[0] * ways_right[2]

Note: a=1, b=1 gives a+b=2, which is also valid? Yes, because 1+1+1=3 > 2. So we also need:
- a=1, b=1: ways_left[1] * ways_right[1]

So the valid cases are all (a,b) such that a+b>=2, i.e., (0,2), (1,1), (1,2), (2,0), (2,1), (2,2).

We can precompute the frequency arrays for left and right as we iterate i from 0 to n-1. We'll maintain a frequency map for the left part (initially empty) and for the right part (initially the entire array minus the current element). Then for each i, update the frequencies and compute the answer.

Complexity: O(n) iterations, each iteration does constant work (since the number of distinct values doesn't affect the inner loop, we just use the counts cL and cR). So overall O(n).

Pitfalls:
- Need to handle cases where total_left < 2 or total_right < 2: then no subsequence can be formed with that middle, so skip.
- The combinatorial functions C(n, k) should return 0 if n < k.
- Modulo arithmetic at each addition.

Let's implement accordingly.

## worker: (none)
The solution iterates over each element considering it as the middle element of a subsequence of size 5. For each middle element at index `i`, we need to choose 2 elements from the left (indices < i) and 2 from the right (indices > i).

The key insight is that for the middle element to be the unique mode, its frequency in the subsequence must be strictly greater than any other element's frequency. Since we only pick 2 elements from left and 2 from right, the maximum frequency of any other element is 2. Therefore, the middle element's frequency (1 + count in left 2 + count in right 2) must be at least 3, which means the sum of counts of the middle element in the chosen left 2 and right 2 must be at least 2.

We precompute frequencies and maintain left and right frequency maps as we iterate. For each middle element, we calculate the number of ways to choose 2 elements from left and right such that the middle element appears at least twice in total among those 4 elements. This is done by breaking down into cases based on how many times the middle element appears in the left 2 (a=0,1,2) and right 2 (b=0,1,2), and summing the valid combinations where a+b >= 2.

The algorithm runs in O(n) time since each iteration does constant work, and O(n) space for the frequency maps.
