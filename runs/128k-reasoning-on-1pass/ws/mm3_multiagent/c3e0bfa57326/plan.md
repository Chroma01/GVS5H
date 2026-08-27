**Solution Explanation**

For a parenthesis string `S` ( `|S| = N` ) we can do the following operation any number of times  

*choose a balanced substring and replace it by its “reverse complement”*  

(the substring is read from right to left and each ‘(’ is changed to ‘)’ and
vice‑versa).

--------------------------------------------------------------------

#### 1.   From a string to a rooted ordered tree  

For a balanced string the usual stack parsing gives a rooted ordered tree.

* a node = a pair of matching parentheses,
* its children = the immediate inner pairs (the first level inside the node).

If the whole string is a concatenation of several primitive blocks,
the first ‘(’ does **not** match the last ‘)’.  
In that case we add a dummy root whose children are the top level blocks.
The dummy root has no surrounding parentheses, it only concatenates its
children.

For the whole input we obtain

```
real nodes :  N/2
dummy root :  one more node
edges      :  (N/2 - 1)   (the tree is a forest)
```

--------------------------------------------------------------------

#### 2.   What can an operation do ?

Take a node `v` and a **contiguous** block of its children  
`c[i] , c[i+1] , … , c[j]`.  
The block itself is a balanced substring, therefore the operation may be
applied to it.
If the block consists of one child, the operation is just “reverse‑complement
of this child”, i.e. we may **toggle** this child.
If the block has length `≥ 2` the operation is

```
reverse the order of the children in the block
and toggle every child inside the block
```

Consequences  

* for a fixed node we can
    * toggle any child,
    * swap two adjacent children **and** toggle both.

From these elementary moves we can obtain

* any permutation of the children,
* independently toggle each child.

Thus for every node the reachable configurations of its children are exactly

```
all signed permutations of the original child list
```

The root of the whole tree behaves the same, only its outermost parentheses
are fixed.

--------------------------------------------------------------------

#### 3.   Counting the strings of a subtree  

For a node `v`

* let `t1 , … , tk` be the types of its children,
  `cnt[t]` – how many children of type `t` (`k = Σ cnt[t]`),
* `DP[t]` – number of different strings that can be obtained from a
  subtree of type `t` (already computed, because the tree is processed
  bottom‑up).

All strings reachable for a child of type `t` are different,
and strings of different types are also different.
For the `cnt[t]` children of the same type we may choose the string of the
child independently – `DP[t]^{cnt[t]}` possibilities.
After the strings are chosen we may permute the children arbitrarily.
For a fixed multiset of chosen strings the number of different orders is
`k! / ( Π mult(s)! )`, where `mult(s)` is the multiplicity of a string `s`.
Summing over all choices gives

```
DP[v] = k! · ∏_t  ( DP[t]^{cnt[t]} / cnt[t]! )
```

The formula can be proved by a simple generating function or by a direct
Burnside argument – both lead to the same expression.

*Leaf* : `k = 0` → `DP = 1`.

All operations on different nodes are independent, therefore the formula
can be applied recursively.

--------------------------------------------------------------------

#### 4.   Whole algorithm  

```
parse S → tree (real nodes) + list of top level children
pre‑compute factorials and inverse factorials modulo MOD

process real nodes in reverse order (children before parent)
        for the current node
                count how many children of each type
                k = number of children
                DP = fact[k] *
                     Π  ( DP_of_type[t] ^ cnt[t]  *  inv_fact[cnt[t]] )
                make a canonical key = sorted list of (type , cnt)
                give the node a type id (the same key → same id)
                store DP for this type
        (the leaf type gets id 0, DP = 1)

finally treat the dummy root:
        its children are the top level real nodes
        compute the same formula for the dummy root
        the obtained value is the answer
```

`N ≤ 5000`, the tree has at most `2500` real nodes,
the total number of children over all nodes is `O(N)`.  
All steps are linear (or `O(N log N)` because of sorting the child type
lists), easily fast enough.

