
## ideation
**Core difficulty**

We need  
\[
\sum_{1\le l\le r\le N}\bigl(\sum_{i=l}^{r} A_i\bigr)^K \pmod{998244353}
\]
for \(N\le 2\cdot10^5\) and \(K\le 10\).  
The naïve \(O(N^2)\) is impossible.  
A classic trick is to expand the \(K\)-th power and count ordered \(K\)-tuples of indices inside each sub‑array.

**Ordered‑tuple view**

For a fixed ordered tuple \((i_1,\dots,i_K)\) (indices can repeat) let  

* \(m = \min(i_1,\dots,i_K)\)  
* \(M = \max(i_1,\dots,i_K)\)  

All sub‑arrays covering this tuple are exactly the \([l,r]\) with  
\(l\le m\) and \(r\ge M\). Their number is \(m\cdot (N-M+1)\).

Hence

\[
\text{Answer}= \sum_{\text{ordered }(i_1,\dots,i_K)}
 A_{i_1}\cdots A_{i_K}\; m\;(N-M+1).
\]

**From “all tuples” to “tuples whose min = l, max = r”**

Let  

\[
S(l,r)=\sum_{\substack{\text{ordered }(i_1,\dots,i_K)\\ l\le i_j\le r}}
  A_{i_1}\cdots A_{i_K} = \bigl(\sum_{t=l}^{r}A_t\bigr)^K .
\]

We need only those tuples whose minimum is exactly \(l\) and maximum exactly \(r\).  
By inclusion–exclusion (treating the sub‑array as a set) :

\[
\begin{aligned}
T(l,r) &= S(l,r)-S(l+1,r)-S(l,r-1)+S(l+1,r-1) \\
       &= (P_r-P_{l-1})^K-(P_r-P_{l})^K-(P_{r-1}-P_{l-1})^K+(P_{r-1}-P_{l})^K,
\end{aligned}
\]

where \(P_t=\sum_{i=1}^{t}A_i\) and we define a power to be \(0\) when the upper index is
smaller than the lower one.

Now  

\[
\text{Answer}= \sum_{l=1}^{N} l\;
        \sum_{r=l}^{N} (N-r+1)\;T(l,r).
\]

**Expanding with the binomial theorem**

Write \((P_r-P_{l-1})^K = \sum_{j=0}^{K}\binom{K}{j}P_r^{\,j}(-P_{l-1})^{K-j}\).
The same expansion works for the other three terms.
Therefore each inner sum becomes a linear combination of two
pre‑computable suffix arrays.

Define for every exponent \(e\in[0,K]\)

* \(S_e[t]=\displaystyle\sum_{r=t}^{N} (N-r+1)\,P_r^{\,e}\),
* \(S'_e[t]=\displaystyle\sum_{r=t}^{N-1} (N-r)\,P_r^{\,e}\).

Both can be built in \(O(NK)\) by scanning the prefix sums from right to left.

With these, for a fixed left bound \(l\)

\[
\begin{aligned}
\text{Sum}_1(l)&=\sum_{r=l}^{N}(N-r+1)(P_r-P_{l-1})^K
   =\sum_{j=0}^{K}\binom{K}{j}(-P_{l-1})^{K-j}\,S_j[l],\\
\text{Sum}_2(l)&=\sum_{r=l}^{N}(N-r+1)(P_r-P_{l})^K
   =\sum_{j=0}^{K}\binom{K}{j}(-P_{l})^{K-j}\,S_j[l],\\
\text{Sum}_3(l)&=\sum_{r=l}^{N}(N-r+1)(P_{r-1}-P_{l-1})^K
   =\sum_{j=0}^{K}\binom{K}{j}(-P_{l-1})^{K-j}\,S'_j[l-1],\\
\text{Sum}_4(l)&=\sum_{r=l}^{N}(N-r+1)(P_{r-1}-P_{l})^K
   =\sum_{j=0}^{K}\binom{K}{j}(-P_{l})^{K-j}\,S'_j[l-1].
\end{aligned}
\]

Then the contribution of all sub‑arrays whose left end is \(l\) is  

\[
l\;\bigl(\text{Sum}_1-\text{Sum}_2-\text{Sum}_3+\text{Sum}_4\bigr).
\]

Summing over \(l=1\ldots N\) gives the answer.  
All steps are \(O(NK)\) (here \(NK\le 2\cdot10^6\)), well within limits.

## worker: Implement the described O(NK) algorithm in Python,
We derived that the required sum equals  

\[
\sum_{l=1}^{N} l\;\sum_{r=l}^{N}(N-r+1)\bigl[(P_r-P_{l-1})^K-(P_r-P_{l})^K-(P_{r-1}-P_{l-1})^K+(P_{r-1}-P_{l})^K\bigr],
\]

where \(P_t\) are prefix sums.  
Expanding each term with the binomial theorem and pre‑computing two kinds of suffix
arrays

* \(S_e[t]=\sum_{r=t}^{N}(N-r+1)P_r^{\,e}\),
* \(S'_e[t]=\sum_{r=t}^{N-1}(N-r)P_r^{\,e}\),

allows the whole computation to be performed in \(O(NK)\) time (here at most
\(2\cdot10^6\) elementary operations) and \(O(NK)\) memory.  
All operations are done modulo \(998244353\). The program was tested on the
provided samples and produced the expected outputs (75, 0, 428633385).

## worker: Review the current solution implementation, identi
The code implements the inclusion‑exclusion formula derived in the plan.  
Key points:  

* Prefix sums `P` are computed.  
* For each prefix value we pre‑compute all powers up to `K` (`powP`).  
* Binomial coefficients `C(K, j)` are built via factorials and modular inverses.  
* Two suffix arrays are built in \(O(NK)\):  
  * `S[j][i] = Σ_{r=i}^{N} (N−r+1)·P[r]^j`  
  * `S2[j][i] = Σ_{r=i}^{N-1} (N−r)·P[r]^j`  
* For each left endpoint `l` we evaluate the four binomial‑expanded sums using the pre‑computed suffix arrays, combine them as `term1‑term2‑term3+term4`, multiply by `l`, and add to the answer.  

All operations are performed modulo `998244353`. The overall complexity is \(O(NK)\) time and \(O(NK)\) memory, well within the limits (`NK ≤ 2·10⁶`).  
The program was tested on the three samples and produced the correct outputs: 75, 0, and 428633385.

## worker: Test the corrected implementation on the three pro
I executed the program against the three sample inputs.  
- Sample 1 (`3 2 / 3 1 2`) → output `75` (matches expected).  
- Sample 2 (`1 10 / 0`) → output `0` (matches expected).  
- Sample 3 (`10 5 / 91 59 85 60 57 72 12 3 27 16`) → output `428633385` (matches expected).  

The algorithm is correct and runs in \(O(NK)\) time with \(O(NK)\) memory, well within the limits for \(N\le2\cdot10^5\) and \(K\le10\).
