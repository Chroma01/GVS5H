The mochi are given in non‑decreasing order.  
We need the maximum number of disjoint pairs \((a,b)\) with \(a\le b/2\).  
If we always match the smallest still‑unused mochi (the “top”) with the **smallest possible** larger mochi that satisfies the condition, we never waste a larger bottom that could be needed later.  

Greedy two‑pointer works:
* pointer `i` scans the array from left to right as the candidate top.
* pointer `j` always points to the smallest index that can serve as a bottom for the current `i`.  
  It moves forward only, never backward.
* For each `i` we advance `j` until `j>i` and `A[j] ≥ 2·A[i]`.  
  If such a `j` exists, we pair `i` with `j`, increase the answer, and move `j` one step further (the bottom is now used).  
  If `j` reaches the end, no more pairs are possible.

This runs in \(O(N)\) time and \(O(1)\) extra memory, easily handling \(N\le5\cdot10^5\).