--------------------------------------------------------------------

#### 5.   Correctness Proof  

We prove that the algorithm prints the required number of different
strings.

---

##### Lemma 1  
For a node `v` and a contiguous block of its children the operation
“reverse‑complement of the block” is equivalent to

* toggling every child inside the block (apply the operation to the child
  alone) and
* reversing the order of the children of the block.

**Proof.**  
Let the block consist of children `A1 , A2 , … , Am` (each a balanced
substring).  
The block’s string is `A1 A2 … Am`.  
Reverse order → `Am … A2 A1`.  
Complement each character → `dual(Am) … dual(A2) dual(A1)`.  
The result is the concatenation of the duals of the children in the
reversed order. ∎



##### Lemma 2  
Using the operation on a node and on its children we can realise

* any permutation of the children,
* independently toggling each child.

**Proof.**  
*Toggle a single child* – apply the operation to the substring consisting
only of this child, which is exactly the reverse‑complement of the child,
i.e. toggle it.

*Swap two adjacent children and toggle both* – apply the operation to the
block consisting of the two children (Lemma&nbsp;1).  
If we first swap and then toggle each child once more, the toggles cancel,
so we obtain a plain swap.

Repeatedly swapping adjacent children gives every permutation.
Combined with the ability to toggle a child we obtain any signed
permutation. ∎



##### Lemma 3  
For a node `v` let  

* `cnt[t]` – number of children of type `t`,
* `DP[t]` – number of different strings reachable for a child of type `t`.

Then the number of different strings reachable for the whole subtree of `v`
is  

```
DP[v] = ( Σ cnt[t] )!  ·  ∏_t  ( DP[t]^{cnt[t]} / cnt[t]! )
```

**Proof.**  
Because of Lemma&nbsp;2 the children can be arranged in any order and each
child may be replaced by any string from the set `S_t` (size `DP[t]`).

*Choose the string for each child.*  
For the `cnt[t]` children of type `t` we have `DP[t]^{cnt[t]}` ordered
choices.

*Now forget the order of the children.*  
For a fixed multiset of chosen strings the number of different orders is
`k! / ( Π mult(s)! )`.  
Summation over all possible choices is exactly the coefficient of
`x^{k}` in  

```
( Σ_{multiset of size cnt[t]}   1 / ( Π mult! ) )   =   DP[t]^{cnt[t]} / cnt[t]!
```

(the ordinary generating function of a multiset).  
Multiplying the contributions of all types and by `k!` gives the formula. ∎



##### Lemma 4  
The algorithm computes `DP[v]` for every real node `v` and for the dummy
root.

**Proof.**  
Processing order is reverse topological (children first).  
When a node `v` is processed, all its children already have a type id and
a stored value `DP_of_type[·]`.  
The algorithm applies exactly the formula of Lemma&nbsp;3, therefore the
computed number equals `DP[v]`. ∎



##### Lemma 5  
Two real nodes have the same type id **iff** the multisets of their
children’s types are equal.

**Proof.**  
The type id is created from the sorted list
`(type, multiplicity)` of the node’s children.
If two nodes have the same multiset, the lists are identical, they obtain
the same key and the same id.
Conversely, different multisets give different keys, hence different ids. ∎



##### Lemma 6  
For every node the value stored for its type (`type_dp[id]`) equals the
number of reachable strings of any node of that type.

**Proof.**  
Induction over the processing order.

*Base* – a leaf has an empty child multiset, key `()`, receives a fresh id,
and the algorithm stores `DP = 1`, which is the correct number of strings
for a leaf.

*Induction step* – assume the statement true for all children of a node
`v`.  
All children already have correct type ids and the associated values
`type_dp`.  
The algorithm computes `DP[v]` using Lemma&nbsp;3, therefore the stored
value is correct. ∎



##### Lemma 7  
The value printed by the algorithm equals the number of different strings
obtainable from the original string `S`.

