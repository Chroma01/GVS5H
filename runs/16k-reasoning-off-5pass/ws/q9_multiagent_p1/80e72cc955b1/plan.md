The problem asks for the minimum operations to reduce all numbers in a range $[l, r]$ to zero, where one operation takes two numbers $a, b$ and replaces them with $\lfloor a/4 \rfloor, \lfloor b/4 \rfloor$. Notice that an operation does not reduce the *count* of non-zero elements unless at least one of the operands becomes zero. Specifically, if we pick two non-zero numbers, we still have two non-zero numbers (since $\lfloor x/4 \rfloor = 0$ only if $x < 4$). To reduce the count of non-zero elements by 1, we must pair a non-zero number with a number that is already zero (or effectively zero). However, the operation definition says "Select two integers... Replace them". If we select two non-zeros, we get two new numbers. The count of non-zeros stays the same unless one of the results is 0.
Actually, let's re-evaluate the operation cost.
Goal: All elements become 0.
Operation: $a, b \to \lfloor a/4 \rfloor, \lfloor b/4 \rfloor$.
If we have a number $x$, how many operations to make it 0?
$x \to \lfloor x/4 \rfloor \to \dots \to 0$. This takes $\lceil \log_4 x \rceil$ steps if we could operate on it alone. But we must operate on pairs.
Consider the process in reverse or by counting "reductions".
Actually, observe the examples.
Ex 1: [1, 2]. 1 op -> [0, 0]. Cost 1.
Ex 1: [2, 3, 4]. 2 ops -> [0, 0, 0]. Cost 2.
Ex 2: [2, 3, 4, 5, 6]. 4 ops.
Let $k$ be the number of non-zero elements. We need to reduce $k$ to 0.
Each operation involves 2 elements.
If we pick two non-zeros $a, b$, they become $a', b'$. If $a' > 0$ and $b' > 0$, the count of non-zeros is unchanged. If one becomes 0, count decreases by 1. If both become 0, count decreases by 2.
If we pick a non-zero $a$ and a zero $z$, they become $a', 0$. Count decreases by 1 if $a' > 0$, or 2 if $a'=0$.
Wait, the example [2, 3, 4] -> 2 ops.
Initial non-zeros: 3.
Op 1: 2, 4 -> 0, 1. Array: [0, 3, 1]. Non-zeros: 2. (Decreased by 1).
Op 2: 3, 1 -> 0, 0. Array: [0, 0, 0]. Non-zeros: 0. (Decreased by 2).
Total ops: 2.
It seems the strategy is to pair large numbers to generate zeros as fast as possible.
Actually, notice that $\lfloor x/4 \rfloor$ reduces the magnitude.
Let's look at the "cost" per number.
Number $x$ needs $c(x) = \lceil \log_4 x \rceil$ divisions to reach 0.
But we can combine divisions? No, the operation is simultaneous on two numbers.
Key Insight: The operation $a, b \to \lfloor a/4 \rfloor, \lfloor b/4 \rfloor$ is equivalent to saying we perform a division by 4 on two numbers simultaneously.
We need to perform enough divisions so that every number becomes 0.
Let $max\_ops = \max_{x \in nums} (\text{steps to make } x \text{ zero})$.
In each step, we can reduce the "step count" of two numbers by 1.
So if we have a set of numbers, and we want to reduce all of them to 0, we can think of it as:
Each number $x$ has a "height" $h(x) = \lceil \log_4 x \rceil$.
We need to reduce all heights to 0.
In one operation, we pick two numbers and reduce their heights by 1.
However, if a height is already 0, we can still pick it (it stays 0) to reduce another number's height?
Yes, if we pick $0$ (height 0) and $x$ (height $h$), result is $0, \lfloor x/4 \rfloor$. The height of $x$ reduces by 1. The height of 0 stays 0.
So effectively, in one operation, we can reduce the height of *two* numbers by 1, provided they are not already 0? No, even if one is 0, the other reduces.
Wait, if we pick $x$ and $y$, both reduce. If we pick $x$ and $0$, only $x$ reduces.
To minimize operations, we should always pick two numbers that still need reduction.
So, if we have $N$ numbers with heights $h_1, h_2, \dots, h_N$.
We want to reduce all to 0.
Each operation reduces the sum of heights by at most 2 (if we pick two non-zero-height numbers).
Actually, the constraint is simpler:
We have $N$ items. We need to apply $h_i$ reductions to item $i$.
Total reductions needed = $\sum h_i$.
Each operation provides 2 reduction slots.
So minimum operations = $\lceil (\sum h_i) / 2 \rceil$?
Let's check Ex 1: [1, 2].
$h(1) = \lceil \log_4 1 \rceil = 0$.
$h(2) = \lceil \log_4 2 \rceil = 1$.
Sum = 1. Ops = $\lceil 1/2 \rceil = 1$. Correct.
Ex 1: [2, 3, 4].
$h(2)=1, h(3)=1, h(4)=1$.
Sum = 3. Ops = $\lceil 3/2 \rceil = 2$. Correct.
Ex 2: [2, 3, 4, 5, 6].
$h(2)=1, h(3)=1, h(4)=1, h(5)=1, h(6)=1$.
Sum = 5. Ops = $\lceil 5/2 \rceil = 3$?
But Example 2 output is 4.
Why?
Let's re-read the operation. "Select two integers a and b... Replace them with floor(a/4) and floor(b/4)".
Ah, if $a=1$, $\lfloor 1/4 \rfloor = 0$.
$h(1)=0$.
$h(2)=1$ ($2 \to 0$).
$h(3)=1$ ($3 \to 0$).
$h(4)=1$ ($4 \to 1 \to 0$). Wait.
$4 \to \lfloor 4/4 \rfloor = 1$. Then $1 \to 0$. So $h(4)=2$.
My calculation of $h(x)$ was wrong.
$h(x)$ is the number of times we divide by 4 until 0.
$x=1: 1 \to 0$ (1 op). $h(1)=1$.
$x=2: 2 \to 0$ (1 op). $h(2)=1$.
$x=3: 3 \to 0$ (1 op). $h(3)=1$.
$x=4: 4 \to 1 \to 0$ (2 ops). $h(4)=2$.
$x=5: 5 \to 1 \to 0$ (2 ops). $h(5)=2$.
$x=6: 6 \to 1 \to 0$ (2 ops). $h(6)=2$.
Re-eval Ex 2: [2, 3, 4, 5, 6].
$h$: 1, 1, 2, 2, 2.
Sum = 8.
Ops = $\lceil 8/2 \rceil = 4$. Matches Example 2.
Re-eval Ex 1: [1, 2].
$h$: 1, 1. Sum = 2. Ops = 1. Matches.
Ex 1: [2, 3, 4].
$h$: 1, 1, 2. Sum = 4. Ops = 2. Matches.

