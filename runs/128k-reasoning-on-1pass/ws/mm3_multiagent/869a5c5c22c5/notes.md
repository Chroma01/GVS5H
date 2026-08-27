
## ideation
The board is huge (10⁹×10⁹) so the only real constraints come from the movement rules.  
* A red move changes the colour of the square (flips parity of r + c), a blue move keeps it.  
* After going once around the required cycle the colour must be restored, therefore the number of red moves **R** must be even.  
* When **R = 0** all moves are diagonal; the diagonal‑move graph is bipartite, so any cycle has even length. Hence **B** must be even as well.

These two parity conditions are also sufficient.  
The task reduces to constructing, for every feasible pair (R,B), a simple closed walk on the grid that uses exactly R orthogonal steps and B diagonal steps, each step moving to a distinct square (the squares of the walk are the piece positions).

Candidate constructions:
1. **Parallelogram** – a rightward segment (w red steps), a down‑right segment (h blue steps), a leftward segment (w red steps) and an up‑left segment (h blue steps). Gives R = 2w, B = 2h. Works for all even R and even B.
2. **Rectangle (B = 0)** – a height‑2 rectangle using only red steps.
3. **B = 1** – a “right‑down‑left‑up‑left” shape with one diagonal closing edge.
4. **Pure blue cycle (R = 0, B even)** – a diagonal rectangle (or the 2‑cycle (1,1)↔(2,2) for B = 2) that uses only diagonal steps.
5. **Detour** – replace one red right step `(x,y)→(x,y+1)` by a diagonal up‑right step `(x,y)→(x‑1,y+1)` followed by a down step `(x‑1,y+1)→(x,y+1)`. This adds exactly one blue move without breaking simplicity, allowing to turn an even‑B construction into an odd‑B one (for B ≥ 3).

All pieces are placed in the order of the walk, and the required “i‑th piece can move to (i+1)‑th piece” is satisfied because consecutive vertices are adjacent by a legal move.

Pitfalls to watch for:
* Ensure the walk never revisits a square (simplicity). The detour introduces a new square, the other constructions are simple by design.
* Keep coordinates inside 1…10⁹ – the constructions use rows and columns ≤ 2·10⁵, far below the limit.
* Handle edge cases: R = 2, B = 0; R = 0, B = 2; B = 1; large B odd.
* The total number of pieces over all test cases ≤ 2·10⁵, so linear‑time per test case is fine.

## worker: finalize
The solution uses a constructive approach based on parity constraints:
- A red move flips the colour of a square, a blue move does not; therefore the number of red pieces **R** must be even.
- When **R = 0**, only diagonal moves are used and the diagonal‑move graph is bipartite, so **B** must also be even.
These conditions are also sufficient.  
The algorithm builds explicit cycles for every feasible case:

* **R even, B = 0** – a 2 × (R/2) rectangle.
* **R even, B = 1** – a “right‑down‑left‑up‑left’’ shape.
* **R even, B even** – a parallelogram (right, down‑right, left, up‑left).
* **R even, B odd (≥3)** – start with the parallelogram for the even part **B‑1** and apply one *detour* (replace a right step by a diagonal up‑right step and a down step) to add the extra blue move.
* **R = 0, B even** – a diagonal rectangle (or the 2‑cycle for B = 2).

All constructed paths are simple, coordinates stay within 1…10⁹, and the total size over all test cases is at most 2·10⁵, giving an overall O(Σ(R+B)) time and memory.
