We need the minimum number of operations (adjacent swaps + prefix deletions of equal values) to delete the whole array.

Observation: each prefix deletion removes a block of identical elements at the front. Adjacent swaps let us reorder elements to bring equal elements together at the front.

We can think greedily: we want to bring equal elements together as much as possible. The optimal strategy is to repeatedly take the longest prefix of equal elements (after swaps) and delete it, possibly inserting the current element at a different position via swaps. 

After analysis, the problem reduces to a stack-like DP:
We process the array left to right. Maintain a stack where each element is (value, count of consecutive equal elements currently at front of the remaining array after some swaps). When we see a new element v:
- If stack top has the same value, increment its count.
- Else push a new block with count 1.
Then pop the top two blocks if they have the same value (because we can bring the lower block up to the top and merge with the current top via swaps costing the lower block's size). The total number of operations is sum of (counts of all blocks that get popped) because each time a block is merged into the one above, we need that many swaps to bring it to the front. We add the total sum of sizes of merged blocks to the answer.

This yields an O(N) solution per test case.