So the logic is:
1. Calculate $h(x) = \text{number of divisions by 4 to reach 0}$ for each $x$.
   $h(x) = 0$ if $x=0$ (but input $l \ge 1$).
   For $x \ge 1$, $h(x) = \lfloor \log_4 x \rfloor + 1$?
   Let's check:
   $x=1, 2, 3$: $\log_4 x < 1$, floor 0, +1 = 1. Correct.
   $x=4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15$:
   $4 \to 1 \to 0$ (2). $\log_4 4 = 1$, floor 1, +1 = 2.
   $15 \to 3 \to 0$ (2). $\log_4 15 \approx 1.95$, floor 1, +1 = 2.
   $16 \to 4 \to 1 \to 0$ (3). $\log_4 16 = 2$, floor 2, +1 = 3.
   Formula: $h(x) = \lfloor \log_4 x \rfloor + 1$.
   Alternatively, using bit length or loops. Since $x \le 10^9$, $\log_4 10^9 \approx 15$. Very small.
2. For each query $[l, r]$, we need $\sum_{i=l}^r h(i)$.
3. Result for query is $\lceil (\sum h(i)) / 2 \rceil$.
4. Sum these results.

We need to compute $\sum_{i=l}^r h(i)$ efficiently.
$h(i)$ is a step function. It is constant for ranges $[4^k, 4^{k+1}-1]$.
Range $[1, 3]$: value 1.
Range $[4, 15]$: value 2.
Range $[16, 63]$: value 3.
...
Range $[4^k, 4^{k+1}-1]$: value $k+1$.
We can precompute prefix sums of $h(i)$? No, $r$ up to $10^9$.
But the number of distinct values of $h(i)$ is small (~15).
We can calculate the sum of $h(i)$ in $[l, r]$ by iterating over the intervals defined by powers of 4.
Algorithm for sum in $[l, r]$:
Iterate $k$ from 1 upwards.
Interval $I_k = [4^k, 4^{k+1}-1]$.
Find intersection of $I_k$ with $[l, r]$.
If intersection is non-empty, add $(length) \times (k+1)$ to total.
Stop when $4^k > r$.
This is $O(\log(\max R))$ per query.
Total complexity: $O(Q \log(\max R))$. With $Q=10^5$, $\log \approx 15$, total ops $\approx 1.5 \times 10^6$, well within limits.