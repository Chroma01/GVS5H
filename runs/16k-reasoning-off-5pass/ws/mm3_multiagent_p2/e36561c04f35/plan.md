The sequence of operations allowed is: swap any adjacent pair, or delete a prefix consisting of equal elements. We need the minimum number of operations to empty the array.

Key observation: The only way to delete elements is to bring equal elements to the front and delete them as a prefix. So we can think of this as repeatedly "collecting" equal values and removing them.

Strategy: Greedy from left to right. Maintain a stack where each element is a pair (value, count of how many of that value we've seen consecutively after processing). For each new element `x`:
- If stack is empty, push `(x, 0)`.
- If top of stack has value `x`, push `(x, 0)` (start a new group of this value).
- Else (top has different value), we need to "merge" the previous groups. If the stack has at least 2 groups below the top, pop the top (cost: 1 swap) and merge it into the group below (increment its count by 1). If stack has only 1 group, pop it and discard (we cannot merge it, so it will be deleted later? Wait, we need to be careful).

Actually, the well-known solution for this type of problem (similar to AtCoder problems) uses a greedy with a stack:
- Process array from left to right.
- Maintain a stack of values. For each element `x`:
  - If stack is empty or top != x, push `x`.
  - Else (top == x), we can "cancel" two consecutive equal values: pop the top (this costs 1 operation: swap the x below with this x, making them adjacent, then... actually the standard trick is: increment a counter for this value, and when counter reaches 2, we can effectively "remove" them).

Let me think more carefully. The standard solution:
- Use a stack. For each element `x`:
  - If stack is not empty and top == x, increment a counter for this value (or pop twice when count reaches 2).
  - Else push `x`.
- The answer is related to the number of "cancellations".

Actually, looking at this problem, I recall it's from AtCoder. The solution is:
- Process left to right. Maintain a stack.
- For each element `x`:
  - If stack is empty or stack[-1] != x: push `x`.
  - Else (stack[-1] == x): we need to handle the pair. Increment the count of consecutive `x`s at the top. When the count reaches 2, pop the top (this simulates using one swap to bring the next `x` adjacent, then deleting the prefix of two `x`s? No...).

Let me reconsider. The operation 2 deletes a prefix of equal elements. So if we have `x x x`, we can delete all 3 in one operation. But we might need swaps to bring elements together.

The optimal strategy: We want to delete elements in groups. The cost is the number of swaps needed plus the number of delete operations. But the relationship is: to delete a group of `k` equal elements that are not adjacent, we need `k-1` swaps to make them adjacent, then 1 delete. But actually, swaps can be interleaved.

A cleaner view: Consider the array as we process it. We maintain a stack. When we see `x`:
- If the top of stack is `x`, we have a choice: either leave it (push another `x`? no, it's equal so we can merge). Actually, the standard greedy: 
  - If top == x, then we have a run of `x`s. We want to delete them. The cost of deleting a run of length `k` of value `x` is 1 (the delete operation), but we might have needed swaps before to bring them together.
  - If top != x, we push `x` (meaning we start a new block).

But this doesn't account for swaps between different values. When we have `a b a` on the stack, we can swap the `b` and `a` (1 operation) to get `a a b`, then delete the `a a` (1 operation), then we have `b` left.

So the algorithm:
- Process left to right with a stack.
- For each new element `x`:
  - While stack is not empty and top == x: 
    - Actually, we should track the count of the top value.
  - If stack is empty or top != x: push `x`.
  - Else (top == x): we have at least one `x` on top. We want to "merge" this new `x` with the block. If the block has count `c`, after processing the new `x`, the block now has `c+1` elements. We can think of this as: the new `x` can be swapped down to the block (cost 1 swap per element between them), then the block size increases. But to minimize, we should delete as soon as possible? No, we want to minimize total operations.

Wait, the key insight: This problem is equivalent to: we have a string. We can swap adjacent characters. We can delete a prefix if all characters in the prefix are the same. Find minimum operations to delete the string.

I recall the solution: The answer is the number of "segments" in the sequence after removing some structure. Actually, let's think small:
- N=1: A=[x]. We can delete it: 1 op.
- N=2: [x,x]: delete prefix: 1 op.
- N=2: [x,y]: swap to [y,x], then delete: 2 ops. Or swap to [x,y]? No, we must delete prefix of equal. [x,y] cannot delete prefix unless x=y. So we must swap: [y,x], then delete y: 2 ops.
- N=3: [x,y,x]: swap positions 2,3: [x,x,y], then delete first 2: 2 ops total. Or: swap 1,2: [y,x,x], delete first 1? No, first is y alone, not a prefix of equal? Actually, "all the values from the 1st through i-th are equal". So for i=1, always true (single element). So we can always delete the first element alone! That's important.

Oh! I missed that: we can delete a prefix of length 1, which is always a prefix of equal elements (trivially). So we can always delete the first element in 1 operation. That changes everything.

So the problem becomes: we can delete the first element at cost 1, or swap any adjacent pair at cost 1. We want to empty the array.

With the ability to delete the first element, the problem is: arrange deletions and swaps to minimize total operations.

Observation: Deleting the first element is always available. So if we do nothing else, we need N operations (delete one by one). But we can save by bringing equal elements together and deleting a block.

Actually, the optimal strategy: We want to find a sequence of operations. This is similar to: we have a string, we can delete the first character at cost 1, or swap adjacent at cost 1. We want to delete the string.

This is equivalent to: we process from left to right, maintaining a stack. When we encounter a character:
- If the stack top equals it, we can "cancel" them (they will eventually be deleted together with some swaps).
- If not, we push it.

But with the ability to delete the first element at any time, the greedy is:
- Maintain a stack. For each element `x`:
  - If stack is empty or top != x, push `x`.
  - Else (top == x), we can pop the top (this represents: we will use 1 swap to bring this `x` next to the previous `x`, then delete the pair). Wait, but we might have a run of many `x`s.

Actually, the known solution for this problem (AtCoder ABC 233 H? or similar) is:
- Process from left to right with a stack.
- For each `x`:
  - If stack is empty or stack[-1] != x: push `x`.
  - Else: pop the stack (this corresponds to 1 swap + 1 delete of the pair? No, the count of operations is not simply the number of pops).

Let me look for the pattern. The answer is the number of elements in the stack after processing. No, that's for a different problem.

Let me derive from scratch.
Let f(i) be the minimum operations to make the prefix A[1..i] empty.
When we add A[i+1], we can:
- Swap it leftwards until it meets an equal element, then delete the block.
- Or delete previous elements first.

The structure: We process the array. At any point, we can choose to "close" a block of equal elements at the left end. The cost to close a block of size k of value v is: we need to bring k-1 elements next to it via swaps, then 1 delete. But if the block is already formed, it's 1 delete.

This is getting complex. Let me search my memory: This is AtCoder ABC 233 Ex? No.

Actually, I think this is "Sequence" from some contest. The solution: 
- Use a stack. For each element, if it equals the top, pop (with a counter to handle multiple). If not, push.
- The answer is the number of pushes minus the number of effective pops? No.

Let's simulate sample 1: A = [1,1,2,1,2]
Stack: []
1: top empty -> push [1]
1: top == 1 -> pop? If we pop, stack = []. Count = 1? 
2: top empty -> push [2]
1: top != 1 -> push [1]
2: top == 2 -> pop? Stack = [1]. 
Final stack size = 1. But answer is 3.

That doesn't match. Maybe we count operations: 
- Each push is 1 op (delete the single element? No).
- Each pop is 1 op (swap to merge).

Let's count operations with the stack method for sample 1:
Process: 1(push,1), 1(pop,1 -> means 1 swap to merge, then delete? Actually the pair [1,1] is deleted). So 1 push + 1 pop = 2 ops to handle two 1s. But we didn't delete them yet, we just merged them conceptually.
Then 2(push,1 op: this 2 will eventually be deleted alone or merged).
Then 1: top is 2 != 1, push. Now stack has [2,1].
Then 2: top is 1 != 2, push. Stack [2,1,2].
Now we need to resolve. The remaining stack has alternating. We need 2 swaps to make it [2,2,1], then 1 delete of the two 2s, then 1 delete of the 1. That's 4 more ops, total 6. But answer is 3.

So that's not right.

Let me reconsider the operations. The key is: we can delete a prefix of equal elements of any length i. So if we have [1,1,1], we delete all 3 in 1 op. If we have [2,1,1], we can swap to [1,2,1] (1 op), swap to [1,1,2] (1 op), delete first two (1 op), leaving [2] which we delete (1 op). Total 4.

For the sample 1: [1,1,2,1,2]
Optimal: swap 3,4 to get [1,1,1,2,2], delete first 3 (1 op), delete first 2 (1 op). Total 2 swaps + 2 deletes? Wait, sample says 3 operations: 1 swap + 2 deletes. Let's check: [1,1,2,1,2] -> swap pos 3 and 4: [1,1,1,2,2]. Then delete pos 1-3: [2,2]. Then delete pos 1-2: []. That's 1 swap + 2 deletes = 3 ops. Yes.

So the stack approach should yield 3.
Process with a stack that tracks "blocks" and when we can delete:
- We want to minimize: #swaps + #deletes.
- Each delete removes a prefix of equal elements.
- A swap can bring equal elements together.

Observation: The sequence of operations can be seen as building a parse tree. Each delete corresponds to a node that combines some number of children.

Actually, I think the solution is related to the number of "runs" after some processing. Let me think differently.

Consider the reverse: We start from empty and build the array by inserting elements at the front (reverse of delete prefix) and swapping. But that's complex.

Another angle: The minimum number of operations is N minus the maximum number of "savings" we get by grouping equal elements. Each time we delete a block of k equal elements, we save k-1 operations compared to deleting one by one. But we need swaps to bring them together.

If we never swap, we need N operations (delete one by one). If we swap to group, we might save.
- To group two equal elements that are separated by d elements, we need at least d swaps? Not exactly, because we can delete intermediate elements.

For example, to bring the first and third 1 together in [1,1,2,1], we have two 1s adjacent already, third 1 is separated by one 2. We can delete the first 1 (1 op), then we have [1,2,1], swap to [1,1,2] (1 op), delete the two 1s (1 op), delete the 2 (1 op). Total 4. Original length 4, no savings. But if we instead: swap 3,4 to get [1,1,1,2], delete first three (1 op), delete 2 (1 op). Total 3. So we saved 1.

The savings come from having multiple equal elements that we can delete together.

The maximum number of elements we can delete in one operation is the maximum frequency of any value that appears in a "connected" way? No, any value anywhere, but we need swaps to bring them together, and each swap costs 1, but we might delete intermediate elements for free (just 1 op each) which might be better than swapping over them.

So the problem is: choose a sequence of operations to minimize total cost.

This is a known problem. I recall the solution uses a stack and the answer is the number of elements in the stack after processing all elements, plus something. Let me look at sample 3: [1,2,1,2,1,2,1,2,1,2,1] length 11, answer 8.
If we do: pair up the 1s and 2s. There are six 1s and five 2s. We can delete pairs? With the stack method:
Process: 1(push), 2(push, diff), 1(top=2 diff, push), 2(top=1 diff, push), 1(top=2 diff, push), 2(top=1 diff, push), 1(top=2 diff, push), 2(top=1 diff, push), 1(top=2 diff, push), 2(top=1 diff, push), 1(top=2 diff, push).
Stack has 11 elements? That's not 8.

If we do: when we see 1 after 2, we can pop the 2? That would give stack of 1s? Let's try:
1: push [1]
2: push [1,2]
1: top=2 != 1, but we can swap? Actually, we can process: if top != x, we might still be able to do something.
If we maintain a multiset and when we see x and top is y != x, we can "cancel" x and y? That would give: 1,2,1 -> cancel 2 and 1, stack [1]. Then 2: push [1,2]. Then 1: top=2, cancel -> [1]. Then 2: push [1,2]. Then 1: cancel -> [1]. Then 2: push [1,2]. Then 1: cancel -> [1]. Final stack [1], size 1. But answer is 8, not 1.

I'm missing something. Let me read the problem again. "Let K be the length of A just before the operation. Choose i such that all the values from the 1st through i-th are equal, and delete them."
So we can only delete a prefix. We cannot delete arbitrary positions. So my cancellation idea is wrong because we cannot just delete the 2 if it's not at the prefix.

So the stack should represent the suffix of the array after some operations. Actually, we process from left to right, and at each point we can choose to delete the prefix (which removes the leftmost part). So the stack represents the remaining array after we've decided to delete some prefixes.

Specifically, we read the array. We can at any point delete the current prefix. So we have a choice: when we read a new element, we can either:
- Append it to the current sequence (if we haven't deleted everything before it).
- But actually, the array is fixed initially. We can interleave swaps and deletes.

Better: Think of the process as building a sequence of blocks. We can swap adjacent elements. This is like the bubble sort distance but with deletions.

Actually, the minimal number of operations is: N - (number of times we can "save" by deleting a block > 1). But each block > 1 requires the elements to be brought together.

Wait, there's a known result: For this type of problem, the answer is the number of elements in the "reduced" sequence where we remove adjacent duplicates? No.

Let me try a different approach. Let's think of the array as we process it from left to right, maintaining a stack of values that are "pending". When we read `x`:
- If the stack is empty, push `x`.
- If the stack top is `x`, we can "absorb" this `x` into the top (it will be deleted with the top). This costs 0 extra operations? But we need swaps to bring them together if they weren't adjacent. However, if we process left to right and the stack represents the sequence after deleting some prefixes, then when we see `x` and top is `x`, they are adjacent in the remaining sequence? Not necessarily.

Actually, here's the correct interpretation from similar problems: We process left to right. The stack represents the sequence of different values that will be deleted in separate operations. When we encounter a value, if it's the same as the top, we can merge it (meaning we will delete it together with the top), which costs 0 additional operations (the swap was already accounted for or is free because we'll delete the top block which includes this new element). If it's different, we push it.

But we also need to account for the fact that we can only delete a prefix. So if we have stack [a, b, a], the top two a's can be merged (since they are at the end, we can swap them to be adjacent? No, they are already adjacent at the end of the remaining sequence? Actually, if the remaining sequence is a, b, a, then the suffix a, a can be made adjacent? They are already adjacent! So we can delete the two a's at the end? But the delete operation only works on the prefix, not suffix. We can only delete from the front.

So the stack should be built in reverse? Or we process from right to left? Because we can only delete prefixes, it's natural to think of the array backwards: we are building the array by adding to the left (reverse of deleting from the right? No, we delete from the left).

Actually, if we reverse the array, then deleting the prefix of the reversed array corresponds to deleting the suffix of the original array. But we can only delete prefix in the original, so in the reversed array we can only delete suffix. That's symmetric.

Maybe we should think: At any point, we have a sequence. We can delete a prefix. So we can think of peeling off prefixes. The operation of swapping is symmetric.

The key insight: The minimum number of operations is exactly the number of "segments" in the sequence after removing all elements that can be paired? No.

Let me search for "minimum operations swap adjacent delete prefix equal" in my knowledge. This is AtCoder ABC 240 Ex? Or maybe it's from a recent contest.

Actually, I think this is "Sequence" from AtCoder Beginner Contest 233? No.

Let me try to derive the algorithm from the constraints. The sum of N is 2*10^5, so O(N log N) or O(N) per test case is fine.

I recall a solution: Process from left to right. Maintain a stack. For each element x:
- If the stack has at least 2 elements and the top two are equal? No.
- If the top of the stack is equal to x, we increment a counter for that value.
- If the counter reaches 2, we pop the stack (this represents that we can delete a pair of x's using the existing structure).
- If the top is not equal to x, we push x.

And the answer is the number of pushes plus something.

Wait, I found a similar problem: "Make It Empty" or something. The answer is the number of elements in the stack after processing. Let's test with sample 1: [1,1,2,1,2]
- 1: push [1]
- 1: top==1, counter for 1 becomes 2, so pop -> [].
- 2: push [2]
- 1: top==2 !=1, push [2,1]
- 2: top==1 !=2, push [2,1,2]
Final stack size = 3. But answer is 3. Yes! Sample 1 gives 3.

Sample 2: [4,2,1,3]
- 4: push [4]
- 2: push [4,2]
- 1: push [4,2,1]
- 3: push [4,2,1,3]
Stack size = 4. Answer is 4. Yes!

Sample 3: [1,2,1,2,1,2,1,2,1,2,1]
- 1: push [1]
- 2: push [1,2]
- 1: top==2 !=1, push [1,2,1]
- 2: push [1,2,1,2]
- 1: push [1,2,1,2,1]
- 2: push [1,2,1,2,1,2]
- 1: push [1,2,1,2,1,2,1]
- 2: push [1,2,1,2,1,2,1,2]
- 1: push [1,2,1,2,1,2,1,2,1]
- 2: push [...,2]
- 1: push [...,1]
Stack size = 11. But answer is 8. So my rule is wrong.

Hmm. For sample 3, the stack rule gave 11, but answer is 8. So we need to pop sometimes.

Maybe the rule is: if top == x, we don't push, but we also don't pop unless we have a pair? Let's modify:
- 1: push [1], count(1)=1
- 2: push [2], count(2)=1
- 1: top=2 !=1. But we can do something: if we have a block of 1s, we can merge? Actually, if top != x, but the value below top is x, we can pop top (swap the top with the new x? But new x is coming from the right, we can swap it leftwards).
In [1,2,1], we have the third element 1. The stack represents the remaining array [1,2,1]? Actually, if we process left to right and haven't done any operations yet, the remaining is the whole prefix. But we might have deleted some prefixes already.

Alternative: The stack represents the "differences" that will be deleted in separate operations. When we see x and top is y != x, we can "cancel" y and x (they will be deleted separately, but we save an operation because we can pair them? No).

Let's look at sample 3 again. Answer 8. N=11. So we save 3 operations.
The array has 1s and 2s alternating. We can group: 1,2,1,2,1,2,1,2,1,2,1.
One way: Delete the first 1 (1 op). Then we have 2,1,2,1,2,1,2,1,2,1. Swap 1,2 to get 1,2,2,1,2,1,2,1,2,1? This is messy.

Actually, optimal: We can pair the 1s and 2s. There are six 1s and five 2s. We can delete three pairs of (1,2) using swaps? Or we can form blocks.

Another way: Bring all 1s to the front: 
Original: 1 2 1 2 1 2 1 2 1 2 1
Swap 2,3: 1 1 2 2 1 2 1 2 1 2 (1 op)
Swap 4,5: 1 1 2 1 2 2 1 2 1 2 (2 ops)
Swap 5,6: already 2,2
Swap 7,8: 1 1 2 1 2 2 1 1 2 2 (3 ops)
Now we have: 1 1 2 1 2 2 1 1 2 2 1
Continue... this might take many swaps.

But answer is 8, which is less than 11. So we save 3.
Maybe: Delete single elements at the ends? 
Delete the first 1: (2,1,2,1,2,1,2,1,2,1) -> 1 op
Delete the first 2: (1,2,1,2,1,2,1,2,1) -> 2 ops
Delete the first 1: 3 ops
Delete the first 2: 4 ops
...
Delete until we have (1,1) left: 
After 5 deletes: (1,1) -> 5 ops
Delete both: 6 ops. Total 6? But there are 11 elements, deleting one by one is 11. We saved 5? But answer is 8. So 11-8=3, not 5.

So deleting one by one but with some swaps is better.

Actually, with the one-by-one deletion, we do 11 ops. To save 3, we need to form 4 groups? Each group of size k saves k-1 ops. To save 3, we need groups that sum to 4 extra elements (i.e., total size 7 in groups, meaning 4 groups of size 2? No, saving 3 means we have 3 groups of size 2 instead of 6 single deletes, saving 3 ops. So we form 3 pairs. That would be 8 ops total (3 swaps to pair them up? No, pairing requires swaps).

The answer 8 suggests: 5 deletes + 3 swaps? Or 4 deletes + 4 swaps? 8 total.

I think the correct algorithm is:
- Process from left to right.
- Maintain a stack of values.
- For each x:
  - If stack is not empty and top == x: pop the stack (this means we can delete these two x's together, costing 1 swap to bring them adjacent? Actually, the pop represents that we have used 1 operation to handle these two elements).
  - Else: push x.
- The answer is the size of the stack.

Let's test this on sample 1: [1,1,2,1,2]
- 1: push [1]
- 1: top==1, pop -> []
- 2: push [2]
- 1: top==2, push [2,1]
- 2: top==1, push [2,1,2]
Stack size = 3. Answer 3. Yes!

Sample 2: [4,2,1,3]
- 4: push [4]
- 2: push [4,2]
- 1: push [4,2,1]
- 3: push [4,2,1,3]
Stack size = 4. Answer 4. Yes!

Sample 3: [1,2,1,2,1,2,1,2,1,2,1]
- 1: push [1]
- 2: top!=1, push [1,2]
- 1: top!=1? top is 2. So push [1,2,1]
- 2: push [1,2,1,2]
- 1: push [1,2,1,2,1]
- 2: push [...,2]
- 1: push [...,1]
- 2: push [...,2]
- 1: push [...,1]
- 2: push [...,2]
- 1: push [...,1]
Stack size = 11. But answer is 8.

So simple pop on equal doesn't work for sample 3.

Maybe: when top == x, we don't always pop. We only pop if we have a pair? But we pop immediately.
Wait, in sample 3, we never have two consecutive 1s or two consecutive 2s in the input, so we never pop. So we need a different rule.

What if we pop when the top two elements are equal? In sample 3, we never have two equal adjacent in the stack, so we never pop. So that's not it.

Another idea: We can "merge" non-adjacent equal elements in the stack. For example, in [1,2,1], the two 1s are separated by one 2. We can swap the 2 and the last 1 to get [1,1,2], then delete the two 1s. This costs 1 swap + 1 delete for the pair, then we have [2] left, which we delete. Total 3 ops for 3 elements. But without merging, we'd push 1,2,1 and have stack [1,2,1], size 3, meaning 3 ops. Same.

But for the full sample 3, if we can merge across the 2s:
[1,2,1,2,1] -> we can merge the 1s: 1 swap to get [1,1,2,2,1]? Not exactly.
Actually, from [1,2,1,2,1]:
- Swap 2,3: [1,1,2,2,1] (1 op)
- Delete first two 1s: [2,2,1] (2 ops)
- Delete first two 2s: [1] (3 ops)
- Delete the 1: (4 ops)
Total 4 ops for 5 elements. Average < 1.

So the stack should allow us to cancel a 2 when we see a 1 if there's a 1 below? 
Rule: When we see x, if the stack is not empty and the top is y != x, we check the element below the top. If that is x, then we can pop the top (y) and not push x? Let's try.

For [1,2,1]:
- 1: push [1]
- 2: push [1,2]
- 1: top=2 !=1, below top is 1 ==1. So we pop the top (2) and do not push 1. Stack becomes [1]. This represents: we used 1 swap to bring the 1 next to the previous 1, then we will delete them together. So the two 1s are merged, and the 2 is left for later. But the 2 was popped, meaning it will be deleted separately? Actually, popping the 2 means we have "used" it in a swap, so it will be deleted alone later. But we didn't push the new 1, meaning it merged with the bottom 1. So net effect: stack [1] (the merged pair counted as one). This is 1 operation (the swap) to handle the three elements? Then later we delete the 1-block and the 2 separately? Total: 1 swap + 1 delete (1s) + 1 delete (2) = 3 ops. Correct.

For [1,2,1,2,1,2,1,2,1,2,1]:
- 1: push [1] -> [1]
- 2: push -> [1,2]
- 1: top=2, below=1. Pop 2, don't push. -> [1]
- 2: push -> [1,2]
- 1: top=2, below=1. Pop 2. -> [1]
- 2: push -> [1,2]
- 1: pop 2. -> [1]
- 2: push -> [1,2]
- 1: pop 2. -> [1]
- 2: push -> [1,2]
- 1: pop 2. -> [1]
Final stack: [1]. Size 1. But answer is 8. So this gives 1, which is too small. We are undercounting because we are not accounting for the deletes of the 2s that were popped. Each popped 2 needs to be deleted, which is 1 op each. And the final 1 needs to be deleted. So total ops = number of elements in stack + number of pops? 
In this case: stack size 1, number of pops = 5 (the 2s were popped). Total = 6? But answer is 8.

Maybe the formula is: stack size + number of times we did a "merge" (which is 1 op). In the above, we had 5 merges (each pop of a 2 when below is 1). So 1 (final stack) + 5 (merges) = 6. Still not 8.

Let's trace the actual operations for sample 3 to get 8:
One possible sequence:
Start: 1 2 1 2 1 2 1 2 1 2 1
1. Delete first element (1): [2 1 2 1 2 1 2 1 2 1] (op 1)
2. Delete first (2): [1 2 1 2 1 2 1 2 1] (op 2)
3. Delete first (1): [2 1 2 1 2 1 2 1] (op 3)
4. Delete first (2): [1 2 1 2 1 2 1] (op 4)
5. Delete first (1): [2 1 2 1 2 1] (op 5)
6. Delete first (2): [1 2 1 2 1] (op 6)
7. Delete first (1): [2 1 2 1] (op 7)
8. Delete first (2): [1 2 1] (op 8)
9. Delete first (1): [2 1] (op 9)
10. Delete first (2): [1] (op 10)
11. Delete first (1): [] (op 11)
This is 11, no savings.

But we can swap:
1. Swap 2,3: [1 1 2 2 1 2 1 2 1 2 1] (op 1)
2. Delete first two (1,1): [2 2 1 2 1 2 1 2 1 2 1] (op 2)
3. Delete first two (2,2): [1 2 1 2 1 2 1 2 1 2] (op 3)
4. Swap 2,3: [1 1 2 2 1 2 1 2 1 2] (op 4)
5. Delete first two: [2 2 1 2 1 2 1 2] (op 5)
6. Delete first two: [1 2 1 2 1 2] (op 6)
7. Swap 2,3: [1 1 2 2 1 2] (op 7)
8. Delete first two: [2 2 1] (op 8)
9. Delete first two: [1] (op 9)
10. Delete first: [] (op 10)
This is 10.

Better:
1. Swap 2,3: [1 1 2 2 1 2 1 2 1 2 1]
2. Swap 5,6: [1 1 2 2 2 1 2 1 2 1 2] wait, 1 2 2 1 2 1...
Let's be systematic.
Actually, the answer 8 is given. So there is a way with 8 ops.

I found a solution online in my memory: This problem is from AtCoder, and the solution is to use a stack and the answer is the number of elements in the stack after processing, where the rule is:
- If the stack is not empty and the top element is the same as the current element, then we pop the top (and we increment a counter or something).
- But we only pop if the count of that element in the stack is odd? Or something.

Let's try: For sample 3, we have 1,2,1,2,1,2,1,2,1,2,1.
If we process and pop when we see the same as top, we get stack of size 11 (no pops).
If we pop when the top two are equal (which never happens here), we get 11.

What if we process and we are allowed to "match" the current element with any element in the stack? Like, if we see 1 and there is a 1 in the stack, we can match it and remove both, but we need to account for the elements in between.

The correct algorithm is: Maintain a stack. For each x:
- If stack is not empty and top == x: pop the stack. (This means we can delete these two x's together with 1 operation: swap to make them adjacent, then delete the prefix? But wait, if they are not adjacent, we need more swaps.)

Actually, the trick is that we can always "bring" the current element to the top of the stack in 1 operation (swap with the top), and if the top equals x, we can delete the pair in 1 operation. So the cost is 1 per element, except when we can pair them, we save 1.

But that's not right because we might need to bring x past multiple elements.

Wait, I think I got it. The stack represents the sequence of "unmatched" elements. When we read x:
- If the top of the stack is x, we can "cancel" the top with x: pop the stack. This uses 1 operation (the swap to bring x next to the top, and then they are both at the front? Actually, if the stack top is x, and we have a new x, we can swap the new x with the top? No, the new x is at the end of the current array. We can swap it leftwards until it hits the previous x, then we have two x's at the front, then we delete them. The number of swaps needed is the number of elements between them. But those elements are exactly the elements in the stack! So if the stack has k elements, we need k swaps to bring the new x to the front? No, the stack elements are at the front. The new x is at the end. To bring it to the front, we need to swap it left past all elements in the stack and the previous occurrences? 

This is getting complicated. Let me look for the standard solution.
The standard solution for this problem (I believe it's AtCoder ABC 240 Ex or similar) is:
- Process the array from left to right.
- Maintain a stack (or vector) and a counter for the current value.
- For each element x:
  - If the stack is empty or the top value is not x, push x onto the stack.
  - Else (top is x):
    - Increment the count of x.
    - If the count of x is 2, pop the stack and reset the count? Or something.
- The answer is the size of the stack.

But sample 3 has no consecutive equal elements, so the stack would never pop, giving size 11.

Unless... we process from right to left? Or we group differently.

Another idea: The answer is the number of "segments" in the array after removing all elements that appear an even number of times? No.

Let's think about the problem as: we want to partition the array into segments that can be deleted together. A segment can be deleted together if it consists of equal elements (after some swaps). Actually, a segment is deleted by a delete operation, which requires the segment to be a prefix of equal elements. So after some swaps, we can make any multiset of equal elements become a prefix. But the swaps cost operations.

The optimal strategy is to use a greedy algorithm: always delete the smallest possible prefix that is "efficient". 

I recall now: This is "Make Them Empty" or "Sequence Operation". The solution is to use a stack and the answer is the number of elements in the stack after processing, where we pop when the top two elements are equal. But that only works for some cases.

Wait, I think I remember the exact problem. It's from AtCoder, and the solution is:
- Process from left to right.
- For each element, if it's the same as the previous element in the original array, we can group them? No.

Let me try to derive the answer for sample 3 manually to understand the pattern.
N=11, answer=8. So we have 3 "savings".
The array: 1 2 1 2 1 2 1 2 1 2 1
If we delete the first 1, we have 2 1 2 1 2 1 2 1 2 1 (length 10). 
If we then swap the first two: 1 2 2 1 2 1 2 1 2 1. 
Delete first 1: 2 2 1 2 1 2 1 2 1 (length 8).
Delete first two 2s: 1 2 1 2 1 2 1 (length 7).
This is getting messy.

Actually, I can write a brute force for small N to see the pattern, but I can't run code now. I need to reason.

Let's consider the inverse: building the array. We start with empty. We can:
- Insert a block of equal elements at the front (reverse of delete).
- Swap the first two elements (reverse of swap).

This is equivalent to: we can prepend any number of equal elements, and we can swap the first two elements. We want to build A in minimum operations.

With prepending equal elements: we can build the array in the reverse order by deciding when to "commit" to the next element.
When we prepend a block of k equal elements of value v, it costs 1 operation. When we swap the first two, it costs 1 operation.

This is like: we read A from right to left. We maintain a sequence. We can:
- If the sequence is empty, or the first element (leftmost) is not equal to the next needed element (from right), we can prepend a block of that element (cost 1).
- If the first element is equal to the next needed element, we can "merge" it: we need to remove the first element. How? We can swap the first two elements. If the second element is also equal, then after swap we have the same first element, and we can swap again? This is like we can "consume" the first element by swapping it with the second if the second is different? No.

Actually, the reverse process: we want to build A by adding to the left. We can add a block of equal elements (cost 1). We can also swap the first two elements (cost 1). But swapping the first two changes the order of the first two. So we can reorder the first two elements.

This is equivalent to: we have a deque. We can push_front a block (cost 1). We can swap the first two elements (cost 1). We want to build A in minimum operations.

Processing from right to left (building A backwards):
Let B be the reverse of A. We want to build B.
We process B from left to right (which is A from right to left).
We maintain a deque D.
For each element x in B:
- If D is empty or D[0] != x: push_front x (cost 1).
- Else (D[0] == x): we need to "use" the x at the front. We can swap the first two elements. If D has only one element, swapping does nothing, so we must push_front? Or if D has >=2 elements, we can swap D[0] and D[1]. If D[1] == x, then after swap we still have x at front, so we can "absorb" the new x? 
This is getting into the details of the reverse process.

Actually, there's a known result: The minimum number of operations equals the number of "runs" in the sequence after compressing adjacent duplicates, plus something. But sample 3 has 11 runs (all elements are different from neighbors), so that would give 11.

Another thought: The problem is equivalent to: we have a string. We can delete a prefix of identical characters, or swap adjacent. This is similar to the problem of sorting by swaps and deletions. The answer is the length of the string minus the length of the longest "even" subsequence? No.

I recall now: This is AtCoder ABC 240 Ex "Sequence Decoding"? No.

Let me search my memory for "swap adjacent delete prefix equal". This is AtCoder Grand Contest or Regular Contest. I think it's AGC 047 or something. The solution uses a stack and the answer is the size of the stack after processing, where we pop when the top element is equal to the current element, BUT we only pop if the element has appeared an even number of times? Or we use a parity bit.

For sample 3: 1,2,1,2,1,2,1,2,1,2,1
Count of 1 is 6 (even), 2 is 5 (odd).
If we process and pop on equal, we get 11. But if we only pop when the count of the current value is even, then:
- 1: push [1], count(1)=1 (odd)
- 2: push [1,2], count(2)=1 (odd)
- 1: count(1)=2 (even) -> pop? But top is 2, not 1. So we can't pop.
That doesn't work.

What if we pop when we see the same value as the second element from top?
- 1: push [1]
- 2: push [1,2]
- 1: second from top is 1. Pop the top (2) and don't push? Or pop the second?
Let's try: if x == second from top, we pop the top.
- 1: [1]
- 2: [1,2]
- 1: second is 1 == x. Pop top -> [1]
- 2: [1,2]
- 1: pop top -> [1]
- 2: [1,2]
- 1: pop top -> [1]
- 2: [1,2]
- 1: pop top -> [1]
- 2: [1,2]
- 1: pop top -> [1]
Final size 1. Not 8.

What if we count the number of "unmatched" elements? For sample 3, there are 6 ones and 5 twos. The minimum operations might be max(freq(1), freq(2)) * 2 - 1? No.

Let's think about the lower bound. Each operation can increase the number of "equal adjacencies" by at most 1 (swap) or decrease the length by k (delete). To delete all elements, we need to reduce the length to 0. Each delete reduces the length by at least 1. So we need at least ceil(N / max_delete_size) deletes. But max_delete_size can be up to N if all elements are equal. In the worst case (all distinct), max_delete_size is 1, so we need at least N deletes, but we can do it in N operations (delete one by one). So the answer is between N/2 and N? No, with swaps we can group elements, so we can have larger delete blocks.

Actually, the answer is always at most N (delete one by one). The savings come from grouping. Each swap can increase the size of a deletable block by 1? Not exactly.

I think I need to look up the solution structure. The problem is likely "Sequence" from AtCoder. The solution is:
- Use a stack.
- For each element x:
  - If the stack is not empty and the top is x, pop the stack and increment a counter (or just pop).
  - If the stack is not empty and the top is not x, push x.
  - If the stack is empty, push x.
- The answer is the size of the stack.

But we saw this gives 11 for sample 3. So maybe we also pop when x is not equal to top but x is equal to the second element? No, that gave 1.

What if we process from right to left with the same rule?
Sample 1 reversed: [2,1,2,1,1]
- 2: push [2]
- 1: push [2,1]
- 2: top=1 !=2, push [2,1,2]
- 1: top=2 !=1, push [2,1,2,1]
- 1: top=1 ==1, pop -> [2,1,2]
Size 3. Answer 3. Good.
Sample 2 reversed: [3,1,2,4]
- 3: push [3]
- 1: push [3,1]
- 2: push [3,1,2]
- 4: push [3,1,2,4]
Size 4. Answer 4. Good.
Sample 3 reversed: [1,2,1,2,1,2,1,2,1,2,1] (palindrome, same as original)
Size 11. Not 8.

So processing right to left with the same rule doesn't fix sample 3.

Maybe the rule is: we pop when the top is equal to x, AND we keep a separate count. If we have seen x twice in a row (in the stack), we pop. In sample 3, we never have two in a row, so we never pop. So that's not it.

Another idea: The answer is the number of "blocks" in the sequence after removing all elements that can be matched with a previous element of the same value, but with the constraint that the matching must be "non-crossing"? Like, we match equal elements and they annihilate? That would be like parentheses matching, but for any value.

If we match equal elements in a stack-like way (LIFO), we get: for each x, if top is x, pop; else push.
This is exactly the stack rule. For sample 3, it gives 11. So it's not LIFO matching.

What if we match greedily: for each x, we find the closest previous x and match them? 
Sample 3: 1 matches with the 1 at position 3, 2 matches with 2 at pos 4, 1 matches with 1 at pos 5, etc. The number of unmatched elements would be the last unmatched of each type? Actually, if we match each x with the previous x, we can think of the "first occurrence" as starting a block, and the second as closing it, etc. This is like a counter. The number of unmatched elements is the sum of (freq(x) mod 2) = (6 mod 2) + (5 mod 2) = 0 + 1 = 1. So answer would be 1 + number of blocks? No.

Wait, if we can pair up all but one 1, we have one 1 left. But we also need to delete the 2s. The 2s are odd, so one 2 left. But we can't have both left because they are interleaved. Actually, if we pair 1s and 2s in some way, the minimum number of elements left might be 1? But answer is 8, which is much larger than 1.

I think I'm confusing the number of operations with the number of elements left in the stack. The stack size might represent the number of operations, but we need to account for swaps.

Let's try to find the recurrence. Let dp[i] be the min ops to delete A[1..i]. 
When we add A[i+1] = x, we can:
- Delete A[1..i] first, then delete x: dp[i] + 1.
- Or, we can bring x to the front (cost i swaps), then delete the block of x's at the front. But we need to know how many x's are at the front after swaps.
- Or, we can swap x leftwards until it hits an x, then we have a block of x's of size 2, then we can delete the block and the prefix before it? This is complex.

Actually, the optimal strategy is to use a stack that represents the "unmatched" elements. When we see x:
- If the stack top is x, we can pop it (meaning we delete these two x's together). This costs 1 swap (to bring the new x to the stack top? No, the new x is already at the end. The stack represents the sequence after some deletions. When we append x, if the last element is x, we can delete the last two elements? But we can only delete the prefix, not the suffix. So if the stack represents the sequence, we can only delete from the left. So the stack should be built by adding to the left, i.e., we process from right to left.

Yes! Process from right to left. Maintain a stack. For each x (from right to left):
- If the stack top (which is the leftmost element of the remaining sequence) is x, we can "merge" them: pop the stack. This corresponds to: in the original array, these two x's will be deleted together. Since we are building from right to left, the rightmost x's are added first. When we add a new x on the left, if the leftmost of the current sequence is x, we can delete the pair with 1 operation? 
Let's test with sample 1: A=[1,1,2,1,2]. Right to left: x=2,1,2,1,1.
Stack: []
2: push [2]
1: top=2 !=1, push [2,1]
2: top=1 !=2, push [2,1,2]
1: top=2 !=1, push [2,1,2,1]
1: top=1 ==1, pop -> [2,1,2]
Size 3. Answer 3. Good.
Sample 2: [4,2,1,3] right to left: 3,1,2,4.
3: push [3]
1: push [3,1]
2: push [3,1,2]
4: push [3,1,2,4]
Size 4. Good.
Sample 3: [1,2,1,2,1,2,1,2,1,2,1] right to left: same.
1: push [1]
2: push [1,2]
1: top=2 !=1, push [1,2,1]
2: push [1,2,1,2]
1: push [1,2,1,2,1]
2: push [1,2,1,2,1,2]
1: push [1,2,1,2,1,2,1]
2: push [1,2,1,2,1,2,1,2]
1: push [1,2,1,2,1,2,1,2,1]
2: push [1,2,1,2,1,2,1,2,1,2]
1: top=2 !=1, push [1,2,1,2,1,2,1,2,1,2,1]
Size 11. Still 11.

So processing right to left with pop on equal gives 11 for sample 3.

But wait! In sample 3, when processing right to left, we never have top == x because the array is alternating. So we never pop. But the answer is 8, which is less than 11. So we must be able to pop sometimes even when top != x.

How? If we have ... x, y, x (from right to left, this is x, y, x), then when we process the leftmost x, the stack has [x, y]. The top is y != x. But we can swap the y and the new x? In the right-to-left processing, the stack represents the sequence built so far. When we add a new x to the left, we can "insert" it. If the sequence is x, y, we can swap the first two to get y, x, x. Then the first two are y, x, not equal. We can swap again? y, x, x -> swap first two: x, y, x. Then the first two are x, y. Not helpful.
But from x, y, x (left to right), we can swap the last two to get x, x, y, then delete the first two. So in the stack [x, y] and new x, we can merge the two x's by "swapping" the y out of the way. This costs 1 swap. So we should be able to pop the y and push the x? Or pop the y and not push x, meaning the two x's are merged and the y is left for later.

Let's try: when processing right to left, for each x:
- If stack is not empty and top == x: pop. (Merge with the previous x).
- Else if stack is not empty and second from top == x: pop the top (and maybe push x? Or just pop). This means we swap the top with the new x, merging the x's, and the top (y) is left for later.
- Else: push x.

Test on sample 3 right to left: 1,2,1,2,1,2,1,2,1,2,1
- 1: push [1]
- 2: top=1 !=2, second doesn't exist. Push [1,2]
- 1: top=2 !=1, second=1 ==1. Pop top -> [1]. (This represents: we had [1,2] and new 1. We swap to get [1,1,2], delete the two 1s, left with [2]. But wait, we popped the 2, so the 2 is gone? No, popping the top means we "used" the 2 in a swap, so it will be deleted later? Actually, the stack should represent the remaining elements. If we pop the 2, we are saying the 2 is no longer at the front, it's somewhere else? This is confusing.)

Let's track the actual remaining sequence. Process right to left, building the sequence by adding to the left. We want to minimize operations. Each "add to left" of a block of equal elements costs 1. Swapping the first two costs 1.
When we add x to the left of the current sequence S:
- If S is empty or S[0] != x, we can just prepend x. Cost 1.
- If S[0] == x, we can "merge": we prepend x, but then we have two x's at the front. We can delete the first two? But in the reverse, we can't delete; we can only add and swap. To merge, we can swap the first two. If S[0] == x and S[1] == x, swapping does nothing useful. If S[0] == x and S[1] != x, swapping gives S[1], x, x. Then we have two x's at the front? No, S[1] is now at the front. So swapping moves the x away. That doesn't help.
Wait, in the reverse, we want to build S. The forward operation is: delete prefix of equal elements. The reverse is: insert a block of equal elements at the front. But also, we can swap adjacent in forward, so reverse we can swap adjacent. But in the reverse, the array is being built from right to left, so we are adding elements to the left. The forward swap is swapping adjacent in the current array. In the reverse, the current array is being built, and we can swap any adjacent pair. So when we add a new element to the left, we can also perform swaps to rearrange the left part.

The cost to add x to the left and make it merge with an existing x at the front:
- If S[0] == x, we can just add x. Now we have x, x, ... We can then delete the first two in forward, which corresponds to... what in reverse? In reverse, we are building. We don't delete. So the condition for merging is: if S[0] == x, we can "absorb" the new x into the first block for free? But that would mean cost 0, which is not right because in forward we need to bring the x to the front (cost of swaps) then delete (cost 1). But in forward, the x is at the end initially. Bringing it to the front costs swaps equal to the number of elements before it that we don't delete. This is complex.

Given the time, I think the correct solution is the one where the answer is the number of elements in the stack after processing left to right, with the rule that we pop when the top is equal to the current element, AND we also pop when the current element equals the element below the top? Or we use a frequency count.

I recall a problem "Make It Empty" where the answer is the number of distinct values or something. No.

Let me think about the problem as a graph or matching. Each delete operation removes a prefix of equal elements. This is equivalent to saying we can remove any set of elements that forms a prefix of some sequence obtained by swapping. But we can only swap adjacent, so the relative order of elements is preserved. So the only thing that changes is the positions.

So the final sequence of deletions corresponds to a partition of the array into "blocks" that are deleted in some order. But the blocks must be prefixes at the time of deletion.

Actually, there's a known theorem: The minimum number of operations to delete a string by deleting prefixes of equal characters and swapping adjacent characters is equal to the number of "segments" in the string after removing all characters that appear an even number of times? No.

Let's look at the answer for sample 3: 8. N=11. The array has 6 ones and 5 twos. 6+5=11. 8 = 11 - 3. 3 is the minimum number of pairs we can form? We can form 3 pairs of (1,2) or something.

Maybe the answer is: for each value, we can form floor(count/2) pairs, each pair saves 1 operation? Then savings = sum floor(count/2). For sample 3: floor(6/2)+floor(5/2) = 3+2=5. Then answer = 11-5=6. But answer is 8. So not that.

Maybe the answer is: N - (number of times we can merge) where merge is when we have two consecutive equal elements after some swaps. The maximum number of merges is limited by the structure.

Another approach: Use BFS or DP for small N to see the pattern. Since I can't run code, I need to deduce.

Let's try to find the solution online in my mind. I think this is AtCoder ABC 233 H? No, ABC 233 H is hard.
Maybe it's from Codeforces? "Sequence" problems are common.

I remember a solution: 
- Process the array from left to right.
- Maintain a stack of pairs (value, count).
- For each x:
  - If stack is not empty and top.value == x:
    - top.count += 1
    - If top.count == 2: pop the stack (this means we can delete these two with 1 operation? Actually, the count is the number of times we've seen this value consecutively in the stack? Or the number of blocks?).
  - Else:
    - Push (x, 1).
- The answer is the size of the stack.

Let's test on sample 1: [1,1,2,1,2]
- 1: push (1,1) -> [(1,1)]
- 1: top.value=1, count becomes 2. Pop -> [].
- 2: push (2,1) -> [(2,1)]
- 1: push (1,1) -> [(2,1), (1,1)]
- 2: push (2,1) -> [(2,1), (1,1), (2,1)]
Size 3. Answer 3. Good.
Sample 2: [4,2,1,3]
- 4: push
- 2: push
- 1: push
- 3: push
Size 4. Good.
Sample 3: [1,2,1,2,1,2,1,2,1,2,1]
- 1: push (1,1)
- 2: push (2,1)
- 1: top=2, push (1,1)
- 2: push (2,1)
- 1: push (1,1)
- 2: push (2,1)
- 1: push (1,1)
- 2: push (2,1)
- 1: push (1,1)
- 2: push (2,1)
- 1: push (1,1)
Size 11. Not 8.

So the count of 2 never happens because we never have two consecutive 1s or 2s. So the stack just grows.

What if we count the number of times we've seen the value, not consecutive in the stack? 
- For 1: count=1
- 2: count=1
- 1: count=2 -> pop the previous 1? But the stack has 1,2,1. We want to pop the 2? 
If we maintain a global count for each value, and when count becomes 2, we pop the stack and decrement? 
For sample 3:
- 1: push, count(1)=1
- 2: push, count(2)=1
- 1: count(1)=2. We can "merge" this 1 with the previous 1. But they are not adjacent. We need to remove the 2 between them. So we pop the 2. Stack: [1]. count(2) remains 1? But we used the 2. 
Then 2: push, count(2)=1 (or 2? It was 1, now becomes 2? No, the 2 is new).
This is getting messy.

I think I have it. The correct algorithm is:
- Process from left to right.
- Use a stack.
- For each element x:
  - If the stack is not empty and the top is x, pop the stack. (This represents deleting a pair of x's).
  - If the stack is not empty and the top is y != x, AND the element below the top (if exists) is x, then pop the top (y). This represents: we swap y and the new x (cost 1), making them x, x, y, then we can delete the two x's (cost 1), but we already accounted for the swap? Actually, the pop of y means we use 1 operation to "eliminate" y and merge the x's. The new x is not pushed, meaning it's part of the merged block.
  - If the stack is not empty and the top is y != x, and the second is not x, push x.
  - If the stack is empty, push x.
- The answer is the size of the stack.

Let's test this on sample 3:
- 1: push [1]
- 2: top=1 !=2, second doesn't exist. Push [1,2]
- 1: top=2 !=1, second=1 ==1. Pop top (2). Stack -> [1]. (This means: we used 1 op to merge the two 1's and eliminate the 2? But the 2 is gone, so we saved an op? The answer is stack size + number of such pops? Let's see.)
- 2: top=1 !=2, second doesn't exist. Push [1,2]
- 1: top=2, second=1. Pop top -> [1]
- 2: push [1,2]
- 1: pop top -> [1]
- 2: push [1,2]
- 1: pop top -> [1]
- 2: push [1,2]
- 1: pop top -> [1]
Final stack: [1]. Size 1. But answer is 8. So stack size is 1, but we did 5 pops. So total operations = size + pops? 1+5=6. Not 8.
Or total operations = size + 2*pops? 1+10=11. No.
Or total operations = 2*size - 1 + something? 

Maybe the answer is the number of elements in the stack plus the number of "levels" of nesting? I'm stuck.

Given the time constraint, I need to make a decision. I'll go with the algorithm that worked for the first two samples and see if there's a pattern. The first two samples are satisfied by:
- Process left to right.
- For each x, if stack is empty or top != x, push x.
- If top == x, pop the stack.
- Answer = size of stack.

For sample 3, this gives 11. But answer is 8. So this algorithm is wrong for sample 3. However, sample 3 is a very specific alternating case. Maybe the answer is indeed the stack size with a different rule.

Let me check if the answer for sample 3 could be 8 with a different interpretation. 1,2,1,2,1,2,1,2,1,2,1.
What if we process and pop when the top is x, and also when the top is not x but the new x can be swapped to match the second? 
Actually, the correct answer for this problem is known to be the number of "segments" after a certain compression. I recall a solution: 
- Group the array into segments of equal elements? No.
- Use a stack and maintain the "parity" of each value. 
Or: the answer is the number of elements in the stack after repeatedly removing adjacent equal elements. That's the stack rule we had.

Wait, I think I have it. The problem is from AtCoder, and it's called "Sequence" or "Make It Empty". The solution is:
- The answer is the number of elements in the array after removing all elements that appear an odd number of times? No.

Let's calculate the number of operations for sample 3 using the optimal strategy to see the pattern.
N=11, answer=8.
If we delete the first 1 (op 1), we have 10 elements: 2,1,2,1,2,1,2,1,2,1.
Now we have an alternating sequence of length 10 starting with 2.
If we swap the first two: 1,2,2,1,2,1,2,1,2,1 (op 2).
Delete the first 1: 2,2,1,2,1,2,1,2,1 (op 3).
Delete the first two 2s: 1,2,1,2,1,2,