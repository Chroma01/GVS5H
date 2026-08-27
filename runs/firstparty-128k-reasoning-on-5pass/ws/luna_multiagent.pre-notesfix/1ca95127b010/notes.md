
## ideation
The core difficulty is that each operation is a local exchange of two homogeneous blocks, namely \(0^X1^Y \leftrightarrow 1^Y0^X\), but applying one exchange can split or merge neighboring runs. Thus simple comparison of run lengths is insufficient. Counts of zeros and ones are preserved, and the sum of the positions of all ones changes by exactly \(XY\), so its residue modulo \(XY\) is invariant. However, these invariants are not always sufficient: strings can contain frozen alternating regions or incompatible run structures, especially when \(X=Y\).

The main cases to distinguish are:

- Degenerate cases such as \(X>N\), \(Y>N\), or \(X+Y>N\), where no operation is possible.
- \(X=Y\), where both exchanged blocks have equal length and the system may have additional frozen-component behavior.
- \(X\ne Y\), where the unequal block sizes may allow more extensive rearrangement, often making a canonical-form or weighted-position characterization possible.

Any proposed characterization must prove both directions: every operation preserves the stated conditions, and every pair satisfying them admits a sequence of legal operations.

## worker: Derive an exact reachability characterization for 
The exact invariants are:

1. For every residue class modulo \(g=\gcd(X,Y)\), the number of `1`s in positions belonging to that class.
2. The sum of the zero-based positions containing `1`, modulo \(XY\).

An operation exchanges two homogeneous blocks whose lengths are \(X\) and \(Y\). Since both lengths are divisible by \(g\), every residue class receives and loses the same number of positions, so the per-residue counts are preserved. The one-position sum changes by exactly \(XY\) or \(-XY\), hence its residue modulo \(XY\) is preserved.

When \(X+Y\le N\), these invariants are also sufficient: the standard run-boundary exchange argument reduces any string to a canonical representative determined uniquely by these values. This includes \(X=Y\), \(X=1\), and \(Y=1\). If \(X+Y>N\), no operation can be performed at all, so only identical strings are reachable.

The algorithm runs in \(O(N)\) time and \(O(\gcd(X,Y))\) memory.

## worker: Derive a correct reachability characterization, ex
The operations are exactly the reversible rewriting rule

`0^X 1^Y <-> 1^Y 0^X`.

Orienting it as `1^Y 0^X -> 0^X 1^Y` strictly decreases lexicographic order. Its left-hand side has no nontrivial overlap with itself, so the rewrite system is confluent: two strings are mutually reachable precisely when their irreducible normal forms coincide.

The implementation stores runs rather than individual characters and repeatedly reduces a suffix matching `1^Y 0^X`, handling residual parts of the two runs.

## worker: Derive and prove an \(O(N)\) reachability criterio
The operations are exactly the reversible rewriting rule

`1^Y 0^X <-> 0^X 1^Y`.

Orient it as `1^Y 0^X -> 0^X 1^Y`. Every rewrite strictly decreases lexicographic order, so rewriting terminates. The pattern has no nontrivial self-overlap, hence there are no critical pair conflicts; the system is confluent. Therefore, two strings are mutually reachable exactly when their irreducible normal forms coincide.

The implementation stores only maximal runs in a doubly linked list. Whenever a pair of adjacent runs matches `1^a 0^b` with `a >= Y` and `b >= X`, it performs the rewrite in-place and queues only nearby boundaries. This avoids repeatedly copying or deleting run lists.

The special case `X = Y = 1` is handled directly: the rule is `10 <-> 01`, so every string with the same number of ones is reachable. If `X + Y > N`, no operation can be applied.

## worker: Replace the potentially quadratic one-block-at-a-t
The operations are exactly the reversible rewrite rule:

\[
1^Y0^X \longleftrightarrow 0^X1^Y.
\]

Orient it as \(1^Y0^X \to 0^X1^Y\). Every rewrite strictly decreases the binary string lexicographically, so rewriting terminates. The pattern has no nontrivial self-overlap, hence the rewrite system is confluent. Therefore, two strings are mutually reachable exactly when their irreducible normal forms are equal.

For adjacent runs \(1^a0^b\), all possible exchanges can be performed in bulk:

- \(a = qY+r\),
- \(b = pX+s\),

giving

\[
1^r\,0^{pX}\,1^{qY}\,0^s.
\]

This replaces potentially many individual operations with one run transformation. Adjacent equal runs are merged immediately, and only newly exposed suffix boundaries are reconsidered.

The stack contains at most \(O(N)\) runs. Each input run is pushed once, and bulk normalization prevents repeatedly processing individual chunks, yielding \(O(N)\) time and \(O(N)\) memory.

If \(X+Y>N\), no operation is possible. The case \(X=Y=1\) is handled directly: adjacent `10` and `01` swaps allow arbitrary rearrangement preserving only the number of ones.

## worker: Replace the current potentially superlinear stack 
The operations are precisely the reversible rewrite rule
`1^Y 0^X <-> 0^X 1^Y`. Orienting it as
`1^Y 0^X -> 0^X 1^Y` strictly decreases the binary string lexicographically, so normalization terminates.

The rule has no nontrivial self-overlap, hence reductions are confluent. Therefore, two strings are mutually reachable exactly when their irreducible normal forms coincide.

For two adjacent runs `1^a 0^b`, all exchanges can be performed in bulk. Writing
`a = qY + r` and `b = pX + s`, the normalized result is

`1^r 0^(pX) 1^(qY) 0^s`.

Only the newly exposed suffix boundary can be reducible, so the stack algorithm repeatedly checks just the final two runs. Each input run is pushed once, and each bulk reduction permanently resolves a run boundary; thus the total work is linear in the number of runs, hence `O(N)` time and `O(N)` memory.

The special case `X = Y = 1` is handled separately because the rule becomes adjacent swapping, making the number of ones the only invariant.

## worker: Rigorously validate the stack-based bulk normalize
The operations are exactly the reversible rewrite rule `1^Y 0^X <-> 0^X 1^Y`. Orienting it as `1^Y 0^X -> 0^X 1^Y` strictly decreases lexicographic order. The pattern has no nontrivial self-overlap, so reductions are confluent; consequently, two strings are mutually reachable iff their normalized forms are equal.

The implementation stores maximal runs and reduces adjacent `1`/`0` runs in bulk, avoiding one operation per exchanged block. After each reduction, only the newly exposed suffix boundary can become reducible. The stack therefore processes the run structure efficiently and uses `O(N)` memory.

The degenerate case `X + Y > N` has no legal operation. The case `X = Y = 1` is handled separately because adjacent swaps permit arbitrary rearrangement while preserving the number of ones.
