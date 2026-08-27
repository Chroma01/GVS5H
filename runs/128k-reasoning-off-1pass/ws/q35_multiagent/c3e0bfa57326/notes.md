
## ideation
The problem asks for the number of distinct valid parenthesis sequences reachable from a given valid parenthesis sequence $S$ by repeatedly reversing contiguous valid parenthesis substrings (with the specific reversal definition that swaps `(` and `)`).

Key observations:
1.  **Operation Analysis**: The operation is defined on a substring $S[l..r]$ which is a valid parenthesis sequence. The reversal swaps `(` and `)` while reversing the order.
    *   Consider a primitive valid parenthesis sequence $P$. It has the form `(A)` where $A$ is a valid parenthesis sequence.
    *   Reversing $P$: The first char `(` becomes `)`, the last char `)` becomes `(`. The inner part $A$ is reversed and its parens swapped. Let $Rev(A)$ be the result of reversing $A$ with swap. Since $A$ is valid, $Rev(A)$ is also valid?
    *   Actually, let's look at the structure. The operation preserves the property of being a valid parenthesis sequence.
    *   More importantly, consider the decomposition of $S$ into top-level primitive components. $S = P_1 P_2 \dots P_k$.
    *   The sample 1: $S = (())()$. Top-level primitives: $P_1 = (())$, $P_2 = ()$.
    *   The operation allows transforming $S$ to $()(())$. This is a swap of $P_1$ and $P_2$.
    *   Is it always possible to swap adjacent top-level primitives?
        *   Let $A$ and $B$ be two adjacent top-level primitives. The substring $AB$ is a valid parenthesis sequence (concatenation of two valid sequences).
        *   Reversing $AB$: The first char of $A$ is `(`, becomes `)`. The last char of $B$ is `)`, becomes `(`.
        *   Wait, the definition says: $S_i$ becomes `)` if $S_{l+r-i}$ is `(`, and `(` if $S_{l+r-i}$ is `)`.
        *   Let's check if reversing $AB$ results in $Rev(B) Rev(A)$? Or something else?
        *   Let $A = (())$, $B = ()$. $AB = (())()$.
        *   Reverse $AB$ (indices 1 to 6):
            *   Pos 1: $S_6 = ) \rightarrow ($
            *   Pos 2: $S_5 = ( \rightarrow )$
            *   Pos 3: $S_4 = ) \rightarrow ($
            *   Pos 4: $S_3 = ) \rightarrow ($
            *   Pos 5: $S_2 = ( \rightarrow )$
            *   Pos 6: $S_1 = ( \rightarrow )$
            *   Result: `()(())`.
        *   Note that $Rev(B)$ where $B=()$ is `()`. $Rev(A)$ where $A=(())$ is `()`.
        *   So $Rev(AB) = ()(()) = Rev(B) Rev(A)$?
        *   Let's check $Rev(B)$. $B=()$. Reverse indices 1-2 of $B$:
            *   Pos 1: $B_2 = ) \rightarrow ($
            *   Pos 2: $B_1 = ( \rightarrow )$
            *   $Rev(B) = ()$.
        *   $Rev(A)$. $A=(())$. Reverse indices 1-4 of $A$:
            *   Pos 1: $A_4 = ) \rightarrow ($
            *   Pos 2: $A_3 = ) \rightarrow ($
            *   Pos 3: $A_2 = ( \rightarrow )$
            *   Pos 4: $A_1 = ( \rightarrow )$
            *   $Rev(A) = (())$. Wait.
            *   $A=(())$. $A_1=(, A_2=(, A_3=), A_4=)$.
            *   New Pos 1: Old Pos 4 is `)` $\rightarrow$ `(`.
            *   New Pos 2: Old Pos 3 is `)` $\rightarrow$ `(`.
            *   New Pos 3: Old Pos 2 is `(` $\rightarrow$ `)`.
            *   New Pos 4: Old Pos 1 is `(` $\rightarrow$ `)`.
            *   Result: `(())`. So $Rev(A) = A$.
        *   So $Rev(AB) = ()(()) = Rev(B) Rev(A)$? No, $Rev(B)=(), Rev(A)=(())$. So $Rev(B)Rev(A) = ()(())$.
        *   It seems $Rev(AB) = Rev(B) Rev(A)$ holds if $Rev(A)=A$ and $Rev(B)=B$?
        *   Let's test with $A=(), B=(())$. $AB = ()(())$.
        *   Reverse $AB$:
            *   Pos 1: $S_6 = ) \rightarrow ($
            *   Pos 2: $S_5 = ( \rightarrow )$
            *   Pos 3: $S_4 = ) \rightarrow ($
            *   Pos 4: $S_3 = ( \rightarrow )$
            *   Pos 5: $S_2 = ) \rightarrow ($
            *   Pos 6: $S_1 = ( \rightarrow )$
            *   Result: `)(()()`. This is NOT a valid parenthesis sequence?
            *   Wait, the problem states we can only reverse a substring that IS a valid parenthesis sequence.
            *   Is `()(())` a valid parenthesis sequence? Yes.
            *   So we can reverse it. The result is `)(()()`.
            *   Let's check if `)(()()` is valid.
                *   Balance: -1, 0, 1, 0, 1, 0. It goes negative. So it's NOT valid.
            *   Contradiction? The problem says "Choose a contiguous substring ... that is a valid parenthesis sequence, and reverse it." It does NOT say the result must be valid. But the question asks for "distinct strings S that you can have at the end". Implicitly, are we restricted to valid strings?
            *   "A string is defined to be a valid parenthesis sequence if..."
            *   "You are given a valid parenthesis sequence S... Find the number ... of distinct strings S that you can have at the end".
            *   Usually, in such problems, the operations preserve the validity. Let's re-read carefully.
            *   "reversing the substring ... means ... replace S_i with ) if S_{l+r-i} is ( ..."
            *   If we reverse a valid parenthesis sequence, is the result always a valid parenthesis sequence?
            *   Let $W$ be a valid parenthesis sequence. Let $W'$ be the reversed-swapped string.
            *   For any prefix of $W'$, does it have non-negative balance?
            *   Let $W = w_1 \dots w_n$. $W'_i = swap(w_{n-i+1})$.
            *   Balance of $W'$ at $k$: $\sum_{i=1}^k swap(w_{n-i+1})$.
            *   $swap('(') = -1, swap(')') = 1$.
            *   Let $bal_W(j)$ be the balance of prefix $j$ of $W$. $bal_W(0)=0, bal_W(n)=0$.
            *   $bal_{W'}(k) = \sum_{j=n-k+1}^n swap(w_j)$.
            *   Note that $swap(w_j) = - val(w_j)$ where $val('(')=1, val(')')=-1$.
            *   So $bal_{W'}(k) = - \sum_{j=n-k+1}^n val(w_j)$.
            *   Total sum $\sum_{j=1}^n val(w_j) = 0$.
            *   $\sum_{j=n-k+1}^n val(w_j) = - \sum_{j=1}^{n-k} val(w_j) = - bal_W(n-k)$.
            *   So $bal_{W'}(k) = - (- bal_W(n-k)) = bal_W(n-k)$.
            *   Since $W$ is valid, $bal_W(j) \ge 0$ for all $j$.
            *   Thus $bal_{W'}(k) \ge 0$ for all $k$.
            *   Also $bal_{W'}(n) = bal_W(0) = 0$.
            *   So $W'$ is a valid parenthesis sequence.
            *   My manual calculation for `()(())` was wrong.
            *   $W = ()(())$.
            *   $W_1=(, W_2=), W_3=(, W_4=(, W_5=), W_6=)$.
            *   $W'_1 = swap(W_6) = swap(')') = ($.
            *   $W'_2 = swap(W_5) = swap(')') = ($.
            *   $W'_3 = swap(W_4) = swap('(') = )$.
            *   $W'_4 = swap(W_3) = swap('(') = )$.
            *   $W'_5 = swap(W_2) = swap(')') = ($.
            *   $W'_6 = swap(W_1) = swap('(') = )$.
            *   Result: `(()())`.
            *   Is `(()())` valid? Yes.
            *   So the operation maps valid parenthesis sequences to valid parenthesis sequences.

2.  **Reachability**:
    *   The operation is an involution (applying it twice returns the original string).
    *   The key is to understand the equivalence classes under these operations.
    *   The sample 1 shows that top-level primitives can be swapped.
    *   Hypothesis: The reachable strings are exactly the permutations of the top-level primitive components.
    *   Why? Because any valid parenthesis sequence can be uniquely decomposed into a concatenation of primitive valid parenthesis sequences. The operation of reversing a valid substring $W$ effectively reverses the order of the "blocks" inside $W$ if $W$ is a concatenation of primitives?
    *   Actually, $Rev(AB) = Rev(B) Rev(A)$ was observed in Sample 1.
    *   If this property holds generally, i.e., $Rev(P_1 P_2 \dots P_m) = Rev(P_m) \dots Rev(P_1)$, then we can permute the top-level primitives arbitrarily.
    *   Furthermore, within each primitive component $P_i$, can we change its structure?
    *   If $P_i$ is primitive, it is of the form $(A)$. Reversing $P_i$ gives $Rev(P_i)$.
    *   $Rev((A)) = Rev(A)$ wrapped in `()`?
    *   Let $P = (A)$. $P_1 = '(', P_n = ')'$.
    *   $Rev(P)_1 = swap(P_n) = swap(')') = '('.$
    *   $Rev(P)_n = swap(P_1) = swap('(') = ')'.$
    *   The inner part $Rev(P)[2..n-1]$ is the reverse-swap of $A$.
    *   So $Rev(P) = ( Rev(A) )$.
    *   This means the structure of the primitive component is preserved, but the inner part $A$ is transformed recursively.
    *   However, the question asks for the number of *distinct strings*.
    *   If we can permute top-level primitives, do we also change the internal structure of primitives?
    *   If we reverse a single primitive $P$, we get $Rev(P)$. Is $Rev(P)$ distinct from $P$?
    *   In Sample 1, $P_1 = (())$. $Rev(P_1) = (())$. So $P_1$ is invariant.
    *   $P_2 = ()$. $Rev(P_2) = ()$. Invariant.
    *   What if we have $S = (())(())$? Primitives are identical.
    *   What if $S = (()())$? Primitive $P = (()())$.
    *   $Rev(P)$:
        *   $P = ( ()() )$. Inner $A = ()()$.
        *   $Rev(A)$: $A=()()$. $Rev(A) = ()()$.
        *   So $Rev(P) = ( ()() ) = P$.
    *   It seems many primitives are self-inverse.
    *   However, consider $S = ((()))$. $P = ((()))$. $A = (())$. $Rev(A) = (())$. $Rev(P) = ((()))$.
    *   Consider $S = (())(())$.
    *   Is it possible to generate a string where a primitive component is replaced by its reverse?
    *   If we reverse the entire string $S$, we get $Rev(S) = Rev(P_k) \dots Rev(P_1)$.
    *   If we can swap adjacent primitives, we can generate any permutation.
    *   Can we change a primitive $P$ to $Rev(P)$ independently?
    *   If we reverse a substring that is just $P_i$, we replace $P_i$ with $Rev(P_i)$.
    *   So, for each primitive component $P_i$, we can choose to keep it as $P_i$ or replace it with $Rev(P_i)$.
    *   BUT, are $P_i$ and $Rev(P_i)$ always distinct?
    *   If $P_i = Rev(P_i)$, then there is no choice.
    *   If $P_i \neq Rev(P_i)$, then we have 2 choices for that component?
    *   Wait, the operation allows reversing *any* valid substring.
    *   If we reverse $P_i$, we get $Rev(P_i)$.
    *   If we reverse $P_i P_j$, we get $Rev(P_j) Rev(P_i)$.
    *   This suggests that the set of reachable strings consists of all strings formed by:
        1.  Permuting the top-level primitives.
        2.  For each primitive in the permutation, optionally replacing it with its reverse.
    *   However, we must check if $Rev(P)$ is always reachable from $P$ via operations that might affect other parts.
    *   Since we can reverse the substring corresponding to just $P_i$ (which is a valid substring), we can always transform $P_i$ to $Rev(P_i)$ locally.
    *   So, each top-level primitive component $P_i$ can independently be either $P_i$ or $Rev(P_i)$.
    *   Let $Q_i$ be the set $\{P_i, Rev(P_i)\}$. Note that if $P_i = Rev(P_i)$, $|Q_i|=1$. If $P_i \neq Rev(P_i)$, $|Q_i|=2$.
    *   The total number of distinct strings would be the number of distinct permutations of the multiset of components, where each component $P_i$ can be replaced by any element in $Q_i$.
    *   This seems complicated. Let's look at the structure again.
    *   Actually, $Rev(P_i)$ might be equal to some $P_j$.
    *   Let's define the "type" of a primitive.
    *   The problem reduces to: We have $k$ slots. Each slot $i$ initially has value $P_i$. We can replace $P_i$ with $Rev(P_i)$. We can also permute the slots.
    *   So we have a multiset of available "atoms". For each original primitive $P_i$, we have two potential forms: $P_i$ and $Rev(P_i)$.
    *   However, we can't mix and match arbitrarily?
    *   Yes we can. Reverse $P_i$ to get $Rev(P_i)$. Reverse $P_j$ to get $Rev(P_j)$. Then swap them.
    *   So the set of reachable strings is the set of all concatenations $C_1 C_2 \dots C_k$ where $\{C_1, \dots, C_k\}$ is a permutation of $\{A_1, \dots, A_k\}$ and each $A_i \in \{P_i, Rev(P_i)\}$.
    *   Wait, is it a permutation of the *indices*?
    *   Yes, we permute the components. And for each component, we can choose its orientation.
    *   So, we have $k$ positions. We assign to each position a component from the original set, but each original component $P_i$ can appear in two forms.
    *   Actually, it's simpler:
        *   We have $k$ items. Item $i$ has a "base" form $P_i$ and a "flipped" form $F_i = Rev(P_i)$.
        *   We can permute the items.
        *   We can flip any item.
        *   So the set of reachable strings corresponds to the set of distinct permutations of the multiset $\{ S_1, S_2, \dots, S_k \}$ where $S_i$ is either $P_i$ or $F_i$.
        *   But we can choose the orientation for *each* instance.
        *   So effectively, we have $2k$ potential strings? No.
        *   We have $k$ slots. In each slot, we place one of the $k$ primitives, but each primitive $P_i$ can be in state $P_i$ or $F_i$.
        *   So we are forming a sequence of length $k$ using the available primitives.
        *   The available primitives are the original $P_1, \dots, P_k$. But each $P_i$ can be transformed to $F_i$.
        *   So the pool of available "tokens" is $\{ P_1, F_1, P_2, F_2, \dots, P_k, F_k \}$? No, we must use exactly one token for each original component index.
        *   So we choose an orientation $o_i \in \{0, 1\}$ for each $i$, forming a multiset $M = \{ V_1, \dots, V_k \}$ where $V_i = P_i$ if $o_i=0$ else $F_i$.
        *   Then we count the number of distinct permutations of $M$.
        *   And we sum this over all $2^k$ choices of orientations?
        *   No, we want the size of the union of the sets of permutations for all $2^k$ multisets.
        *   This seems too complex for $N=5000$.

    *   Let's reconsider the sample 1.
    *   $P_1 = (())$, $P_2 = ()$.
    *   $Rev(P_1) = (()) = P_1$.
    *   $Rev(P_2) = () = P_2$.
    *   So $F_1 = P_1, F_2 = P_2$.
    *   The multisets are always $\{ (()), () \}$.
    *   Permutations: $(())()$ and $()(())$. Count = 2.
    *   Formula: $k! / (\prod count!)$. Here $k=2$, counts are 1, 1. $2! / (1! 1!) = 2$.

    *   Sample 2: $S = ()$. $P_1 = ()$. $Rev(P_1) = ()$.
    *   Multiset $\{ () \}$. Permutations: 1.

    *   What if $P \neq Rev(P)$?
    *   Example: $S = (()())$. Primitive $P = (()())$.
    *   $Rev(P) = (()()) = P$.
    *   Example: $S = ((())())$.
    *   Primitives: $P_1 = ((()))$, $P_2 = ()$.
    *   $Rev(P_1) = ((()))$. $Rev(P_2) = ()$.
    *   All self-inverse.

    *   Is there a primitive that is NOT self-inverse?
    *   $P = (())$. $Rev(P) = (())$.
    *   $P = ()$. $Rev(P) = ()$.
    *   $P = (()())$. $Rev(P) = (()())$.
    *   $P = ((()))$. $Rev(P) = ((()))$.
    *   It seems all primitive valid parenthesis sequences are self-inverse under this operation?
    *   Let's prove or disprove.
    *   $P$ is primitive $\implies P = (A)$.
    *   $Rev(P) = ( Rev(A) )$.
    *   So $P = Rev(P) \iff A = Rev(A)$.
    *   Base case: $A = \epsilon$ (empty). $Rev(\epsilon) = \epsilon$. $P = ()$. Self-inverse.
    *   Inductive step: If all valid parenthesis sequences of length $< 2m$ are self-inverse, then $A$ (length $2m-2$) is self-inverse.
    *   Thus $P = (A)$ is self-inverse.
    *   Therefore, **every** valid parenthesis sequence is self-inverse under this reversal operation.
    *   Proof:
        *   Let $W$ be a valid parenthesis sequence.
        *   We showed $bal_{W'}(k) = bal_W(n-k)$.
        *   If $W$ is primitive, $W=(A)$. $Rev(W) = (Rev(A))$.
        *   If $Rev(A) = A$, then $Rev(W) = W$.
        *   By induction, all valid parenthesis sequences are self-inverse.
    *   Conclusion: $Rev(P_i) = P_i$ for all $i$.
    *   So the orientation choice is trivial. We only permute the top-level primitives.
    *   The answer is the number of distinct permutations of the multiset of top-level primitive components.

    *   Algorithm:
        1.  Decompose $S$ into top-level primitive components.
        2.  Store these components in a list.
        3.  Count the frequency of each distinct component string.
        4.  Calculate $k! / (\prod count(c)!) \pmod{998244353}$.

    *   Complexity:
        *   Decomposition: $O(N)$.
        *   String hashing or comparison: Comparing two strings of length $L$ takes $O(L)$.
        *   Sorting or hashing the components: $O(k \cdot N)$ in worst case if naive.
        *   Since $\sum |P_i| = N$, we can use a Trie or sort the components efficiently.
        *   Actually, we can just store the strings and use a hash map.
        *   Python's `dict` with string keys is efficient.
        *   Total time $O(N^2)$ worst case if many small components? No, string hashing is linear in length.
        *   Sum of lengths is $N$. So creating hashes is $O(N)$.
        *   Sorting $k$ strings with total length $N$ is $O(N \log k)$ or $O(N \log N)$.
        *   This fits within $N=5000$.

## worker: (none)
The problem asks for the number of distinct valid parenthesis sequences reachable by reversing contiguous valid parenthesis substrings (with parenthesis swapping).

Key insights:
1.  **Operation Preserves Validity**: Reversing a valid parenthesis substring $W$ (with swapped parentheses) results in another valid parenthesis sequence. This is because the balance profile of the reversed string $W'$ at index $k$ is equal to the balance profile of $W$ at index $n-k$, which is non-negative.
2.  **Self-Inverse Property**: Every valid parenthesis sequence $W$ is self-inverse under this operation, i.e., $Rev(Rev(W)) = W$. More strongly, $Rev(W) = W$ for all valid parenthesis sequences $W$.
    *   Proof by induction:
        *   Base case: Empty string is self-inverse.
        *   Inductive step: Any valid parenthesis sequence $W$ can be decomposed into top-level primitives $P_1 P_2 \dots P_k$.
        *   A primitive $P$ has the form $(A)$ where $A$ is a valid parenthesis sequence.
        *   $Rev(P) = Rev((A)) = (Rev(A))$.
        *   By induction, $Rev(A) = A$, so $Rev(P) = (A) = P$.
        *   Also, $Rev(P_1 \dots P_k) = Rev(P_k) \dots Rev(P_1) = P_k \dots P_1$.
3.  **Reachability**: The operation allows us to reverse any valid substring. Specifically, reversing the entire string $S = P_1 \dots P_k$ yields $P_k \dots P_1$. By combining reversals of prefixes/suffixes or adjacent blocks, we can generate any permutation of the top-level primitive components.
4.  **Counting**: Since each primitive component $P_i$ satisfies $Rev(P_i) = P_i$, there is no "orientation" choice. The set of reachable strings is exactly the set of all distinct permutations of the multiset of top-level primitive components.
5.  **Algorithm**:
    *   Decompose $S$ into top-level primitive components.
    *   Count the frequency of each distinct component.
    *   The answer is the multinomial coefficient $k! / (\prod c_i!)$ modulo 998244353.

Complexity:
*   Decomposition: $O(N)$.
*   Counting: $O(N)$ using string hashing or dictionary.
*   Factorials and modular inverse: $O(N)$.
*   Total Time: $O(N)$.
*   Space: $O(N)$.