**Proof.**  
The dummy root’s children are exactly the top level blocks of `S`.  
By Lemma&nbsp;4 the algorithm computes the value for the dummy root using
the same formula as for a normal node, therefore this value is the number
of strings reachable for the whole string. ∎



##### Theorem  
The algorithm outputs the number of distinct strings that can be obtained
from the given valid parenthesis sequence by any sequence of allowed
operations, modulo `998244353`.

**Proof.**  
Lemmas&nbsp;1 and&nbsp;2 describe precisely the group generated by the
operations.  
Lemma&nbsp;3 gives the exact number of strings for a subtree.
Lemmas&nbsp;4–6 show that the algorithm evaluates this number for every
subtree.  
Lemma&nbsp;7 shows that the final value is the required answer.
All calculations are performed modulo a prime, therefore the printed
value is the required answer modulo `998244353`. ∎



--------------------------------------------------------------------

#### 6.   Complexity Analysis  

```
M = N/2  ( ≤ 2500 )
```

* parsing the string: `O(N)`
* total number of children over all nodes: `M‑1`
* for every node:
    * counting child types – `O(degree)`
    * sorting the distinct types – `O( degree log degree )`
* all other work is `O(1)` per node

```
Time   :  O( N log N )   ( ≤ 5·10³·log 5·10³ )
Memory :  O( N )
```

Both limits easily satisfy the constraints.

--------------------------------------------------------------------

#### 7.   Reference Implementation  (Python 3)

```python
import sys

MOD = 998244353


def solve() -> None:
    data = sys.stdin.read().split()
    N = int(data[0])
    S = data[1].strip()

    # ---------- factorials ----------
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # ---------- parse the string ----------
    children = []               # children[i] = list of child ids of node i
    stack = []                 # stack of currently open '('
    top_level = []             # children of the dummy root

    for ch in S:
        if ch == '(':
            node_id = len(children)
            children.append([])
            stack.append(node_id)
        else:                   # ')'
            node_id = stack.pop()
            if stack:
                parent = stack[-1]
                children[parent].append(node_id)
            else:
                top_level.append(node_id)

    M = len(children)          # number of real nodes = N/2

    # ---------- DP for real nodes (bottom‑up) ----------
    type_id = [-1] * M          # type id of each real node
    dp_node = [0] * M           # DP value of the node (not needed later)
    type_dp = []                # DP value of each type
    key_to_type = {}            # canonical key -> type id

    # nodes are numbered in the order of their '(',
    # therefore children have larger ids – process backwards
    for v in range(M - 1, -1, -1):
        childs = children[v]

        # frequency of child types
        freq = {}
        for c in childs:
            t = type_id[c]
            freq[t] = freq.get(t, 0) + 1

        k = len(childs)
        cur = fact[k]
        for t, cnt in freq.items():
            cur = cur * pow(type_dp[t], cnt, MOD) % MOD
            cur = cur * inv_fact[cnt] % MOD
        dp_node[v] = cur

        # canonical key: sorted list of (type, count)
        key = tuple(sorted(freq.items()))
        if key not in key_to_type:
            new_type = len(type_dp)
            key_to_type[key] = new_type
            type_dp.append(cur)
        else:
            new_type = key_to_type[key]          # the same DP must be stored
            # (optional) assert type_dp[new_type] == cur
        type_id[v] = new_type

    # ---------- DP for the dummy root (concatenation of top level) ----------
    freq = {}
    for v in top_level:
        t = type_id[v]
        freq[t] = freq.get(t, 0) + 1

    k = len(top_level)
    ans = fact[k]
    for t, cnt in freq.items():
        ans = ans * pow(type_dp[t], cnt, MOD) % MOD
        ans = ans * inv_fact[cnt] % MOD

    print(ans % MOD)


if __name__ == "__main__":
    solve()
```

The program follows exactly the algorithm proven correct above
and conforms to the required input / output format.