1.  **Parse Input**: Read $T$ and each test case ($N, A, B$).
2.  **Preprocessing**: Identify the indices of '1's in strings $A$ and $B$. Let these be lists `posA` and `posB`.
3.  **Feasibility Check**: If the number of pieces in $A$ is less than the number of required pieces in $B$ (i.e., `len(posA) < len(posB)`), it's impossible to satisfy the condition because pieces cannot be created, only merged. Output -1.
4.  **Binary Search**: The minimum number of operations $L$ is monotonic. We binary search for $L$ in the range $[0, 2N]$.
5.  **Validation Function**: For a given $L$, check if a valid assignment exists:
    *   The operation implies a parity constraint: for any piece $x$ moving to target $b$, the displacement $|x-b|$ must have the same parity as $L$ (i.e., $(x-b) \equiv L \pmod 2$).
    *   We must assign pieces from `posA` to targets in `posB` in a monotonic order (preserving relative order) such that