
## ideation
**Core difficulty:**  
We must decide the order of absorbing adjacent slimes. The condition `strength < current_strength / X` depends on the current strength, which grows as we absorb. Since absorption only increases strength, once a slime becomes absorbable it stays absorbable. The challenge is to find the maximum total reachable strength, which is equivalent to finding the set of cells that can eventually be absorbed in some order.

**Key observation:**  
If we always absorb the strongest currently absorbable adjacent slime, we increase our strength as fast as possible, which can only help unlock more slimes. This greedy choice is optimal because any other order would result in a smaller (or equal) strength at each step, never allowing more absorptions.

**Candidate approaches:**
1. **Greedy BFS with max‑heap:**  
   - Maintain current strength `cur`.  
   - Use a max‑heap of candidate slimes (neighbors of already visited cells).  
   - Repeatedly pop the strongest slime whose strength `< cur / X`.  
   - If condition holds, add its strength to `cur`, mark visited, push its four neighbors into the heap.  
   - Stop when no candidate satisfies the condition.
2. **Dijkstra‑like variant:**  
   Treat each cell as a node; we can only “enter” a cell if its slime strength is less than the strength we have when we arrive. Since strength only grows, a simple BFS with a priority queue on strength works.
3. **Brute force / DP:**  
   Not feasible due to exponential possibilities.

**Pitfalls:**
- The condition is **strictly less than** `cur / X`. Use integer division carefully: `cur // X` is the largest integer `≤ cur / X`. A slime with strength `s` is absorbable iff `s * X < cur` (to avoid floating point and overflow; `cur` and `s` can be up to `10^12`, product up to `10^21`, fits in Python int).
- We must push neighbors of a newly absorbed slime even if they are not yet absorbable; they become candidates for later.
- Grid size up to 500×500 = 250 000, heap operations are fine.
- Input values can be large; use Python’s arbitrary precision integers.

**Why greedy works:**  
Suppose we have two absorbable neighbors with strengths `a < b`. If we absorb `a` first, new strength = `cur + a`. If we absorb `b` first, new strength = `cur + b`. Since `b > a`, absorbing `b` first yields a larger strength, which cannot hurt future possibilities. By induction, always taking the maximum available strength is optimal.

## worker: Implement the greedy BFS with a max‑heap in a `sol
The algorithm uses a max‑heap (implemented via negative values in Python's min‑heap) to always consider the strongest neighboring slime first. When the strongest candidate does not satisfy `s * X < cur`, no other candidate can, because all others are weaker. At that point we stop. This greedy approach is optimal because absorbing a stronger slime first yields a larger current strength earlier, which can only help unlock more cells. The product `s * X` avoids floating‑point and handles values up to ~10^21, fitting Python's arbitrary‑precision integers.
