1. Define a Segment Tree class that manages an array of size $500005$.
2. Initialize the tree such that `tree[i] = i`.
3. Implement `find_first(val)` to find the smallest index `i` where `tree[i] >= val`.
4. Implement `find_last(val)` to find the largest index `i` where `tree[i] <= val`.
5. Implement `range_add(l, r, val)` to add `val` to all elements in `[l, r]`.
6. Iterate through the $N$ contests, updating the tree based on the intervals.
7. Extract the final array from the tree.
8. Process the $Q$ queries and print the results.