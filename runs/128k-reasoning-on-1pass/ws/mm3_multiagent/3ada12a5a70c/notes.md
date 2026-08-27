
## ideation
The Manhattan distance between any two points on the boundary of an axis‑aligned square equals the circular distance on the perimeter of length \(C = 4\cdot\text{side}\).  
If we map each boundary point to its position along the perimeter (starting at \((0,0)\) and moving clockwise), the distance between two points with perimeter coordinates \(t_i, t_j\) is \(\min(|t_i-t_j|,\,C-|t_i-t_j|)\).

Thus the problem becomes:  
*Given \(n\) points on a circle of circumference \(C\), choose \(k\) of them to maximize the minimum circular distance between any two chosen points.*

This is a classic “max‑min distance on a circle” problem.  
We binary‑search the answer \(D\). For a fixed \(D\) we need to know whether we can pick \(k\) points with pairwise circular distance at least \(D\).

**Feasibility check for a given \(D\):**
1. A necessary condition is \(k\cdot D \le C\); otherwise impossible.
2. Sort the points by their perimeter coordinate \(t\).
3. Duplicate the list with an offset \(+C\) to handle wrap‑around (each physical point appears at most once in an interval of length \(C\)).
4. For each index \(i\) in the extended array, pre‑compute the first index \(j>i\) with \(t_j-t_i \ge D\). This can be done in \(O(n)\) with a two‑pointer sweep.
5. Try every possible starting point \(i\) (the first selected point). From \(i\) follow the pre‑computed “next” pointers greedily; each step must stay inside the interval \([i,\,i+n)\). After picking \(k\) points, verify the wrap‑around gap: the distance from the last chosen point back to the start must be at least \(D\), i.e. \(t_{\text{last}}-t_i \le C-D\).
6. If any start works, \(D\) is feasible.

The greedy choice (always taking the earliest possible next point) is optimal: it leaves the maximum remaining space for further points. If greedy fails the wrap condition for a start, no other selection with that start can succeed.

**Binary search:**
- Range: \([0, C]\).
- Use the standard “upper‑mid” pattern to find the largest feasible \(D\).

**Complexities:**
- Sorting: \(O(n\log n)\).
- Each feasibility test: \(O(n + n\cdot k) = O(nk)\) (since \(k\le 25\)), with the two‑pointer pre‑computation \(O(n)\).
- Binary search: \(O(\log C)\) tests (\(\le 32\) steps for \(C\le 4\cdot10^9\)).
- Total: \(O(n\log n + nk\log C)\) – well within limits for \(n\le15000\).

**Pitfalls:**
- Correct mapping of boundary points to perimeter coordinates (handle corners explicitly).
- Ensure the extended array respects wrap‑around and prevents picking the same physical point twice.
- The necessary condition \(k\cdot D \le C\) prunes large \(D\) quickly.
- Use integer arithmetic; the answer is an integer.

## worker: Implement the feasibility check function that, giv
The Manhattan distance between any two points on the boundary of an axis‑aligned square equals the length of the shorter arc along the perimeter.  By mapping each point to its clockwise distance from \((0,0)\) we obtain a set of positions on a circle of circumference \(C = 4\cdot\text{side}\).  The problem then becomes the classic “max‑min distance on a circle” problem.

A binary search on the answer \(D\) is performed.  For a fixed \(D\) we test feasibility with a greedy construction on a duplicated array of perimeter coordinates (to handle wrap‑around).  The greedy algorithm always picks the earliest possible next point; if it fails for a given start, no other selection with that start can work, making the test optimal.  The necessary condition \(k\cdot D \le C\) quickly prunes large values of \(D\).

Complexities: sorting \(O(n\log n)\); each feasibility check builds the “next” array in \(O(n)\) and then simulates at most \(k\) steps for each of the \(n\) starts, i.e. \(O(nk)\).  Binary search adds a factor of \(\log C\) (≤ 32).  With \(n\le 15000\) and \(k\le 25\) this easily meets the limits.
