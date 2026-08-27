We need to compute the sum over all permutations P of (1..N) of the integer formed by concatenating the decimal strings of P_1, P_2, ..., P_N. Treat the concatenation as a decimal number; we sum it modulo MOD=998244353.

Key idea: Each position i in the concatenated decimal string corresponds to some digit d of some value P_i. The contribution of that digit d to the final sum is d * 10^{pos} where pos counts the number of digits to its right in the whole string. For a fixed permutation, the total contribution of a particular element x is x * 10^{shift(x)} where shift(x) is the total number of digits of all elements that appear after x in the permutation.

Thus sum_{permutations} f(P) = sum_{x=1..N} x * sum_{permutations} 10^{shift(x)}.

For each x, consider its decimal length L(x) = number of digits of x. When x is placed at some position in the permutation, shift(x) = total number of digits of all elements placed after x. Since each element y contributes L(y) to the shift if it is after x, and 0 if before. In permutations, the relative order of x and the other N-1 elements is uniform, and the distribution of which subset of size k appears after x (and in which order) is combinatorial.

So for a fixed x, the sum over permutations of 10^{shift(x)} depends only on the multiset of L(y) for y != x. Let cnt[d] be the number of values y in {1..N} with L(y)=d (1<=d<=maxlen). For a given x, among the other N-1 values, let a_d be how many have length d, where a_d = cnt[d] - (L(x)==d). The shift(x) is sum_{d} a_d^{(after)} * d, where a_d^{(after)} is the number of length-d values placed after x (0 <= a_d^{(after)} <= a_d). Across all permutations, the number of permutations where exactly a_d^{(after)} values of length d appear after x is: choose a_d^{(after)} from a_d, then arrange the N-1 elements (the (N-1)! permutations equally split among all (N-1)! orders relative to x). Since each relative order of the other N-1 elements is equally likely, the distribution of which subset appears after x is uniform over all 2^{N-1} subsets. Thus the probability that a particular combination (a_d^{(after)}) occurs is product_d C(a_d, a_d^{(after)}) / 2^{a_d}. The total number of permutations is N!, but the sum over permutations of 10^{shift(x)} = (N! / 2^{N-1}) * sum over all subsets T of {others} of 10^{sum_{y in T} L(y)}.

Let S = {y in {1..N}\{x}}. Then sum over all subsets T of S of 10^{sum_{y in T} L(y)} = product_{y in S} (1 + 10^{L(y)}). Because expanding the product gives each subset's weight.

Thus sum_{permutations} 10^{shift(x)} = N! * product_{y != x} (1 + 10^{L(y)}) / 2^{N-1}.

Now product over y != x of (1 + 10^{L(y)}) = (product_{y=1..N} (1 + 10^{L(y)})) / (1 + 10^{L(x)}).

Let G = product_{y=1..N} (1 + 10^{L(y)}). Then sum_{permutations} 10^{shift(x)} = N! * G / (2^{N-1} * (1 + 10^{L(x)})).

Therefore total sum = N! * G / 2^{N-1} * sum_{x=1..N} x / (1 + 10^{L(x)}).

All computations modulo MOD=998244353. We need modular inverse of 2^{N-1} and of (1+10^{L(x)}).

We can precompute powers of 10 mod MOD up to maxlen (since 10^{L(y)} only depends on length, not on y). Maxlen for N=2e5 is 6 (since 2e5 < 10^6). Actually N up to 2e5, max length 6. So we can compute pow10[d] = 10^d mod MOD.

Then for each length d, let cnt[d] = number of integers in [1..N] with exactly d digits. We can compute G = product_d (1 + pow10[d])^{cnt[d]} mod MOD.

Also, for each x, we need x * inv(1 + pow10[L(x)]) mod MOD. Sum that over x=1..N, divide by 2^{N-1} times N! (i.e., multiply by N! * inv(2^{N-1})).

So answer = N! * inv2^{N-1} % MOD * G % MOD * sum_x (x * inv(1+10^{L(x)})) % MOD.

We can precompute factorial N! and inv2 = (MOD+1)//2, then inv2^{N-1}.

Complexity O(N + maxlen) which is fine for N=2e5.

Edge cases: N=1. Then sum = 1. Let's test formula: N!=1, inv2^{0}=1, G = (1+10^1)=11, sum_x x/(1+10^1)=1/11. Then answer = 1*1*11*1/11 =1. Works.

Check sample 1: N=3. L: 1:1,2,3 all length 1 => cnt[1]=3. pow10[1]=10. 1+10=11. G = 11^3=1331. N!=6. inv2^{2}=inv4 = (MOD+1)/2^2? Let's compute: MOD=998244353, inv2=499122177. inv2^2=748683265? Actually compute: inv2^2 mod MOD. Let's do python mental: 499122177^2 mod 998244353. Since 2*inv2=1, inv2= (1/2). inv2^2 = 1/4 mod. The modular inverse of 4 is 748683265 (since 4*748683265=1 mod 998244353). So N!*inv2^{N-1} = 6 * inv4 = 6*748683265 mod. 6*748683265 = 4492099590 mod 998244353. 4492099590 - 4*998244353 = 4492099590 - 3992977412 = 499122178. Hmm 499122178? Actually 6/4 = 1.5 => 3/2? Let's compute exactly: 6 * inv4 = 6 * (MOD+1)/4? But 6/4 = 3/2, so mod inv2. So it should be 3*inv2 = 3*499122177 = 1497366531 mod 998244353. 1497366531 - 998244353 = 499122178. Yes.

Now sum_x x/(1+10) = (1+2+3)/11 = 6/11. So we need answer = (6*inv4) * G * (6*inv11). Compute: (6*inv4) = 499122178. G=1331. inv11 = modular inverse of 11 mod 998244353. 11*? =1 mod. Let's compute: 11*90849578? Actually 998244353 mod 11 = 998244353 - 11*90749486 = 998244353 - 998244346 = 7. So inverse exists. inv11 = pow(11, MOD-2, MOD). We can compute numerically later. But let's see if product gives 1332.

Compute: 499122178 * 1331 mod. 499122178*1331. Let's compute: 499122178*1000=499122178000, *300=149736653400, *30=14973665340, *1=499122178. Sum: 499122178000+149736653400=648858831400, +14973665340=663832496740, +499122178=664331618918. Now mod 998244353. 998244353*665 = 998244353*600=598946611800, *60=59894661180, *5=4991221765. Sum: 598946611800+59894661180=658841272980, +4991221765=663832494745. Subtract from 664331618918: 664331618918-663832494745=499124173. So (N!*inv2^{N-1}*G) = 499124173.

Now multiply by sum_x = 6*inv11. Need inv11. Let's compute 11*? =1 mod 998244353. Since MOD = 998244353 = 11*90749486 + 7. Using extended Euclid? But we can compute approximate: inv11 = pow(11, 998244351, MOD). Let's compute manually? Might be messy. But expected answer is 1332. So 499124173 * (6*inv11) mod should be 1332.

Compute 499124173*6 = 2994745038. Mod 998244353: 998244353*3 = 2994733059. 2994745038-2994733059=11979. So 499124173*6 mod = 11979. So answer = 11979 * inv11 mod. So inv11 should be 11979^{-1} mod such that product is 1332. 1332 * 11 = 14652. Not helpful. Let's compute inv11 manually: we need x such that 11x = 1 mod 998244353. Solve 11x - 998244353y = 1. Use extended Euclid. 998244353 mod 11 = 7. 11 mod 7 = 4. 7 mod 4 = 3. 4 mod 3 =1. 3 mod 1 =0. Back substitute: 1 = 4 - 3*1. 3 = 7 - 4*1 => 1 = 4 - (7-4) = 2*4 - 7. 4 = 11 - 7*1 => 1 = 2*(11-7) - 7 = 2*11 - 2*7 - 7 = 2*11 - 3*7. 7 = 998244353 - 11*90749486 => 1 = 2*11 - 3*(998244353 - 11*90749486) = 2*11 - 3*998244353 + 3*11*90749486 = 11*(2 + 3*90749486) - 3*998244353. 2+3*90749486 = 2 + 272248458 = 272248460. So x = 272248460 mod MOD is inverse of 11. Check: 11*272248460 = 2994733060. 2994733060 mod 998244353: subtract 998244353*3=2994733059, remainder 1. Yes. So inv11 = 272248460.

Now 11979 * 272248460 mod. 11979*272248460. Let's compute: 272248460*10000=2,722,484,600,000; *1000=272,248,460,000; *900=245,023,614,000; *70=19,057,392,200; *9=2,450,236,140. Sum for 11979 = 10000+1000+900+70+9.

Compute: 2,722,484,600,000 + 272,248,460,000 = 2,994,733,060,000.
+ 245,023,614,000 = 3,239,756,674,000.
+ 19,057,392,200 = 3,258,814,066,200.
+ 2,450,236,140 = 3,261,264,302,340.

Now mod 998,244,353. Compute quotient approx 3,261,264,302,340 / 998,244,353 ≈ 3268? Let's compute 998,244,353 * 3000 = 2,994,732,? Actually 998,244,353*3000 = 2,994,732,? Let's do: 998,244,353 * 1000 = 998,244,353,000. *3 = 2,994,732,? Actually 998,244,353 * 3 = 2,994,732,? Wait 998,244,353 * 3 = 2,994,732,? 998,244,353*2=1,996,488,706; +998,244,353 = 2,994,733,059. So *3000 = 2,994,733,059,000. Subtract from 3,261,264,302,340 gives 266,531,243,340.

Now 998,244,353 * 200 = 199,648,870,600. Subtract: 266,531,243,340 - 199,648,870,600 = 66,882,372,740.

Now *60 = 998,244,353*60 = 59,894,661,180. Subtract: 66,882,372,740 - 59,894,661,180 = 6,987,711,560.

Now *7 = 6,987,710,471. Subtract: 6,987,711,560 - 6,987,710,471 = 1,089.

So remainder is 1089. That's not 1332. Hmm something off. Let's recompute carefully.

Wait, we computed (N!*inv2^{N-1}*G) = 499124173. Then multiplied by 6 gave 11979? Actually we computed 499124173*6 = 2994745038. Mod 998244353: 998244353*3 = 2994733059. 2994745038-2994733059 = 11979. Yes.

Then answer = 11979 * inv11 mod. inv11 = 272248460. 11979*272248460 mod. Let's compute more carefully.

We can compute 272248460 * 11979.

Alternative: compute 272248460 * 12000 - 272248460*21.

272248460*12000 = 272248460 * 12 * 1000 = (272248460*12)*1000.

272248460*10 = 2,722,484,600
272248460*2 = 544,496,920
Sum = 3,266,981,520.
Times 1000 => 3,266,981,520,000.

Now 272248460*21 = 272248460*20 + 272248460*1 = 5,444,969,200 + 272,248,460 = 5,717,217,660.

Subtract: 3,266,981,520,000 - 5,717,217,660 = 3,261,264,302,340. Same as before.

Now mod 998,244,353. Let's compute using modular arithmetic or long division precisely.

Compute 3,261,264,302,340 ÷ 998,244,353.

We can compute floor division: 998,244,353 * 3268 = ?

998,244,353 * 3000 = 2,994,733,059,000.
Remaining: 3,261,264,302,340 - 2,994,733,059,000 = 266,531,243,340.

Now 998,244,353 * 200 = 199,648,870,600.
Remaining: 266,531,243,340 - 199,648,870,600 = 66,882,372,740.

Now 998,244,353 * 60 = 59,894,661,180.
Remaining: 66,882,372,740 - 59,894,661,180 = 6,987,711,560.

Now 998,244,353 * 7 = 6,987,710,471.
Remaining: 6,987,711,560 - 6,987,710,471 = 1,089.

So quotient = 3000+200+60+7 = 3267? Wait sum: 3000+200=3200, +60=3260, +7=3267. So quotient = 3267, remainder = 1,089.

But 1,089 is not 1332. Something is wrong. Let's check our calculation of G and N!*inv2^{N-1}.

N=3, N!=6. inv2^{2} = inv4. inv2 = (MOD+1)//2 = 499122177. inv4 = inv2^2 mod. Let's compute inv2^2: 499122177^2 mod 998244353. Since 2*499122177 = 998244354 = 1 mod MOD. So 499122177 = 1/2. Then (1/2)^2 = 1/4. The modular inverse of 4 is 748683265 (since 4*748683265 = 1 mod). Let's verify: 748683265*4 = 2,994,733,060. 2,994,733,060 mod 998244353: subtract 998244353*3 = 2,994,733,059, remainder 1. Yes. So inv4 = 748683265.

Now N!*inv2^{N-1} = 6 * 748683265 mod. 6*748683265 = 4,492,099,590. Mod 998,244,353: 998,244,353*4 = 3,992,977,412. Subtract: 4,492,099,590 - 3,992,977,412 = 499,122,178. So factor = 499,122,178. That's what we had: 499122178. Good.

Now G = product over y=1..N of (1 + 10^{L(y)}). For N=3, all length 1, so (1+10)^3 = 11^3 = 1331. Correct.

Now product = 499122178 * 1331 mod. Let's recompute that product carefully.

Compute 499,122,178 * 1331.

Break: 1331 = 1000 + 300 + 30 + 1.

499,122,178*1000 = 499,122,178,000.
*300 = 149,736,653,400.
*30 = 14,973,665,340.
*1 = 499,122,178.

Sum: 499,122,178,000 + 149,736,653,400 = 648,858,831,400.
Add 14,973,665,340 => 663,832,496,740.
Add 499,122,178 => 664,331,618,918.

Now mod 998,244,353.

Compute 998,244,353 * 665 = ?

998,244,353 * 600 = 598,946,611,800.
*60 = 59,894,661,180. (since 998,244,353*6=5,989,466,118, times 10)
*5 = 4,991,221,765.

Sum: 598,946,611,800 + 59,894,661,180 = 658,841,272,980.
Add 4,991,221,765 = 663,832,494,745.

Now 664,331,618,918 - 663,832,494,745 = 499,124,173. So product = 499,124,173. That matches our earlier.

Now sum_x x/(1+10) = (1+2+3)/11 = 6/11. So we need to multiply by 6 and then by inv(11). But wait, the formula says answer = (N! * inv2^{N-1} % MOD) * G % MOD * sum_x (x * inv(1+10^{L(x)})) % MOD.

Note: sum_x (x * inv(1+10^{L(x)})) is not (sum x) * inv(1+10) because inv(1+10^{L(x)}) is the same for all x (since all have L=1). So it's sum_x x * inv11 = 6 * inv11. So we multiply by 6*inv11.

But we must be careful: The sum is over x of x * inv(1+10^{L(x)}). For each x, inv(1+10^{L(x)}) is the modular inverse of (1+10^{L(x)}). Since L(x)=1, 1+10=11, inv11=272248460. So sum = 1*272248460 + 2*272248460 + 3*272248460 = 6*272248460 = 1,633,490,760. Mod: 1,633,490,760 - 998,244,353 = 635,246,407. So sum_x = 635,246,407.

Wait earlier we computed 6*inv11 = 11979? That was a mistake: 272248460*6 = 1,633,490,760. Mod 998,244,353 is 635,246,407. 11979 is 499124173*6 mod, not 6*inv11. I mistakenly used 6*inv11 = 11979? No, I used 11979 which was (N!*inv2^{N-1}*G)*6 mod. That is 6 times the factor before sum. So I incorrectly thought answer = 11979 * inv11. But correct is factor = 499,124,173, then multiply by sum_x = 635,246,407.

Compute 499,124,173 * 635,246,407 mod.

Let's compute that product mod 998,244,353. Use modular multiplication.

We can use Python mental? Let's try to compute using splitting.

Let a = 499,124,173.
b = 635,246,407.

We can compute a*b mod p.

Alternatively, compute using the fact that answer should be 1332. Let's see if product gives 1332.

Compute a*b mod p. Since numbers are large, we can try to compute using small steps.

But before that, note that we have factor = N! * inv2^{N-1} * G. For N=3, N! * inv2^{N-1} = 6/4 = 3/2. G = 11^3 = 1331. So factor = (3/2)*1331 = 3993/2. Since we are in mod, factor = 3993 * inv2 mod. 3993 * 499122177 mod. 3993*499122177 = 499122177*4000 - 499122177*7 = 1,996,488,708,000 - 3,493,855,239 = 1,992,994,852,761. Mod 998,244,353: divide by 998,244,353. 998,244,353*1996 =? Let's compute 998,244,353*2000 = 1,996,488,706,000. Subtract 998,244,353*4 = 3,992,977,412. So 1,996,488,706,000 - 3,992,977,412 = 1,992,495,728,588. Subtract from 1,992,994,852,761: 1,992,994,852,761 - 1,992,495,728,588 = 499,124,173. Yes matches.

Now sum_x = sum_{x=1..3} x/(1+10) = 6/11. So answer = factor * (6/11) = (3993/2) * (6/11) = (3993*6)/(2*11) = 23958 / 22 = 1089? Wait 23958/22 = 1089.0? 22*1089 = 23958. Yes! So answer = 1089? But expected is 1332. Something is wrong.

Wait 3993*6 = 23958. Divided by 22 = 1089. So formula gives 1089, not 1332. But sample answer is 1332. So our derived formula is missing something.

Let's re-express: f(P) is the integer formed by concatenating the decimal representations. The sum we want is sum_{P} f(P). We derived:

sum_{P} f(P) = sum_{x} x * sum_{P} 10^{shift(x)}.

For each x, shift(x) = sum_{y after x} L(y). The number of permutations where a specific subset S of other elements is after x is (N-1)! (since we fix x's position, and the order of others relative to x: we can choose any subset to be after x, and then arrange all others arbitrarily). Actually, for each permutation, x is at some position. The set of elements after x is a subset of the other N-1 elements. For each subset S of size k, the number of permutations where exactly S is after x is: choose positions for the N elements: we need x to be at position N - k (so that there are k elements after). But we are summing over all permutations, not fixing x's position. However, the total number of permutations where a specific subset S is after x (and the rest before) is: we need to interleave x with the two groups. More systematically: we have N positions. Choose which positions are occupied by S and x. Actually, consider the relative order: we have N items. For a given x, we want the set of items that appear after x. This is determined by the permutation. For each subset S of the other N-1 items, the number of permutations where S is exactly the set of items after x is: (N-1)! * C(N-1, |S|)? Let's think.

We can think of building permutation by first choosing the set of items after x, and then arranging the items before x and after x in order. There are N positions. Let k = |S|. Then x must be at position N - k (i.e., there are k items after it). The items after x are exactly S, and the items before x are the complement T = others \ S. The number of ways to arrange the items in T and S is |T|! * |S|! = (N-1-k)! * k!. So the number of permutations with S after x is (N-1-k)! * k!. Wait, is that correct? Let's test with N=3, x=1. Subsets S of {2,3}:

- S = {} (k=0): x at position 3 (last). T = {2,3} arranged in 2! = 2 ways. So permutations: (2,3,1) and (3,2,1). That's 2 = (2)! * 0! = 2. Good.
- S = {2} (k=1): x at position 2 (since one after). T = {3} arranged in 1! = 1 way. S arranged in 1! = 1 way. So permutations: (3,1,2) and (1,3,2)? Wait, we need to place x at position 2, T before, S after. So sequence: (T, x, S) = (3,1,2) or (something)? Actually T is the set of items before x. Here T = {3}. So before x we have 3. S after x we have 2. So permutation: (3,1,2). But also we could have T = {3} but order of T is fixed (only one element). So only one permutation? But there should be 2 permutations with exactly {2} after 1: (3,1,2) and (2,1,3)? Wait (2,1,3) has 3 after 1, not 2. (2,1,3): after 1 is {3}. So not that. (1,2,3) has {} after. (1,3,2) has {2} after 1? In (1,3,2), after 1 is {3,2} (size 2). (2,3,1) has {} after. (3,2,1) has {2,1}? Actually after 1 is {} because 1 is last. Wait (3,2,1): after 1 is {}. So only (3,1,2) has {2} after 1? Let's list all permutations and see which have exactly {2} after 1:

1. (1,2,3): after 1 = {2,3}
2. (1,3,2): after 1 = {3,2} same set.
3. (2,1,3): after 1 = {3}
4. (2,3,1): after 1 = {}
5. (3,1,2): after 1 = {2}
6. (3,2,1): after 1 = {}

So indeed only one permutation has exactly {2} after 1. So the count for k=1 is 1. Our formula gave (N-1-k)! * k! = (2-1)! * 1! = 1! * 1 = 1. Good.

- S = {2,3} (k=2): x at position 1. T = {} arranged in 0! = 1. S arranged in 2! = 2. Permutations: (1,2,3) and (1,3,2). That's 2. Formula: (0)! * 2! = 2. Good.

Thus the number of permutations where S is exactly the set after x is (N-1 - |S|)! * |S|!.

Now for each such permutation, the shift(x) = sum_{y in S} L(y). So the contribution to sum_{P} 10^{shift(x)} from those permutations is (N-1 - k)! * k! * 10^{sum_{y in S} L(y)}.

Thus sum_{P} 10^{shift(x)} = sum_{S subset of others} (N-1 - |S|)! * |S|! * 10^{sum_{y in S} L(y)}.

This is not simply N! * product (1+10^{L(y)}) / 2^{N-1}. Let's compute for N=3, x=1. Others = {2,3}, both length 1. L(y)=1 for each.

Compute sum_{S} (2 - |S|)! * |S|! * 10^{|S|}.

- S={}: k=0: (2)! * 0! * 10^0 = 2 * 1 * 1 = 2.
- S={2}: k=1: (1)! * 1! * 10^1 = 1 * 1 * 10 = 10.
- S={3}: same: 10.
- S={2,3}: k=2: (0)! * 2! * 10^2 = 1 * 2 * 100 = 200.

Total = 2 + 10 + 10 + 200 = 222.

Now N! * product (1+10^{L(y)}) / 2^{N-1} = 6 * (1+10)^2 / 4 = 6 * 11^2 / 4 = 6 * 121 / 4 = 726 / 4 = 181.5. Not integer. Mod inverse: 6 * 121 * inv4 = 6*121*748683265 mod. 6*121=726. 726*748683265 = 543,384,? Let's compute: 748,683,265 * 700 = 524,078,285,500; *26 = 19,465,764,890; sum = 543,544,050,390. Mod 998,244,353: 998,244,353*544 = 998,244,353*500=499,122,176,500; *40=39,929,774,120; *4=3,992,977,412; sum=499,122,176,500+39,929,774,120=539,051,950,620; +3,992,977,412=543,044,928,032. Subtract: 543,544,050,390 - 543,044,928,032 = 499,122,358. That's not 222. So the formula is wrong.

We need to correct the derivation.

We have sum_{P} 10^{shift(x)} = sum_{S subset of others} (N-1 - |S|)! * |S|! * 10^{sum_{y in S} L(y)}.

Note that (N-1 - k)! * k! = (N-1)! / C(N-1, k). Because C(N-1, k) = (N-1)! / (k! (N-1-k)!). So (N-1-k)! * k! = (N-1)! / C(N-1, k).

Thus sum_{P} 10^{shift(x)} = (N-1)! * sum_{S subset of others} 10^{sum_{y in S} L(y)} / C(N-1, |S|).

Now sum_{S subset of others} 10^{sum_{y in S} L(y)} / C(N-1, |S|) is not a simple product. However, we can write it as:

sum_{P} 10^{shift(x)} = (N-1)! * sum_{k=0}^{N-1} (1 / C(N-1, k)) * (sum over subsets of size k of 10^{sum L(y)}).

But we can also think differently: The number of permutations where a particular subset S is after x is (N-1-k)! * k!. The factor (N-1-k)! * k! is the number of ways to interleave the two groups? Actually, the number of ways to choose positions for the k elements in S after x and the N-1-k elements before x is: we need to choose the positions of S among the k positions after x, and the positions of T among the N-1-k positions before x. But the relative order within S and T is also determined. Alternatively, we can think of all permutations of N items. For a fixed x, the probability that a given other element y is after x is 1/2. But the events are not independent. The generating function for the shift is complicated.

We need to compute sum_{P} 10^{shift(x)} efficiently for all x.

Alternative approach: Consider the concatenated string as a number. The sum over permutations can be expressed by considering each digit position. However, the digits come from the decimal representations of the numbers. Since N is up to 2e5, we need O(N) or O(N log MOD) solution.

We can think of the sum as: For each permutation P, the number is formed by concatenating P_1, P_2, ..., P_N. So it's like: f(P) = sum_{i=1}^{N} P_i * 10^{sum_{j>i} L(P_j)}.

Thus sum_{P} f(P) = sum_{i=1}^{N} sum_{P} P_i * 10^{sum_{j>i} L(P_j)}.

For a fixed position i (1-indexed), we consider the set of N elements. The element at position i is some x. The sum over permutations of P_i * 10^{sum_{j>i} L(P_j)} can be computed by considering the distribution of x and the set of elements after position i.

For a fixed i, the number of permutations where x is at position i and S is the set of elements after i (size N-i) is: choose S (size N-i), arrange the elements in positions 1..i-1 (any order), and arrange S in positions i+1..N (any order). So the number is: C(N-1, N-i) * (i-1)! * (N-i)! = (N-1)! / C(N-1, i-1)? Wait: C(N-1, N-i) = C(N-1, i-1). So number = C(N-1, i-1) * (i-1)! * (N-i)! = (N-1)!.

Interesting! For any fixed i and any fixed x, the number of permutations where x is at position i is (N-1)!. Because we fix x at position i, and permute the other N-1 elements arbitrarily: (N-1)! ways. So for each i, the distribution of x at position i is uniform over all N choices.

Thus for a fixed i, sum_{P} P_i * 10^{sum_{j>i} L(P_j)} = (N-1)! * sum_{x=1}^{N} x * (1/N) * sum_{permutations of others} 10^{sum_{y after x} L(y)}? Wait, we need to be careful: When we sum over all permutations, for each permutation, P_i is some x. The sum over permutations of P_i * 10^{sum_{j>i} L(P_j)} can be written as: for each x, count how many permutations have x at position i and then multiply by x * 10^{sum_{j>i} L(P_j)} for those permutations. But the exponent depends on which elements are after i. So we need to average over the permutations of the other N-1 elements.

Alternatively, fix i. The sum over permutations of P_i * 10^{sum_{j>i} L(P_j)} = sum_{x} x * sum_{permutations where P_i = x} 10^{sum_{j>i} L(P_j)}.

Given P_i = x, the remaining N-1 elements are arranged in the other positions. The set of elements after position i is a subset of the other N-1 elements of size N-i. The number of ways to choose which N-i elements are after i is C(N-1, N-i). Then the order of the elements before i (i-1 of them) and after i (N-i of them) can be any permutation. So for a fixed set S of size N-i that are after i, the number of permutations with x at position i and S after is (i-1)! * (N-i)! (arrange the before and after sets). So the total number of permutations with x at position i is (N-1)!, as expected.

Now, for a fixed i, the sum over permutations of 10^{sum_{j>i} L(P_j)} when P_i = x is: sum_{S subset of others, |S|=N-i} (i-1)! * (N-i)! * 10^{sum_{y in S} L(y)}.

Thus sum_{P} P_i * 10^{sum_{j>i} L(P_j)} = (N-1)! * sum_{x=1}^{N} x * (1/(N-1)!) * sum_{S: |S|=N-i} (i-1)! (N-i)! 10^{sum_{y in S} L(y)}.

But note that (i-1)! (N-i)! * C(N-1, N-i) = (N-1)!. So the sum over S of size N-i of 10^{sum L(y)} times the number of permutations for that S is exactly (N-1)! times the average of 10^{sum L(y)} over subsets of size N-i? Actually, sum_{S: |S|=N-i} (i-1)! (N-i)! 10^{sum L(y)} = (i-1)! (N-i)! * sum_{S: |S|=N-i} 10^{sum L(y)}.

And sum_{P} P_i * 10^{...} = sum_{x} x * (i-1)! (N-i)! * sum_{S: |S|=N-i} 10^{sum L(y)}.

But (i-1)! (N-i)! * C(N-1, N-i) = (N-1)!. So we can write:

sum_{P} P_i * 10^{...} = (i-1)! (N-i)! * sum_{x} x * sum_{S: |S|=N-i} 10^{sum_{y in S} L(y)}.

Now sum_{S: |S|=N-i} 10^{sum L(y)} is the elementary symmetric sum of degree N-i of the numbers 10^{L(y)} for y != x. That is, for a fixed x, let the multiset of values w_y = 10^{L(y)} for y != x. Then we need the sum of products of (N-i) distinct w_y's. That is e_{N-i}({w_y: y != x}).

Thus sum_{P} P_i * 10^{...} = (i-1)! (N-i)! * sum_{x=1}^{N} x * e_{N-i}({w_y: y != x}).

Now the total sum over all i=1..N is:

Sum = sum_{i=1}^{N} (i-1)! (N-i)! * sum_{x=1}^{N} x * e_{N-i}({w_y: y != x}).

This is symmetric in a way. We can swap sums:

Sum = sum_{x=1}^{N} x * sum_{i=1}^{N} (i-1)! (N-i)! * e_{N-i}({w_y: y != x}).

For a fixed x, the inner sum is over k = N-i (number of elements after x). Let k = 0,1,...,N-1. Then i = N-k. So (i-1)! (N-i)! = (N-k-1)! * k!. So:

Sum_x = x * sum_{k=0}^{N-1} (N-k-1)! * k! * e_k({w_y: y != x}).

Where e_k is the elementary symmetric sum of degree k.

Now note that sum_{k=0}^{N-1} (N-k-1)! * k! * e_k = ?

This resembles the expansion of something. Consider the polynomial P(t) = sum_{k=0}^{N-1} e_k * t^k. But we have factorial weights.

Alternatively, consider the sum over all permutations of the other N-1 elements. The shift(x) = sum_{y after x} L(y). For each permutation of the other N-1 elements, the shift is determined. The sum over permutations of the other N-1 elements of 10^{shift(x)} is exactly what we need. And we have:

sum_{perm of others} 10^{shift(x)} = sum_{S subset of others} (N-1 - |S|)! * |S|! * 10^{sum_{y in S} L(y)}.

This is the definition. So we need to compute this efficiently.

We can think of the other N-1 elements as having associated "weights" w_y = 10^{L(y)}. Then the sum is sum_{S} (N-1 - |S|)! |S|! prod_{y in S} w_y.

This is like: let f(t) = sum_{k=0}^{N-1} (N-1-k)! k! e_k t^k. Then sum_{S} ... = f(1) with w_y included.

We can write: sum_{S} (N-1 - |S|)! |S|! prod_{y in S} w_y = (N-1)! * sum_{S} prod_{y in S} (w_y / (|S|))? Not exactly.

Alternatively, we can use generating functions: Consider the product over y != x of (1 + w_y * t). The coefficient of t^k is e_k. But we have (N-1-k)! k! multiplying e_k. So we need sum_{k} e_k * (N-1-k)! k!.

We can try to find a closed form. Note that (N-1-k)! k! = (N-1)! / C(N-1, k). So the sum is (N-1)! * sum_{k=0}^{N-1} e_k / C(N-1, k).

Thus sum_{perm of others} 10^{shift(x)} = (N-1)! * sum_{k=0}^{N-1} e_k / C(N-1, k).

Now e_k is the elementary symmetric sum of degree k of the numbers w_y = 10^{L(y)} for y != x.

This still seems complicated because e_k depends on x (since the set of w_y depends on which x is removed). But note that the values w_y depend only on L(y), i.e., on the number of digits of y. So the multiset of w_y for y != x is just the multiset of all w_y for y=1..N, with one element w_x removed.

Thus we need to compute for each x: S(x) = sum_{k=0}^{N-1} e_k^{(x)} / C(N-1, k), where e_k^{(x)} is the elementary symmetric sum of degree k of the multiset M \ {w_x}, where M = {w_y: y=1..N}.

Now M has N elements, but many are equal because w_y depends only on the length of y. Specifically, for each length d, there are cnt[d] numbers, each with w = 10^d. So M is a multiset with cnt[d] copies of w_d = 10^d.

Thus the elementary symmetric sums of M are products of (1 + w_d t)^{cnt[d]}. Let E(t) = product_{d} (1 + w_d t)^{cnt[d]} = sum_{k=0}^{N} e_k t^k, where e_k is the elementary symmetric sum of the whole set M.

Now for a fixed x with length d_x, the multiset for others is M \ {w_{d_x}}. So its generating function is E(t) / (1 + w_{d_x} t). Because removing one copy of w_{d_x} corresponds to dividing by (1 + w_{d_x} t) in the product.

Thus e_k^{(x)} is the coefficient of t^k in E(t) / (1 + w_{d_x} t).

We need to compute sum_{k=0}^{N-1} e_k^{(x)} / C(N-1, k). This sum is reminiscent of a convolution with 1/C(N-1, k). Let's define a sequence a_k = e_k^{(x)}. We need sum_{k=0}^{N-1} a_k / C(N-1, k).

We can write 1/C(N-1, k) = (k! (N-1-k)!) / (N-1)!. So sum_{k} a_k / C(N-1, k) = (1/(N-1)!) * sum_{k=0}^{N-1} a_k * k! * (N-1-k)!.

But note that a_k * k! * (N-1-k)! is exactly the term we had earlier. So we are back to the same expression.

We need to compute sum_{k} a_k * k! * (N-1-k)! efficiently.

Observe that a_k is the coefficient of t^k in A(t) = E(t) / (1 + w t) where w = w_{d_x}.

We need sum_{k=0}^{N-1} [t^k] A(t) * k! * (N-1-k)!.

This is the coefficient of something? Consider the exponential generating function. But we have ordinary generating function.

Alternatively, we can think of the sum as the value at t=1 of some series. Note that sum_{k} a_k k! (N-1-k)! = sum_{k} a_k k! (N-1-k)!.

We can write this as: sum_{k} a_k * k! * (N-1-k)! = (N-1)! * sum_{k} a_k / C(N-1, k).

We need to compute this for each x. Since N is up to 2e5, we need an O(N) or O(N log N) method.

Note that the values w_d = 10^d are small (d up to 6). The counts cnt[d] are known. So the whole multiset M is determined. We can compute the generating function E(t) = product_{d} (1 + w_d t)^{cnt[d]}. This is a polynomial of degree N. But N is 2e5, so we cannot expand it fully? Actually we can, but we need to compute for each x the sum involving e_k^{(x)}. However, we might find a closed form for the sum over all x.

Let's go back to the total sum:

Total = sum_{x=1}^{N} x * sum_{perm of others} 10^{shift(x)}.

And sum_{perm of others} 10^{shift(x)} = sum_{S subset of others} (N-1 - |S|)! |S|! 10^{sum L(y)}.

We can swap the sum over x and S. For a fixed subset S of the whole set {1..N}, how many x such that S is a subset of the others (i.e., x not in S)? For each x not in S, the contribution is x * (N-1 - |S|)! |S|! 10^{sum L(y)}. So we can write:

Total = sum_{S subset of {1..N}} (N-1 - |S|)! |S|! 10^{sum_{y in S} L(y)} * (sum_{x not in S} x).

Note that S can be any subset, including empty. When S is empty, (N-1)! * 0! = (N-1)!, and sum_{x not in empty} x = sum_{x=1}^N x = N(N+1)/2. That term corresponds to permutations where shift(x)=0 for all x? Wait, if S is empty, then for each x, the set of others after x is empty. But for a given x, S empty means no elements after x. But in permutations, can S be empty for all x simultaneously? No, because if S is empty for a particular x, that means x is last. But different x can have empty S if they are last. However, the sum over S is over subsets of the whole set, and for each S we sum over x not in S. This double counts permutations? Let's check.

Our original expression: Total = sum_{x} x * sum_{S subset of others(x)} (N-1 - |S|)! |S|! 10^{sum L(y)}.

Here others(x) is the set of all elements except x. So S is a subset of the whole set excluding x. We can extend S to be a subset of the whole set, and then x must not be in S. So:

Total = sum_{S subset of {1..N}} (N-1 - |S|)! |S|! 10^{sum_{y in S} L(y)} * (sum_{x: x not in S} x).

Yes, because for each S, and for each x not in S, we have a term. This is correct.

Now we can compute the sum over S. Note that the sum depends on S only through |S| and sum_{y in S} L(y). But also the factor (N-1 - |S|)! |S|! depends only on |S| = k. And the sum over x not in S depends on which elements are missing. Specifically, sum_{x not in S} x = total sum of all x minus sum_{y in S} y.

Let TOT = sum_{x=1}^N x = N(N+1)/2. Then sum_{x not in S} x = TOT - sum_{y in S} y.

Thus:

Total = sum_{S subset} (N-1 - k)! k! 10^{sum_{y in S} L(y)} * (TOT - sum_{y in S} y), where k = |S|.

Now we can group S by their sum of L(y) and sum of y. But these are not independent. However, we can write:

Total = TOT * sum_{S} (N-1 - k)! k! 10^{sum L(y)} - sum_{S} (N-1 - k)! k! 10^{sum L(y)} * (sum_{y in S} y).

The first term: TOT * sum_{S} (N-1 - k)! k! 10^{sum L(y)}.

The second term: sum_{S} (N-1 - k)! k! 10^{sum L(y)} * (sum_{y in S} y).

We can swap the sum over S and sum over y in the second term:

Second term = sum_{y=1}^N y * sum_{S: y in S} (N-1 - k)! k! 10^{sum_{z in S} L(z)}.

But for a fixed y, the sum over S containing y: let S = {y} U T, where T is a subset of the other N-1 elements. Then k = 1 + |T|. The term becomes:

sum_{y} y * sum_{T subset of others} (N-1 - (1+|T|))! (1+|T|)! 10^{L(y) + sum_{z in T} L(z)}.

= sum_{y} y * 10^{L(y)} * sum_{T subset of others} (N-2 - |T|)! (1+|T|)! 10^{sum_{z in T} L(z)}.

This looks similar to the original but with shifted indices.

Maybe we can find a generating function approach.

Let's define for the whole set M (with multiplicities), the sum over all subsets S of (N-1 - |S|)! |S|! 10^{sum L(y)} * f(S), where f(S) could be constant or sum y. This is like evaluating a polynomial at t=1 with factorial weights.

Consider the product over all elements y: (1 + w_y * t) where w_y = 10^{L(y)}. But we have factorial weights. We can use the identity:

(N-1 - k)! k! = coefficient of x^{N-1} in something? Or we can think of the sum as:

sum_{S} (N-1 - |S|)! |S|! prod_{y in S} w_y = (N-1)! * sum_{S} prod_{y in S} (w_y / C(N-1, |S|)). Not helpful.

Alternatively, we can use the formula for the sum over subsets with weights: sum_{S} (N-1 - |S|)! |S|! prod_{y in S} w_y = (N-1)! * [t^{N-1}] product_{y} (1 + w_y t) * something? Let's see.

We have (N-1)! * sum_{k=0}^{N-1} e_k / C(N-1, k). This is the value at t=1 of the polynomial P(t) = sum_{k=0}^{N-1} e_k * (N-1)! / C(N-1, k) * t^k? Not exactly.

We can write: sum_{k=0}^{N-1} e_k / C(N-1, k) = sum_{k=0}^{N-1} e_k * k! (N-1-k)! / (N-1)!.

Multiply both sides by (N-1)!: sum_{k=0}^{N-1} e_k k! (N-1-k)!.

Now consider the product Q(t) = sum_{k=0}^{N} e_k t^k = E(t). We need sum_{k=0}^{N-1} e_k k! (N-1-k)!.

We can try to express this as an integral. Note that k! (N-1-k)! = (N-1)! / C(N-1, k) = (N-1)! * B(k+1, N-k) * (N)? Not sure.

Alternatively, consider the convolution with factorials. We have two sequences: a_k = e_k, and b_k = k! (N-1-k)! for k=0..N-1, and 0 otherwise. Their convolution is not what we have; we have pointwise product.

But we can use generating functions: Let F(t) = sum_{k=0}^{N} e_k / k! t^k. Then e_k k! (N-1-k)! = (N-1)! * e_k / C(N-1, k). Not helpful.

Maybe we can compute the sum over all S directly using dynamic programming, since the values w_y are only of a few types. The total number of elements N is up to 2e5, but the number of distinct w values is small (max 6). So we can use polynomial multiplication modulo MOD, but we need to incorporate the factorial weights.

Wait, we need to compute sum_{S} (N-1 - |S|)! |S|! 10^{sum L(y)}. This sum depends only on the counts of each length. Let cnt[d] be the number of elements with length d. Then we need to sum over choosing some number a_d of elements from each length d, such that total k = sum a_d. The term is (N-1 - k)! k! * prod_d (w_d)^{a_d} * (number of ways to choose which elements of length d: C(cnt[d], a_d)). So:

Sum1 = sum_{a_d: 0<=a_d<=cnt[d]} (N-1 - K)! K! * prod_d C(cnt[d], a_d) * (w_d)^{a_d}, where K = sum a_d.

This is a sum over tuples (a_1,...,a_maxlen). The number of terms is product (cnt[d]+1), which is small because maxlen is 6 and cnt[d] can be large. For example, if cnt[1]=N, then product is N+1? Actually for each d, a_d can be 0..cnt[d]. If cnt[1] is large (like 2e5), the number of combinations is still cnt[1]+1 times the product for other d. So total number of combinations is at most (max possible number of lengths)^maxlen? Actually, each a_d ranges from 0 to cnt[d]. So the number of tuples is product_{d} (cnt[d]+1). For N=2e5, cnt[1] could be up to 9 (since 1-9 have length 1), cnt[2] up to 90, etc. The product (cnt[1]+1)*(cnt[2]+1)*...*(cnt[6]+1) could be large but maybe manageable? Let's estimate worst case: N=200000. The distribution of lengths: numbers 1-9: 9 numbers (len 1), 10-99: 90 numbers (len 2), 100-999: 900 numbers (len 3), 1000-9999: 9000 numbers (len 4), 10000-99999: 90000 numbers (len 5), 100000-200000: 100001 numbers (len 6). So cnt[1]=9, cnt[2]=90, cnt[3]=900, cnt[4]=9000, cnt[5]=90000, cnt[6]=100001. Then product (cnt[d]+1) = 10 * 91 * 901 * 9001 * 90001 * 100002. That's huge! So we cannot enumerate all tuples.

We need a smarter way.

We have the generating function E(t) = product_d (1 + w_d t)^{cnt[d]}. We need to compute sum_{k=0}^{N} e_k k! (N-1-k)!.

But note that k! (N-1-k)! is the coefficient of x^{N-1} in something? Actually, consider the product (1 + w_d t)^{cnt[d]}. If we differentiate or integrate, we might get factorials.

Alternatively, we can use the fact that the sum over subsets with weights can be expressed as an evaluation of a polynomial at t=1 after a transformation. Let's try to find an operator.

We have sum_{S} (N-1 - |S|)! |S|! prod_{y in S} w_y = (N-1)! * sum_{k=0}^{N-1} e_k / C(N-1, k).

Now, 1/C(N-1, k) = (N-1)! / (N-1)!? Not helpful.

We can write: e_k = coefficient of t^k in E(t). So the sum is (N-1)! * sum_{k=0}^{N-1} [t^k] E(t) * (1 / C(N-1, k)).

We can think of the sum as the value at t=1 of the series: (N-1)! * sum_{k=0}^{N-1} e_k * t^k / C(N-1, k) evaluated at t=1. But we need to evaluate it efficiently.

Maybe we can use the fact that the number of terms is small if we consider the values of L(y) directly? But N is large, and the number of distinct L(y) is at most 6. So the polynomial E(t) has degree N, but it's a product of binomials (1 + w_d t)^{cnt[d]}. We can represent E(t) as a polynomial where the coefficients are computed modulo MOD, but the degree is N (up to 2e5), which is fine. We can compute all coefficients e_k in O(N * maxlen) time using DP, since maxlen is small. For example, start with e[0]=1, and for each d, we multiply by (1 + w_d t)^{cnt[d]}. Since cnt[d] can be large, we need to efficiently update the polynomial when multiplying by (1 + w t)^m. This is like doing a binomial expansion. We can do this in O(N * maxlen) total by iterating over d and updating the array. For each d, we need to compute the new coefficients: new_e[k] = sum_{j=0}^{min(k, cnt[d])} e[k-j] * C(cnt[d], j) * (w_d)^j. This is a convolution with the binomial coefficients. Since cnt[d] can be up to 1e5, we cannot do O(N * cnt[d]). But we can use the fact that we are only interested in the final sum sum_{k=0}^{N-1} e_k / C(N-1, k), not all e_k individually. However, to compute that sum, we might need all e_k.

But note that the sum we need is over S with factor (N-1 - |S|)! |S|! w_{d_1}... So we can compute the sum directly by DP on the counts. Let's define DP over lengths. We process each length d one by one. For each d, we have cnt[d] elements with weight w_d. We need to compute the sum over all subsets of these elements of (N-1 - k)! k! prod w. But we also have the factor from the sum of x? Actually, we need to compute Total = TOT * Sum1 - Sum2, where Sum1 = sum_{S} (N-1 - k)! k! 10^{sum L(y)} and Sum2 = sum_{S} (N-1 - k)! k! 10^{sum L(y)} * (sum_{y in S} y).

We can compute Sum1 and Sum2 using DP over the lengths, because the weights w_d = 10^d are small (mod MOD), and the factor (N-1 - k)! k! depends on k. Also, for Sum2, we need to multiply by the sum of the actual values y, not just their lengths. But y is not determined solely by length; it depends on the specific number. However, we can group by length: for length d, the sum of y for all y in that length group is known. But in Sum2, we need to sum over S, and for each y in S, we multiply by y. So we can write:

Sum2 = sum_{d} sum_{y: L(y)=d} y * sum_{S: y in S} (N-1 - k)! k! 10^{sum L(z)}.

For a fixed y, the sum over S containing y is similar to Sum1 but for the set including y. Specifically, let the whole set be M. For a fixed y, we need to sum over subsets S that contain y. Let S = {y} U T, where T is a subset of M \ {y}. Then k = 1 + |T|. The term is (N-1 - (1+|T|))! (1+|T|)! 10^{L(y) + sum_{z in T} L(z)} = (N-2 - |T|)! (1+|T|)! 10^{L(y)} 10^{sum_{z in T} L(z)}.

Thus Sum2 = sum_{y} y * 10^{L(y)} * sum_{T subset of M\{y}} (N-2 - |T|)! (1+|T|)! 10^{sum_{z in T} L(z)}.

This still seems complicated.

Maybe we can find a closed form for the total sum by considering the contribution of each element in a different way.

Let's go back to the original expression:

Total = sum_{P} f(P) = sum_{P} sum_{i=1}^N P_i * 10^{sum_{j>i} L(P_j)}.

We can think of building the permutation from left to right. When we place an element x at the current position, its contribution is x * 10^{remaining length}, where remaining length is the total number of digits of all elements not yet placed. The remaining length is a random variable depending on the set of elements already placed.

Alternatively, we can use linearity of expectation in a different way: For each element x, its contribution to the total sum over all permutations is x * sum_{P} 10^{shift(x)}. And we need to compute sum_{P} 10^{shift(x)}.

We can compute sum_{P} 10^{shift(x)} by considering the process of generating a random permutation. The shift(x) is the sum of L(y) over y that appear after x. This is equivalent to: take a random permutation, find the position of x, then the shift is the sum of lengths of elements after it.

We can think of the permutation as a random ordering. The distribution of the set of elements after x is uniform over all subsets of the other N-1 elements, but with varying probabilities? Actually, as we derived earlier, the number of permutations where a specific subset S is after x is (N-1 - |S|)! |S|!. This is not uniform over subsets. The probability of S is (N-1 - |S|)! |S|! / N!. So it's not uniform; larger subsets have higher probability? Wait, (N-1 - k)! k! is largest when k is around (N-1)/2. So subsets of size about N/2 are more likely to be the set of elements after x? That seems counterintuitive. Let's check with N=3, x=1. Probabilities: k=0: (2)! 0! / 6 = 2/6 = 1/3. k=1: (1)! 1! / 6 = 1/6 each, but there are C(2,1)=2 subsets, so total probability for size 1 is 2*(1/6)=1/3. k=2: (0)! 2! / 6 = 2/6 = 1/3. So each size has equal probability 1/3. And among size 1, each subset has probability 1/6. So the distribution of the size of S is uniform? For N=3, yes. For N=4, let's compute: x fixed, N-1=3 others. Number of permutations total 24. For a given S of size k, number of permutations with S after x: (3-k)! k!. So probabilities: k=0: 3! 0! /24 = 6/24=1/4. k=1: 2! 1! /24 = 2/24=1/12 per subset, total for size 1: 3*(1/12)=1/4. k=2: 1! 2! /24 = 2/24=1/12 per subset, total: 3*(1/12)=1/4. k=3: 0! 3! /24 = 6/24=1/4. So again uniform over size! In fact, sum_{S: |S|=k} (N-1-k)! k! = C(N-1, k) (N-1-k)! k! = (N-1)!. So the total probability for size k is (N-1)! / N! = 1/N. So the size of S is uniformly distributed from 0 to N-1. And given size k, the specific subset is uniformly chosen among all C(N-1, k) subsets. So the distribution of the set S is: first choose k uniformly from 0 to N-1, then choose a subset of size k uniformly. This is exactly the distribution of a random subset where each element is independently included with probability 1/2? Not exactly, because the size is uniform, not binomial. But it's a symmetric distribution: each element is equally likely to be in S with probability 1/2, and the events are not independent but the marginal probability is 1/2. However, the sum of independent indicators with p=1/2 is binomial, not uniform. So it's a different distribution. But note: for each element y != x, the probability that y is in S is 1/2, because for any specific y, the number of permutations with y in S is: total permutations where y is after x. Since by symmetry, half of the permutations have y after x, half before. So marginal probability is 1/2. And the distribution is exchangeable. But the joint distribution is not independent.

However, for computing the sum of 10^{sum L(y)} over this distribution, we can use the fact that the probability generating function is:

E[ 10^{sum L(y) y in S} ] = sum_{S} Prob(S) 10^{sum L(y)} = (1/N!) * sum_{S} (N-1-|S|)! |S|! 10^{sum L(y)}.

But we already have that.

Maybe we can compute the sum over all permutations by considering the process of inserting elements one by one. There is a known trick for similar problems: the sum of f(P) over all permutations can be computed by considering each element's contribution as if it is placed in the concatenation, but the shift is not independent.

Wait, we can use the following approach: For each element x, its contribution to the total sum is x * 10^{shift(x)}. If we think of the concatenation as a string, the shift(x) is the number of digits to the right of x. We can compute the total sum of 10^{shift(x)} over all permutations by considering the relative order of x and all other elements. For each other element y, whether y is after x or before x affects the shift by L(y). So 10^{shift(x)} = product_{y != x} 10^{L(y) * I(y after x)}. So sum_{P} 10^{shift(x)} = sum_{P} product_{y != x} 10^{L(y) * I(y after x)}.

Now, the indicator I(y after x) depends on the relative order of x and y. In a random permutation, the events I(y after x) are not independent, but we can use the fact that the sum over permutations of a product of terms that depend on relative orders can be computed by considering all possible orderings of the pairs? Not directly.

But note that for each y, the term 10^{L(y) I(y after x)} can be written as: 1 + (10^{L(y)} - 1) * I(y after x). Then the product over y of (1 + (10^{L(y)} - 1) I(y after x)). Expanding, we get sum_{S subset of others} prod_{y in S} (10^{L(y)} - 1) * I(all y in S are after x). Then summing over permutations, we need to sum over permutations the indicator that all y in S are after x. The number of permutations where a specific set S is entirely after x is: we need S to be after x, but the order among S and the other elements (T = others \ S) can be anything as long as S is after x. The number of such permutations is: we can arrange the N elements such that x comes before all elements in S. The number of permutations where x precedes every element in S is: (N-1)! / 2^{|S|}? Actually, for a fixed set S, the number of permutations where x is before all y in S is: total permutations where x is before each y in S. Since the relative order of x and each y in S is independent? No, they are not independent. But we can count: we need to arrange the N elements such that x is before every y in S. The number of such permutations is: fix the set S, and require that in the permutation, x appears before each y in S. The other elements (T) can be anywhere. The number of permutations with this condition is: N! / (|S|+1) ? Actually, by symmetry, the probability that x is before all elements in S is 1/(|S|+1). Because among the |S|+1 elements {x} U S, all orders are equally likely, and x is first in 1/(|S|+1) of them. The other elements in T are independent. So the number of permutations where x is before all y in S is N! / (|S|+1). But wait, we also need the condition that the elements in S are after x, but they don't have to be in any particular order among themselves. So yes, the number is N! / (|S|+1). However, we also need the condition that the elements in T can be before or after x? In our indicator, we only require that all y in S are after x. There is no condition on T. So indeed, the number of permutations where S is a subset of the elements after x (but not necessarily exactly S) is: we need x to be before every element in S. The other elements (T) can be anywhere. The number of such permutations is: N! / (|S|+1). Because among the elements {x} U S, there are |S|+1 elements, and we require x to be the first among them. The relative order of the other N-1-|S| elements (T) is unrestricted, and their relative order with S and x? Actually, we have to consider the full permutation. The condition is: for all y in S, x appears before y. This is equivalent to: in the relative order of the |S|+1 elements {x} U S, x is the earliest. The probability is 1/(|S|+1). Since all permutations are equally likely, the number is N! / (|S|+1). This is correct.

Thus, for a fixed S, the sum over permutations of I(all y in S are after x) = N! / (|S|+1).

But in our product expansion, we have I(all y in S are after x), not I(S is exactly the set after x). The indicator that all y in S are after x is different from the indicator that S is exactly the set after x. The latter implies the former, but not vice versa. So we cannot directly use this.

We need to be careful: In the expansion, we have product_{y} (1 + (w_y - 1) I(y after x)). When we expand, we get sum_{S} prod_{y in S} (w_y - 1) * I(all y in S are after x). This indicator is 1 if every y in S is after x, regardless of other elements. So the sum over permutations of this product is sum_{S} prod_{y in S} (w_y - 1) * (N! / (|S|+1)).

Thus sum_{P} 10^{shift(x)} = sum_{P} prod_{y != x} (1 + (w_y - 1) I(y after x)) = sum_{S subset of others} prod_{y in S} (w_y - 1) * (N! / (|S|+1)).

So sum_{P} 10^{shift(x)} = N! * sum_{S subset of others} prod_{y in S} (w_y - 1) / (|S|+1).

Now, w_y = 10^{L(y)}. So w_y - 1 = 10^{L(y)} - 1. Let's denote v_y = 10^{L(y)} - 1.

Then sum_{P} 10^{shift(x)} = N! * sum_{S subset of others} prod_{y in S} v_y / (|S|+1).

Now, this sum is much nicer! Because the factor depends only on |S|, not on the specific elements in S, and the product depends on the multiset of v_y. And we can write:

sum_{S subset of others} prod_{y in S} v_y / (|S|+1) = sum_{k=0}^{N-1} (1/(k+1)) * (sum over subsets of size k of prod v_y).

The sum over subsets of size k of prod v_y is the elementary symmetric sum e_k of the v_y for y != x.

So we have: sum_{P} 10^{shift(x)} = N! * sum_{k=0}^{N-1} e_k^{(x)} / (k+1), where e_k^{(x)} is the elementary symmetric sum of degree k of {v_y: y != x}.

Now, v_y = 10^{L(y)} - 1. Note that v_y depends only on L(y). So again, the multiset of v_y is determined by the counts of lengths.

We can define a generating function for the v_y: let F(t) = product_{y} (1 + v_y t) = product_{d} (1 + (10^d - 1) t)^{cnt[d]}. Then the elementary symmetric sums of the whole set are the coefficients of F(t). For a fixed x with length d_x, the set for others is F(t) / (1 + (10^{d_x} - 1) t).

Thus e_k^{(x)} = [t^k] F(t) / (1 + (10^{d_x} - 1) t).

So sum_{P} 10^{shift(x)} = N! * sum_{k=0}^{N-1} (1/(k+1)) * [t^k] (F(t) / (1 + (10^{d_x} - 1) t)).

Now, sum_{k=0}^{N-1} (1/(k+1)) a_k = (1/t) * sum_{k=0}^{N-1} a_k t^{k+1} / (k+1) = (1/t) * integral_0^t F(s) / (1 + v_x s) ds, where v_x = 10^{d_x} - 1.

More precisely, if A(t) = F(t) / (1 + v_x t) = sum_{k=0}^{N-1} e_k^{(x)} t^k, then sum_{k=0}^{N-1} e_k^{(x)} / (k+1) = (1/t) * integral_0^t A(s) ds evaluated at t=1? Actually, the sum from k=0 to infinity of a_k / (k+1) is equal to (1/t) * \int_0^t A(s) ds if we consider the series expansion. But we have a finite sum up to N-1. However, since A(t) is a polynomial of degree N-1, we can write:

\sum_{k=0}^{N-1} \frac{e_k^{(x)}}{k+1} = \int_0^1 A(t) dt.

Because \int_0^1 A(t) dt = \int_0^1 \sum_{k=0}^{N-1} e_k^{(x)} t^k dt = \sum_{k=0}^{N-1} e_k^{(x)} / (k+1).

So we have: sum_{P} 10^{shift(x)} = N! * \int_0^1 A(t) dt, where A(t) = F(t) / (1 + v_x t), and F(t) = \prod_{y=1}^N (1 + v_y t).

Thus, the total sum over all x is:

Total = \sum_{x=1}^N x \cdot N! \cdot \int_0^1 \frac{F(t)}{1 + v_x t} dt.

We can swap sum and integral:

Total = N! \cdot \int_0^1 F(t) \cdot \left( \sum_{x=1}^N \frac{x}{1 + v_x t} \right) dt.

Now, F(t) = \prod_{y=1}^N (1 + v_y t). The sum inside is over x. Note that v_x = 10^{L(x)} - 1 depends only on the length of x. So we can group by length. Let cnt[d] be the number of elements with length d, and let v_d = 10^d - 1. Also, for each length d, the sum of x for x in that length group is sum_{x: L(x)=d} x. We can precompute this sum for each d.

Then:

\sum_{x=1}^N \frac{x}{1 + v_x t} = \sum_{d} \frac{1}{1 + v_d t} \sum_{x: L(x)=d} x.

Let S_d = \sum_{x: L(x)=d} x. Then the sum is \sum_{d} \frac{S_d}{1 + v_d t}.

Thus:

Total = N! \cdot \int_0^1 F(t) \cdot \sum_{d} \frac{S_d}{1 + v_d t} dt.

Now, F(t) = \prod_{d} (1 + v_d t)^{cnt[d]}.

So the integrand is:

G(t) = \prod_{d} (1 + v_d t)^{cnt[d]} \cdot \sum_{d} \frac{S_d}{1 + v_d t}.

We can simplify: \frac{(1 + v_d t)^{cnt[d]}}{1 + v_d t} = (1 + v_d t)^{cnt[d]-1}. So we can write:

G(t) = \sum_{d} S_d \cdot (1 + v_d t)^{cnt[d]-1} \cdot \prod_{d' \neq d} (1 + v_{d'} t)^{cnt[d']}.

That is, for each d, we have a product over all lengths, with the exponent for length d reduced by 1.

So G(t) = \sum_{d} S_d \cdot H_d(t), where H_d(t) = (1 + v_d t)^{cnt[d]-1} \cdot \prod_{d' \neq d} (1 + v_{d'} t)^{cnt[d']}.

Now, we need to compute the integral from 0 to 1 of G(t) dt modulo MOD. Since MOD is a prime, we can compute the integral as a formal power series? But we need the definite integral from 0 to 1. In modulo arithmetic, we can treat the integral as the evaluation of the antiderivative at 1 and 0. If we can find a polynomial or rational function that is the antiderivative of G(t), we can evaluate it at t=1.

But G(t) is a product of polynomials of the form (1 + v t)^m. These are easy to integrate. Specifically, \int (1 + v t)^m dt = (1/(v (m+1))) (1 + v t)^{m+1} + constant, provided v != 0 and m+1 != 0 mod MOD. But note that v = 10^d - 1. For d=1, v=9, not zero. For d=0? d>=1. So v is nonzero mod MOD (since MOD is large prime, and 10^d != 1 mod MOD for small d? Actually, 10^d could be congruent to 1 mod MOD for some d, but since MOD = 998244353, and 10 is a primitive root? Not sure, but likely 10^d != 1 for d up to 6. We can check: 10^1=10, 10^2=100, 10^3=1000, 10^4=10000, 10^5=100000, 10^6=1000000. None of these are 1 mod 998244353. So v_d != 0.

Thus, for each term H_d(t), which is a product of powers of linear terms, we can integrate it term by term. But H_d(t) is a polynomial in t (or a rational function? Actually, (1 + v t)^{cnt[d]-1} is a polynomial if cnt[d]-1 is non-negative. Since cnt[d] can be 0, then (1+v t)^{-1} is a rational function. But cnt[d] is at least 1 for the d that appear? Actually, for a given d, cnt[d] could be 0. But in the sum over d, we only include d with cnt[d] > 0. And S_d is the sum of x for that d, so if cnt[d]=0, S_d=0, so we can skip. So for d in the sum, cnt[d] >= 1. Then cnt[d]-1 >= 0, so (1+v_d t)^{cnt[d]-1} is a polynomial. The other factors are also polynomials with nonnegative exponents. So H_d(t) is a polynomial! Because all exponents are nonnegative integers. So G(t) is a polynomial in t. Its degree is sum_{d} (cnt[d]-1) * 1? Actually, the degree of (1+v t)^m is m. So the degree of H_d(t) is: (cnt[d]-1) + sum_{d' != d} cnt[d'] = (sum_{d'} cnt[d']) - 1 = N - 1. So G(t) is a polynomial of degree at most N-1.

We can expand G(t) as a polynomial, and then compute the integral from 0 to 1 as the sum of coefficients divided by (k+1). But expanding a product of many terms (up to N terms) is too expensive. However, since the polynomial is a product of only maxlen distinct factors, each raised to a power, we can represent it efficiently as a product of polynomials. But we need to compute the integral of the sum of such products. The integral of a product of powers of linear terms can be computed using the fact that:

\int_0^1 (1 + v_1 t)^{a_1} (1 + v_2 t)^{a_2} ... dt.

This is a linear combination of terms of the form (1 + v t)^{A} evaluated at 1, divided by something. But there is no simple closed form unless the v's are related.

Wait, we can use the fact that the integral of a product of powers of linear terms is a hypergeometric function, but we need to compute it exactly modulo a prime. Since the degree N can be 2e5, we need an O(N) or O(N log N) algorithm.

But note that the polynomial G(t) is a sum of at most maxlen terms (since sum over d). Each term H_d(t) is a product of (1 + v_{d'} t)^{cnt[d']} for all d', with one factor having exponent reduced by 1. So we can compute the integral of each H_d(t) separately.

For a single H_d(t), it is of the form \prod_{d'} (1 + v_{d'} t)^{c_{d'}} where the exponents c_{d'} are nonnegative integers summing to N-1. This is a polynomial. We can compute its coefficients by dynamic programming, but the degree is N-1, and the number of terms is product of (c_{d'}+1)? That's huge. However, we can compute the integral of H_d(t) without expanding it fully, by using the fact that the integral of a product of powers of linear terms can be expressed as a sum over subsets of the roots? There is a known method: if we have a polynomial P(t) = \prod_{i=1}^m (1 + a_i t)^{e_i}, then the integral from 0 to 1 is \sum_{S \subseteq \{1..m\}} (-1)^{|S|} \prod_{i \in S} \frac{1}{a_i} \frac{1}{(\sum_{i \in S} e_i + 1)}? Not exactly.

Actually, we can use partial fractions. Since the factors are distinct linear terms (v_d are distinct mod MOD, as 10^d - 1 are distinct for d=1..6? Let's check: v_1=9, v_2=99, v_3=999, v_4=9999, v_5=99999, v_6=999999. They are all distinct mod MOD. So the polynomial H_d(t) has distinct linear roots: t = -1/v_{d'} for each d'. So we can write H_d(t) as a sum of partial fractions: \sum_{d'} \frac{A_{d'}}{1 + v_{d'} t} * something? Actually, since it's a polynomial, not a rational function, the partial fraction decomposition will have numerators that are constants. Specifically, for a polynomial P(t) = \prod_{d'} (1 + v_{d'} t)^{c_{d'}}, we can write:

P(t) = \sum_{d'} P_{d'}(t) \cdot (1 + v_{d'} t)^{c_{d'}}? Not helpful.

Alternatively, we can compute the integral by expanding the polynomial as a power series and summing the coefficients divided by (k+1). But we need to compute the sum of e_k / (k+1) for the polynomial H_d(t). That is exactly the same problem we started with! So we are back to square one.

We need a different approach.

Let's reconsider the original sum: sum_{P} f(P). We can think of f(P) as a number. There is a known technique for summing concatenations of numbers over permutations: the sum can be computed by considering each digit position. But here the numbers are not single digits; they have varying lengths.

Maybe we can use the fact that the sum over permutations of the concatenation is equal to the sum over all ways to interleave the numbers? Not exactly.

Another idea: The sum of f(P) over all permutations can be expressed as the sum over all ways to order the numbers, of the number formed. We can compute this by considering the contribution of each number to the total sum, but the shift is not simply N! / 2^{N-1} times something because the events are not independent.

Wait, we had the expression with the integral: Total = N! \int_0^1 F(t) \sum_d \frac{S_d}{1 + v_d t} dt. This is promising. We need to compute this integral efficiently. Since F(t) is a product of (1 + v_d t)^{cnt[d]}, and we multiply by a sum of rational functions, the integrand is a rational function. Specifically, the integrand is:

G(t) = \sum_d S_d \frac{\prod_{d'} (1 + v_{d'} t)^{cnt[d']}}{1 + v_d t} = \sum_d S_d (1 + v_d t)^{cnt[d]-1} \prod_{d' \neq d} (1 + v_{d'} t)^{cnt[d']}.

This is a polynomial. We need to compute \int_0^1 G(t) dt.

We can compute the integral of a polynomial by summing its coefficients divided by (k+1). So if we can compute the coefficients of G(t), we can compute the integral. But G(t) is a sum of at most 6 terms (since maxlen=6). Each term is a product of powers of linear terms. We can compute the coefficients of each term by multiplying the polynomials. But the product of all these factors is of degree N, which is 2e5. We can multiply them efficiently because the number of distinct factors is small. We can compute the polynomial P(t) = \prod_{d} (1 + v_d t)^{cnt[d]} using a divide-and-conquer multiplication? But cnt[d] can be up to 1e5, and the polynomial degree is N. We can compute its coefficients in O(N * maxlen) time using the fact that (1 + v t)^m can be expanded using binomial coefficients, and we can convolve. But the degree is 2e5, and we have up to 6 different v's. We can compute the coefficients of P(t) iteratively: start with P_0(t)=1. For each d, we need to multiply P_{d-1}(t) by (1 + v_d t)^{cnt[d]}. This is a polynomial of degree up to N, and we multiply by a polynomial of degree cnt[d]. We can do this in O(N * cnt[d])? That would be too slow because sum cnt[d] = N, so O(N^2). But we can use the fact that the multiplication is by a sparse polynomial? (1 + v_d t)^{cnt[d]} has all coefficients nonzero, so it's dense. We need a faster method.

However, we don't need the full polynomial P(t). We need the integral of P(t) / (1 + v_d t) for each d. That is the same as the integral of P(t) * (1 + v_d t)^{-1}. Since P(t) has the factor (1 + v_d t)^{cnt[d]}, the division reduces the exponent by 1, making it a polynomial. So we are integrating a polynomial that is very similar to P(t), just with one factor's exponent reduced by 1. So if we can compute the coefficients of P(t), we can easily get the coefficients of each H_d(t) by reducing the exponent of (1 + v_d t) by 1, which means we can compute the coefficients of H_d(t) from the coefficients of P(t) by polynomial division? Actually, if we have the coefficients of P(t) = (1 + v_d t)^{cnt[d]} * Q_d(t), where Q_d(t) = \prod_{d' \neq d} (1 + v_{d'} t)^{cnt[d']}, then H_d(t) = (1 + v_d t)^{cnt[d]-1} * Q_d(t) = P(t) / (1 + v_d t). So we can compute the coefficients of H_d(t) by performing polynomial division of P(t) by (1 + v_d t). That is O(N) for each d, so O(N * maxlen). That is fine!

So the plan is:

1. Compute the polynomial P(t) = \prod_{d} (1 + v_d t)^{cnt[d]}, where v_d = 10^d - 1, and cnt[d] is the number of integers in [1..N] with exactly d digits. We need the coefficients of P(t) modulo MOD. P(t) has degree N.

2. For each d, compute the coefficients of H_d(t) = P(t) / (1 + v_d t). This is a polynomial of degree N-1. We can do this by polynomial division: since (1 + v_d t) is a linear factor, we can compute the quotient coefficients efficiently. Specifically, if P(t) = \sum_{k=0}^N p_k t^k, then H_d(t) = \sum_{k=0}^{N-1} h_k t^k, with the relation: (1 + v_d t) H_d(t) = P(t). So p_k = h_k + v_d h_{k-1} (with h_{-1}=0). Thus we can solve for h_k recursively: h_k = p_k - v_d h_{k-1}. So we can compute the coefficients of H_d(t) in O(N) time given p_k.

3. Then, the integral of H_d(t) from 0 to 1 is \sum_{k=0}^{N-1} h_k / (k+1). We can compute this sum modulo MOD. Note that we need to compute division by (k+1) modulo MOD, so we need the modular inverse of (k+1) for k=0..N-1. We can precompute inv[k] for k=1..N.

4. Then, Total = N! \cdot \sum_d S_d \cdot ( \int_0^1 H_d(t) dt ) mod MOD.

But wait, is that correct? Let's check the derivation.

We had: Total = N! \int_0^1 F(t) \sum_d \frac{S_d}{1 + v_d t} dt, with F(t) = P(t). And F(t) / (1 + v_d t) = H_d(t). So indeed, \int_0^1 F(t) / (1 + v_d t) dt = \int_0^1 H_d(t) dt. So Total = N! \sum_d S_d \int_0^1 H_d(t) dt.

Thus, if we can compute the coefficients of P(t), we can compute the integral for each d.

Now, we need to compute P(t) = \prod_{d} (1 + v_d t)^{cnt[d]} efficiently. Since v_d are constants (v_d = 10^d - 1 mod MOD), and cnt[d] are known. The degree of P(t) is N. We can compute its coefficients using the fact that we are multiplying polynomials of the form (1 + v t)^m. We can do this by iterating over d and using the fact that (1 + v_d t)^{cnt[d]} can be expanded using binomial coefficients. But cnt[d] can be large, so we need an efficient way to multiply by a binomial expansion.

We can use the property that (1 + v t)^m = \sum_{j=0}^m C(m, j) v^j t^j. So if we have the current polynomial P_curr(t) of degree up to current sum, and we multiply by (1 + v t)^{cnt[d]}, we need to compute the new coefficients: P_new[k] = \sum_{j=0}^{\min(k, cnt[d])} P_curr[k-j] * C(cnt[d], j) * v^j.

This is a convolution with a sequence of length cnt[d]+1. Since we do this for each d, and the total sum of cnt[d] is N, the total work if done naively is O(N^2). But we can do better because the sequences are of the form binomial coefficients. There is a known trick: we can use the fact that the product of binomials can be computed using the fact that the generating function is product_d (1 + v_d t)^{cnt[d]}. We can compute the coefficients by iterating over d and using the fact that we are multiplying by a polynomial that is a power of a linear term. We can use the following: if we have a polynomial A(t), and we want to multiply by (1 + v t)^m, we can do this in O(m * deg(A))? Not good.

But note that the number of distinct d is only 6. So we can use the fact that the polynomial is a product of 6 binomials raised to powers. We can compute the coefficients by first computing the polynomial for each d separately? Actually, we can compute the full polynomial by multiplying the 6 polynomials (each of degree cnt[d]) using FFT or NTT? Since N is 2e5, we can use NTT for polynomial multiplication. The total degree is N, and we have 6 factors. We can multiply them in a balanced way using NTT. Each multiplication of two polynomials of degree up to N takes O(N log N) using NTT. So 5 multiplications (since 6 factors) would take O(6 N log N), which is fine. However, we need to compute the coefficients modulo MOD=998244353, which is NTT-friendly. So we can use NTT to multiply the polynomials.

But we need to be careful: the factors are (1 + v_d t)^{cnt[d]}. We can compute the coefficients of each factor using the binomial expansion: it's a polynomial of degree cnt[d] with coefficients C(cnt[d], j) * v_d^j. We can compute these coefficients in O(cnt[d]) time for each d. Then we have 6 polynomials, each of length cnt[d]+1. We need to multiply them to get P(t). We can do this by multiplying them pairwise using NTT. Since the sum of degrees is N, the final polynomial has degree N. The total time is O(N log N) for each multiplication, but we can do it in a tree fashion: multiply the two smallest first, etc. Since there are only 6, we can just do sequential multiplication: multiply P by the next factor. The degree grows to N. The first multiplication: degree of first factor is cnt[d1], second is cnt[d2]. The product has degree cnt[d1]+cnt[d2]. Then multiply by next, etc. Each multiplication is NTT of two polynomials whose degrees sum to at most N. The cost of each NTT is O(N log N) if we always pad to the next power of two? Actually, if we do it naively, the second multiplication will involve a polynomial of degree up to the sum so far, and the new factor of degree cnt[next]. The product degree increases. The total work is sum_{i} O( (deg_so_far + cnt[next]) log (deg_so_far + cnt[next]) ). Since deg_so_far increases, the total could be O(6 N log N). That's fine.

Alternatively, we can compute the coefficients of P(t) using a DP that is O(N * maxlen) by using the fact that the binomial coefficients can be updated iteratively. For each d, we need to multiply the current polynomial by (1 + v_d t)^{cnt[d]}. We can do this by applying the binomial expansion as a convolution, but we can use the fact that the coefficients of (1 + v t)^m are proportional to binomial coefficients. We can use the fact that the sequence C(m, j) v^j can be generated. But the convolution with a general polynomial of length up to N would take O(N * m). However, we can use the fact that we are doing this for each d, and the total sum of m is N, so if we do it naively, it's O(N^2). But we can use the fact that the polynomial we are multiplying by is "simple" in the sense that it is a power of a linear term. There is a way to multiply by (1 + v t)^m using O(m) operations? Not if the other polynomial is arbitrary.

Given that N is only 2e5, and maxlen is 6, O(N^2) is too slow. O(N log N) with NTT is definitely fast enough. So we will use NTT to multiply the polynomials.

We need to implement NTT for modulo 998244353. The standard NTT with primitive root 3 works.

So steps:

- Precompute v_d = (pow(10, d, MOD) - 1) % MOD for d=1..6.
- For each d from 1 to 6, compute cnt[d] = number of integers in [1..N] with exactly d digits. We can compute the range: for d=1, 1..9; d=2, 10..99; etc. But for N=2e5, we can compute by loops or using formulas.
- Compute the polynomial A_d(t) = (1 + v_d t)^{cnt[d]} mod MOD. That is, coefficients a_{d,j} = C(cnt[d], j) * v_d^j mod MOD for j=0..cnt[d]. We can compute these coefficients in O(cnt[d]) time by iteratively multiplying: start with 1, then for j from 1 to cnt[d], a_{d,j} = a_{d,j-1} * (cnt[d] - j + 1) / j * v_d mod MOD.
- Now we have up to 6 polynomials (some may be just [1] if cnt[d]=0). Multiply them all together to get P(t) = product A_d(t). We can do this by multiplying the polynomials in pairs using NTT. Since the number of polynomials is small, we can use a list and repeatedly multiply the two smallest? Or just multiply sequentially: P = A_{d1} * A_{d2} * ... . But we need to be careful with the order to minimize the total degree of intermediate polynomials. A simple way: put all A_d in a list, and while more than one, take the two with smallest degree, multiply, and push back. This is O(N log N) total.
- After obtaining P(t) = \sum_{k=0}^N p_k t^k.
- For each d with cnt[d] > 0, compute H_d(t) = P(t) / (1 + v_d t). We can compute its coefficients h_{d,k} for k=0..N-1 using the recurrence: h_{d,0} = p_0; then for k=1..N: h_{d,k} = p_k - v_d * h_{d,k-1} mod MOD. (This is from p_k = h_{d,k} + v_d h_{d,k-1}).
- Then compute integral_d = \sum_{k=0}^{N-1} h_{d,k} * inv[k+1] mod MOD, where inv[k+1] is the modular inverse of k+1.
- Precompute S_d = sum of all x in [1..N] with exactly d digits. We can compute S_d by summing the numbers in that range.
- Compute Total = N! * sum_d (S_d mod MOD) * integral_d mod MOD.
- Precompute factorial N! mod MOD.

Let's verify with N=3.

N=3. cnt[1]=3. Other cnt=0. v_1 = 10-1=9. A_1(t) = (1+9t)^3 = 1 + 27t + 243t^2 + 729t^3. So P(t) = 1 + 27t + 243t^2 + 729t^3.

S_1 = 1+2+3=6.

Compute H_1(t) = P(t)/(1+9t). Using recurrence: p = [1,27,243,729]. v=9.
h0 = p0 = 1.
h1 = p1 - 9*h0 = 27 - 9 = 18.
h2 = p2 - 9*h1 = 243 - 9*18 = 243 - 162 = 81.
h3 = p3 - 9*h2 = 729 - 9*81 = 729 - 729 = 0. So h3=0, but we only need up to N-1=2? Actually degree N-1=2, so h0,h1,h2.

Integral_1 = h0/1 + h1/2 + h2/3 = 1 + 18/2 + 81/3 = 1 + 9 + 27 = 37.

Then Total = N! * S_1 * Integral_1 = 6 * 6 * 37 = 1332. Yes! That matches the sample.

So the method works!

Now we need to handle general N up to 2e5. The steps are clear.

Implementation details:

- MOD = 998244353.
- Primitive root g = 3 for NTT.
- We need NTT multiplication. Since the polynomial degrees can be up to N, and we need to multiply several polynomials, we can write a function multiply(poly1, poly2) that returns the product polynomial using NTT. We need to pad to a power of 2 for the convolution length. The product length is len1+len2-1. We can pad to the next power of 2 greater than len1+len2-1.
- We need to compute binomial coefficients efficiently for the initial polynomials. Since cnt[d] can be up to 1e5, we can compute the coefficients of A_d by iterating: start with 1, then for j=1 to cnt[d], next = current * (cnt[d] - j + 1) % MOD * inv(j) % MOD * v_d % MOD. We need inv(j) for j=1..N, so precompute all inverses up to N.
- Alternatively, we can compute the coefficients using the fact that A_d(t) = (1 + v_d t)^{cnt[d]} is just the binomial expansion. We can compute it in O(cnt[d]) time.
- For the list of polynomials, we will have at most 6 polynomials. We can multiply them using a priority queue based on length, or just multiply sequentially. Since the number is small, sequential multiplication is fine, but we need to ensure the degrees don't grow too large. The final degree is N, so the largest intermediate degree is at most N. The total time for k multiplications is O(k * N log N). With k=5, it's fine.
- After getting P(t), we have the coefficients p[0..N].
- For each d with cnt[d]>0, compute h coefficients as described. We need to do this for each d. Since there are at most 6, it's O(6N) = O(N).
- Precompute inv[1..N] for the integration.
- Compute S_d for each d. For d=1, numbers 1..min(9,N). For d=2, 10..min(99,N), etc. We can compute the sum of arithmetic progression: sum_{i=L}^{R} i = (R-L+1)*(L+R)//2. But careful with large N. We can compute by loops or using formulas. Since N is up to 2e5, we can just loop from 1 to N and group by length. That is O(N) and simple.
- Compute factorial N! mod MOD. We can precompute factorials up to N.
- Finally, compute Total = fact[N] * sum_d (S_d_mod * integral_d) % MOD.

Let's test on N=1. N=1, cnt[1]=1, v_1=9. A_1(t) = 1+9t. P(t)=1+9t. S_1=1. H_1(t) = P/(1+9t) = 1. integral = 1/1 = 1. Total = 1! * 1 * 1 = 1. Correct.

Test on N=2. Permutations: (1,2) -> 12; (2,1) -> 21. Sum = 33.
Our method: N=2. cnt[1]=2. v=9. A=(1+9t)^2 = 1+18t+81t^2. P=1+18t+81t^2. S_1=3. H = P/(1+9t). p=[1,18,81]. h0=1. h1=18-9=9. h2=81-9*9=0. integral = 1/1 + 9/2 = 1 + 9*inv2. inv2=499122177. 9*499122177 = 4492099593 mod 998244353? 9*499122177 = 4,492,099,593. Mod: 4,492,099,593 - 4*998,244,353 = 4,492,099,593 - 3,992,977,412 = 499,122,181. So integral = 1 + 499,122,181 = 499,122,182. Total = 2! * 3 * 499,122,182 = 6 * 3 * 499,122,182 = 18 * 499,122,182 = 8,984,199,276 mod 998,244,353. Compute: 998,244,353*9 = 8,984,199,177. Subtract: 8,984,199,276 - 8,984,199,177 = 99. So Total = 99? But expected sum is 33. Something is wrong.

Wait, for N=2, the sum of f(P) over permutations: (1,2) -> 12, (2,1) -> 21, sum=33. Our computed Total = 99? That's off by a factor of 3. Let's recalc integral for N=2.

H coefficients: h0=1, h1=9. integral = 1/1 + 9/2 = 1 + 9/2. But 9/2 is not an integer. In modulo arithmetic, 9/2 means 9 * inv2. So integral = 1 + 9*inv2. inv2 = 499122177. 9*inv2 = 4492099593 mod 998244353. As computed, 4492099593 mod 998244353 = 499122181. So integral = 1 + 499122181 = 499122182. Then Total = 2! * S_1 * integral = 2 * 3 * 499122182 = 6 * 499122182 = 2994733092 mod 998244353. 998244353*3 = 2994733059. 2994733092 - 2994733059 = 33. Yes! 33. I miscalculated: 6 * 499122182 = 2,994,733,092. Mod: 2,994,733,092 - 2,994,733,059 = 33. So it works. I did 18*... but should be 6. So correct.

So the method is correct.

Now we need to implement polynomial multiplication using NTT. Since MOD is 998244353, we can use the standard NTT with primitive root 3. We need to implement ntt, inverse ntt, and convolution.

We have to be careful with the sizes. The polynomials we multiply are lists of integers modulo MOD. We need to ensure the length is a power of 2 for NTT.

Let's outline the code:

1. Read N.
2. Precompute pow10[d] for d=1..6: pow10[d] = 10^d % MOD.
3. Compute cnt[d] and S_d for d=1..6. We can loop x from 1 to N, determine its length, and accumulate cnt[d] and S_d. This is O(N) and simple.
4. Compute v[d] = (pow10[d] - 1) % MOD.
5. For each d with cnt[d] > 0, compute the polynomial A_d of length cnt[d]+1: A_d[0]=1; for j=1 to cnt[d]: A_d[j] = A_d[j-1] * (cnt[d] - j + 1) % MOD * inv[j] % MOD * v[d] % MOD. We need inv[1..N] precomputed.
6. Now we have a list of polynomials: polys = [A_d for d in 1..6 if cnt[d] > 0].
7. Multiply them together to get P(t). Use a function multiply(poly1, poly2) that uses NTT. We can use a while loop: while len(polys) > 1, pop the two smallest, multiply, push back. Or just multiply sequentially. Since the number is small, we can sort by length and multiply the two smallest each time. This is efficient.
8. After getting P (list of length N+1), we have coefficients p[0..N].
9. For each d with cnt[d] > 0, compute h_d coefficients:
   h[0] = p[0]
   for k=1 to N:
       h[k] = (p[k] - v[d] * h[k-1]) % MOD
   We only need up to N-1.
10. For each d, compute integral_d = sum_{k=0}^{N-1} h[k] * inv[k+1] % MOD.
11. Compute total_sum = fact[N] * sum_d (S_d_mod * integral_d) % MOD.
12. Print total_sum.

We need to precompute factorials and inverses up to N.

Potential issues:
- The NTT implementation must handle large sizes. The degree of P is N, so the convolution size for multiplying two polynomials of degrees a and b is a+b+1, padded to next power of 2. The maximum size is 2N. For N=2e5, 2N=4e5, next power of 2 is 2^19=524288. That's fine.
- We need to implement ntt efficiently. The standard iterative NTT with bit-reversal is fine.
- We must be careful with the modular arithmetic: all operations mod MOD.

Let's verify with the sample N=390. We can't compute by hand, but we trust the method.

Complexity: O(N log N) for NTT, O(N) for other steps. With N=2e5, it's fast.

Now, we need to ensure that the polynomial A_d is computed correctly. Since cnt[d] can be up to 1e5, computing it iteratively is O(cnt[d]). The total is O(N). That's fine.

One more check: In the formula Total = N! * sum_d S_d * integral_d, we have S_d as the sum of x for x in that length group. We need to take S_d modulo MOD.

Let's test with a small N manually using code mental? Not necessary.

Now, we should write the code.

Implementation details for NTT:

We can write a function ntt(a, invert) that performs in-place NTT. The primitive root for 998244353 is 3. The root of unity for length n is g^{(MOD-1)/n} mod MOD. We can precompute roots for each power of 2, but since we have a fixed MOD, we can compute on the fly.

Standard code:

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(g, (MOD-1)//length, MOD)
        if invert:
            wlen = pow(wlen, MOD-2, MOD)
        for i in range(0, n, length):
            w = 1
            for j in range(i, i+length//2):
                u = a[j]
                v = a[j + length//2] * w % MOD
                a[j] = (u + v) % MOD
                a[j + length//2] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD-2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

Then convolution:

def multiply(a, b):
    n = len(a) + len(b) - 1
    size = 1
    while size < n:
        size <<= 1
    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:n]

We need to ensure that the lists are mutable. In Python, lists are fine.

Now, for the initial polynomials A_d, we need to compute the binomial coefficients. We can do:

def compute_poly(cnt, v):
    if cnt == 0:
        return [1]
    res = [1] * (cnt + 1)
    for j in range(1, cnt + 1):
        res[j] = res[j-1] * (cnt - j + 1) % MOD * inv[j] % MOD * v % MOD
    return res

We need inv[j] precomputed. inv[1..N] can be computed using the linear sieve: inv[1]=1; for i=2..N: inv[i] = MOD - MOD//i * inv[MOD%i] % MOD.

Also factorial: fact[0]=1; for i=1..N: fact[i]=fact[i-1]*i%MOD.

Now, we need to be careful with the lengths: when we multiply polynomials, the result length is sum of degrees + 1. The degree of A_d is cnt[d]. So the final degree is N.

Let's test with N=3. cnt[1]=3. A_1 length 4. Multiply? Actually only one polynomial, so P = A_1. Then P length 4. That works.

For N=390, cnt[1]=9, cnt[2]=90, cnt[3]=300? Actually 100-999: 900 numbers, but N=390, so only 100-390: 291 numbers? Wait, N=390, so numbers 1-9 (len1), 10-99 (len2), 100-390 (len3). So cnt[1]=9, cnt[2]=90, cnt[3]=291. Sum=390. We have 3 polynomials. Multiply them. The first two: degrees 9 and 90, product degree 99. Then multiply by degree 291, final degree 390. That's fine.

Now, we need to compute S_d. We can compute by iterating x from 1 to N, but that is O(N) and easy. Or we can compute by formulas: For d=1: L=1, R=min(9,N); sum = (R-L+1)*(L+R)//2. But careful: if N<9, R=N. For d=2: L=10, R=min(99,N); etc. This is O(maxlen). So we can just use formulas.

Let's write a function to get the sum of numbers with length d in [1..N]:

def get_sum(d, N):
    start = 10**(d-1)
    end = min(10**d - 1, N)
    if start > end:
        return 0
    cnt = end - start + 1
    return cnt * (start + end) // 2

But for d=1, start=1. This works. However, for large d, 10**d might be large, but Python handles it. But we only need d up to 6. So it's fine.

Now, we need to compute the integral: sum_{k=0}^{N-1} h[k] * inv[k+1] mod MOD. We have inv precomputed.

Now, let's code step by step.

But wait: There is a potential issue: The polynomial P(t) is product_{d} (1 + v_d t)^{cnt[d]}. The degree is N. When we compute the coefficients using NTT, we need to ensure that the coefficients are correct modulo MOD. Since MOD is prime and we are doing exact polynomial multiplication, it's fine.

Now, we should test the code with the samples.

Let's simulate N=3 with the code logic:

- cnt[1]=3, v=9. A_1 = [1, 27, 243, 729] mod MOD? Actually 9^1=9, C(3,1)*9=27. 9^2=81, C(3,2)*81=3*81=243. 9^3=729, C(3,3)*729=729. So A_1 = [1, 27, 243, 729]. P = A_1.
- p = [1,27,243,729]
- For d=1: v=9. h[0]=1. h[1]=27-9*1=18. h[2]=243-9*18=81. h[3]=729-9*81=0. integral = 1*inv1 + 18*inv2 + 81*inv3. inv1=1, inv2=499122177, inv3=332748118 (since 3*332748118=1 mod). 18*inv2 = 18*499122177 mod. 499122177*10=4991221770, *8=3992977416, sum=8984199186. Mod: 998244353*9=8984199177, remainder 9. So 18/2=9. 81*inv3: 81*332748118. 332748118*80=26619849440, *1=332748118, sum=26952597558. Mod: 998244353*27=26952597531, remainder 27. So integral = 1+9+27=37.
- S_1=6.
- Total = 6 * 6 * 37 = 1332. Correct.

So the code works.

Now, we need to implement the NTT multiplication. Since we are in Python, we need to write efficient loops. For N=2e5, the NTT size will be up to 2^19=524288. The number of butterflies is about size * log2(size) ~ 524288 * 19 = 10 million, which is fine in Python if optimized. But we need to be careful with the constant factor. Python NTT can be slow if not optimized, but for 10 million operations, it should be okay within time limits (usually 2 seconds? But Python might be borderline). We can use PyPy's JIT to speed up. We can also use the fact that we only need a few multiplications (5). So it's okay.

Alternatively, we can compute the polynomial P(t) using DP without NTT, by iteratively multiplying by (1 + v_d t)^{cnt[d]}. Since cnt[d] can be up to 1e5, we need an efficient way to multiply by a polynomial that is a power of a linear term. There is a trick: we can use the fact that (1 + v t)^m = \sum_{j=0}^m C(m,j) v^j t^j. We can convolve the current polynomial with this. But the convolution can be done in O(N log N) using NTT anyway. So NTT is the way.

We can also compute the coefficients of P(t) by using the fact that the product of binomials can be computed by multiplying the polynomials in a balanced tree. Since the number of factors is small, we can just multiply the two largest? Actually, to minimize total work, we should multiply the two smallest each time. But with 6 factors, the difference is small.

Let's consider the degrees: say cnt[1]=9, cnt[2]=90, cnt[3]=291, etc. The largest is maybe 100001. So we have polynomials of various sizes. We can put them in a list and use heapq.

We need to import heapq.

Now, we must be cautious: the product of two polynomials of degrees a and b has degree a+b. The convolution length is a+b+1. The NTT size is the next power of 2 of a+b+1. So the work for multiplying two polynomials of degrees a and b is O((a+b) log (a+b)). If we always multiply the two smallest, the total work is roughly O(N log N) because the sum of (a+b) log (a+b) over the tree is bounded by O(N log N). For example, if we have N items, the cost of multiplying them in a balanced tree is sum_{i=1}^{log N} (N/2^i) * (N/2^i) log(N) ? Not exactly. Actually, the cost of a single multiplication is proportional to the size of the result times log. If we multiply the two smallest, the result size is small, but then we multiply with a large one. The total cost is O(N log^2 N) if we do it naively? Let's analyze: Suppose we have n items of total size N. If we always multiply the two smallest, the sizes of the polynomials being multiplied at each step are at most the size of the result. The total work over all steps is at most O(N log N) because each element's coefficient participates in O(log N) multiplications? Not exactly. There is a known result: the cost of multiplying many polynomials using a Huffman tree is O(N log N) if the multiplication is done in O(M log M) for size M. Actually, the total work is O(N log^2 N) in the worst case? Let's think: We have 6 polynomials. The total work is dominated by the last multiplication, which is O(N log N). The previous multiplications are on smaller polynomials, so the total is a few times O(N log N). So it's fine.

Thus, using a heap is easy.

Now, we need to handle the case when some cnt[d]=0. Then the polynomial is just [1] (constant 1). Multiplying by 1 does nothing. So we can skip them.

Now, let's write the code.

We'll structure it as:

- Read N.
- Precompute inv and fact up to N.
- Compute cnt and S_d for d=1..6. We can compute cnt by iterating x from 1 to N, but that is O(N) and fine. Actually, we can compute cnt using the ranges. Let's do it by ranges to be O(1).

For d from 1 to 6:
    start = 10**(d-1)
    end = min(10**d - 1, N)
    if start <= end:
        cnt[d] = end - start + 1
        S_d = (start + end) * cnt[d] // 2
    else:
        cnt[d] = 0
        S_d = 0

But careful: for d=1, start=1, end=min(9,N). So if N<9, it's fine.

Now, compute v[d] = (pow(10, d, MOD) - 1) % MOD.

Now, for each d with cnt[d] > 0, compute poly_d = compute_poly(cnt[d], v[d]).

Now, put these polynomials in a list. If the list is empty (N=0? but N>=1), then P(t) = [1].

Use a heap to multiply them. We'll use heapq where the key is the length of the polynomial. But we need to store the polynomial itself. Since we need to compare lengths, we can push tuples (len(poly), poly) into the heap. However, heapq in Python compares the first element. So we can push (len(poly), poly). But we need to be careful: if two polynomials have the same length, the comparison might try to compare the lists, which is not allowed. So we can add a unique id or just store the length as the first element and the polynomial as the second, and ensure that if lengths are equal, we break ties by some other measure. Actually, heapq will try to compare the second element if the first is equal, so we need to make the second element comparable. We can store the length as the first element, and an index or just the polynomial as the second, but since polynomials are lists, they can be compared? In Python, lists can be compared lexicographically. But it's safer to avoid comparing lists. We can store a tuple (len(poly), id(poly), poly). But we can just multiply sequentially: since there are at most 6, we can just multiply them in any order. The simplest is to multiply them one by one. The cost of multiplying sequentially: first multiply the first two, then multiply the result by the third, etc. The intermediate degree grows. The total cost is O(N log N) for the last multiplication, and the others are smaller. So it's fine. We can do:

P = [1]
for d in 1..6:
    if cnt[d] > 0:
        poly_d = compute_poly(cnt[d], v[d])
        P = multiply(P, poly_d)

But this multiplies the largest poly first? Actually, it depends. If we multiply in the order of increasing cnt[d], the intermediate degrees are smaller? For example, if we start with the smallest, P grows slowly. So we can sort the d's by cnt[d] and multiply in that order. That minimizes the intermediate degrees. So:

ds = [d for d in range(1,7) if cnt[d]>0]
ds.sort(key=lambda d: cnt[d])
P = [1]
for d in ds:
    poly_d = compute_poly(cnt[d], v[d])
    P = multiply(P, poly_d)

This is fine.

Now, after getting P, we have p = P. Note that P is a list of length N+1.

Now, for each d in ds:
    h = [0]*N
    h[0] = p[0]
    for k in range(1, N):
        h[k] = (p[k] - v[d] * h[k-1]) % MOD
    integral = 0
    for k in range(N):
        integral = (integral + h[k] * inv[k+1]) % MOD
    total_sum = (total_sum + S_d_mod * integral) % MOD

Finally, answer = fact[N] * total_sum % MOD.

We need to compute S_d_mod = S_d % MOD.

Now, let's test with N=1.
N=1: cnt[1]=1, v=9. poly_1 = [1, 9]. P = [1,9]. p=[1,9].
h[0]=1. h[1] = 9 - 9*1 = 0. integral = 1*1 + 0*inv2 = 1.
S_1=1. total_sum = 1*1=1. fact[1]=1. answer=1. Correct.

Test N=2: cnt[1]=2. poly_1 = (1+9t)^2 = [1, 18, 81]. P = [1,18,81]. p=[1,18,81].
h[0]=1. h[1]=18-9*1=9. h[2]=81-9*9=0. integral = 1*1 + 9*inv2 = 1 + 9*499122177. As before, 9*inv2 = 499122181. integral = 499122182. S_1=3. total_sum = 3 * 499122182 mod = 1497366546 mod 998244353 = 499122193? Wait, 3*499122182 = 1,497,366,546. Mod: 998,244,353*1 = 998,244,353. 1,497,366,546 - 998,244,353 = 499,122,193. Then answer = fact[2] * total_sum = 2 * 499,122,193 = 998,244,386 mod 998,244,353 = 33. Correct.

So the method works.

Now, we need to implement the NTT multiplication carefully. Since we are in Python, we need to ensure it's fast enough. We can use the following optimizations:

- Precompute the roots of unity for each size? Not necessary, we can compute on the fly.
- Use local variables for MOD in the function to avoid global lookups.
- Use while loops instead of for loops where appropriate.

Standard NTT code in Python for competitive programming usually works for sizes up to 2^20 within time limits.

Let's write the code.

We'll define:

MOD = 998244353
G = 3

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        wlen = pow(G, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, length):
            w = 1
            half = length >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b):
    n = len(a) + len(b) - 1
    size = 1
    while size < n:
        size <<= 1
    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:n]

Now, we need to compute the initial polynomials. For cnt[d] up to 100001, we can compute the coefficients in O(cnt[d]) time. The loop:

def compute_poly(cnt, v):
    res = [1] * (cnt + 1)
    for j in range(1, cnt + 1):
        res[j] = res[j-1] * (cnt - j + 1) % MOD * inv[j] % MOD * v % MOD
    return res

We need inv[j] for j=1..cnt[d]. Since cnt[d] can be up to 100001, we precompute inv up to N.

Now, we must be careful with the types: all numbers are integers mod MOD.

Now, let's think about the time. The NTT for size up to 2^19 = 524288 will have about 524288 * 19 = 10 million operations per NTT. We do about 2 forward NTTs and 1 inverse NTT per multiplication, so 3 NTTs per multiplication. With 5 multiplications, that's 15 NTTs, so 150 million operations. In Python, 150 million operations might be around 2-3 seconds, which is acceptable if optimized. But we can also reduce the number of multiplications by using a more balanced tree? Actually, we have 6 factors. If we multiply them in a balanced way, we do about log2(6) ~ 3 levels, but each level has several multiplications. The total number of NTTs is roughly 2 * number of multiplications * average size? Actually, each multiplication does 2 forward and 1 inverse, so 3 NTTs. The total size of all NTTs is proportional to the sum of sizes of all intermediate convolutions. If we multiply in a balanced tree, the total work is O(N log N). With 6 factors, the sequential multiplication might have a larger constant? Let's estimate: sequential: sizes: start with degree 0. Multiply by poly of degree c1: size ~ c1. Multiply by c2: size ~ c1+c2. Multiply by c3: size ~ c1+c2+c3. So the NTT sizes are roughly c1, c1+c2, c1+c2+c3, ... up to N. The sum of sizes is about (number of factors) * N. The log factor is log(N). So total work is O(k N log N) with k=5. That's fine.

But we can also multiply the two largest first? That would make the first multiplication huge, which is bad. So we should multiply the smallest first.

So the plan: sort the polynomials by length, and multiply sequentially.

Now, we need to store the polynomials. Since we have at most 6, we can just compute them and then multiply in order of increasing cnt[d].

Now, let's consider N=200000. The largest cnt[d] is for d=6: numbers from 100000 to 200000: that's 100001 numbers. So cnt[6]=100001. v_6 = 10^6 - 1 = 999999. The polynomial A_6 has degree 100001. Multiplying it with others will eventually give degree 200000. The NTT size for the final multiplication will be next power of 2 of 200001, which is 262144? Actually, 2^18=262144, but 200001 < 262144. So size=262144. That's fine.

Now, we need to ensure that the polynomial multiplication does not produce coefficients that are too large? We are working mod MOD, so it's fine.

Now, we should also consider the case N is small, e.g., N=1,2,3. The NTT code works for any size.

Now, let's write the full code.

We need to be careful with the inv computation. We can compute inv[1..N] using the linear method:

inv = [0] * (N + 1)
inv[1] = 1
for i in range(2, N+1):
    inv[i] = MOD - MOD // i * inv[MOD % i] % MOD

Also factorial:

fact = [1] * (N + 1)
for i in range(1, N+1):
    fact[i] = fact[i-1] * i % MOD

Now, for S_d and cnt[d], we can compute using ranges. Let's write a function:

def get_cnt_sum(d, N):
    start = 10**(d-1)
    end = min(10**d - 1, N)
    if start > end:
        return 0, 0
    cnt = end - start + 1
    s = cnt * (start + end) // 2
    return cnt, s

But note that for d=1, start=1. For d=0? not needed.

We need to compute for d=1 to 6. Since 10**6 = 1,000,000, which is > 2e5, it's fine.

Now, let's code.

One more check: In the integration, we use inv[k+1]. We have inv array up to N, so inv[1..N] is available.

Now, let's test with the sample N=390. We can't verify by hand, but we trust.

Now, we need to consider the time limit. The problem is from AtCoder (likely), and the time limit is usually 2 seconds for Python. NTT in Python for 2e5 might be a bit tight. We can optimize by using PyPy and writing efficient loops. Also, we can reduce the number of NTTs by using the fact that we only need the final polynomial P, and we can compute it by a divide-and-conquer multiplication. Actually, the sequential multiplication does multiple NTTs. We can instead use a single NTT by concatenating the polynomials? No.

Alternatively, we can compute the coefficients of P(t) using the fact that P(t) = product_d (1 + v_d t)^{cnt[d]}. We can compute the coefficients by iterating over d and using the binomial expansion as a convolution, but we can use the fact that the convolution with a binomial can be done using the fact that the generating function is product. There is a way to compute the coefficients using the fact that the polynomial is the product of binomials, and we can compute it by evaluating at many points and using interpolation? Not needed.

Given the time, I think the NTT approach is acceptable. Many solutions to this problem use the same method and pass in Python.

We should also consider using the `numpy` FFT? But we need exact modular arithmetic, so we need NTT.

We can also use the `pyfftw` but it's not standard.

We'll write the NTT as efficient as possible.

Let's code:

def ntt(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    len_ = 2
    while len_ <= n:
        wlen = pow(G, (MOD - 1) // len_, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for i in range(0, n, len_):
            w = 1
            half = len_ >> 1
            for j in range(i, i + half):
                u = a[j]
                v = a[j + half] * w % MOD
                a[j] = (u + v) % MOD
                a[j + half] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        len_ <<= 1
    if invert:
        inv_n = pow(n, MOD - 2, MOD)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(a, b):
    n = len(a) + len(b) - 1
    size = 1
    while size < n:
        size <<= 1
    fa = a + [0] * (size - len(a))
    fb = b + [0] * (size - len(b))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(size):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:n]

Now, we need to compute the initial polynomials. For cnt[d] large, the loop in compute_poly is O(cnt[d]). For d=6, cnt=100001, that's 100k iterations, fine.

Now, let's write the full code.

We must be careful with the indexing: when we compute h[k] for k from 1 to N-1, we need p[k] and h[k-1]. p has length N+1. So we need p[0..N]. h has length N.

Now, the total sum:

total = 0
for d in ds:
    h = [0] * (N)  # we need up to N-1
    h[0] = p[0]
    for k in range(1, N):
        h[k] = (p[k] - v[d] * h[k-1]) % MOD
    integral = 0
    for k in range(N):
        integral = (integral + h[k] * inv[k+1]) % MOD
    total = (total + (S_d % MOD) * integral) % MOD

answer = fact[N] * total % MOD
print(answer)

Now, we need to ensure that S_d is computed correctly. For d=1, start=1, end=min(9,N). s = cnt*(1+end)//2. That's correct.

Let's test N=1: d=1: start=1, end=1, cnt=1, s=1. v=9. poly=[1,9]. P=[1,9]. h[0]=1, h[1]=(9-9*1)=0. integral=1*1 + 0*inv2=1. total=1*1=1. fact[1]=1. answer=1.

N=2: d=1: start=1, end=2, cnt=2, s=3. v=9. poly=[1,18,81]. P=[1,18,81]. h[0]=1, h[1]=18-9=9, h[2]=81-81=0. integral=1 + 9*inv2. inv2=499122177. 9*inv2=499122181. integral=499122182. total=3 * 499122182 mod = 1497366546 mod 998244353 = 499122193. fact[2]=2. answer=2*499122193=998244386 mod 998244353=33.

So it's correct.

Now, we need to handle the case when N is such that some cnt[d] is 0. For example, N=5. Then cnt[1]=5, others 0. ds = [1]. That's fine.

Now, we should also consider N=0? But N>=1.

Now, we need to ensure that the polynomial multiplication does not have any overflow issues. We are using Python integers, so it's fine.

Now, let's write the code in a clean way.

We'll structure:

import sys
sys.setrecursionlimit(1 << 25)

def main():
    MOD = 998244353
    G = 3
    N = int(sys.stdin.readline())
    
    # Precompute inv and fact
    inv = [0] * (N + 1)
    inv[1] = 1
    for i in range(2, N + 1):
        inv[i] = MOD - MOD // i * inv[MOD % i] % MOD
    
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    
    # Compute cnt and S_d
    cnt = [0] * 7
    S = [0] * 7
    for d in range(1, 7):
        start = 10**(d-1)
        end = min(10**d - 1, N)
        if start <= end:
            cnt[d] = end - start + 1
            S[d] = cnt[d] * (start + end) // 2
    
    # Compute v_d
    v = [0] * 7
    for d in range(1, 7):
        v[d] = (pow(10, d, MOD) - 1) % MOD
    
    # Function to compute polynomial (1 + v t)^cnt
    def compute_poly(cnt_d, v_d):
        res = [1] * (cnt_d + 1)
        for j in range(1, cnt_d + 1):
            res[j] = res[j-1] * (cnt_d - j + 1) % MOD * inv[j] % MOD * v_d % MOD
        return res
    
    # List of (d, poly) for d with cnt>0
    polys = []
    for d in range(1, 7):
        if cnt[d] > 0:
            poly = compute_poly(cnt[d], v[d])
            polys.append( (cnt[d], poly) )
    
    # Sort by length
    polys.sort(key=lambda x: x[0])
    
    # Multiply polynomials
    P = [1]
    for _, poly in polys:
        P = multiply(P, poly)
    
    # Now P has length N+1
    # Compute total sum
    total = 0
    for d in range(1, 7):
        if cnt[d] == 0:
            continue
        h = [0] * (N)  # we need N elements (k=0..N-1)
        h[0] = P[0]
        for k in range(1, N):
            h[k] = (P[k] - v[d] * h[k-1]) % MOD
        integral = 0
        for k in range(N):
            integral = (integral + h[k] * inv[k+1]) % MOD
        total = (total + (S[d] % MOD) * integral) % MOD
    
    answer = fact[N] * total % MOD
    print(answer)

if __name__ == "__main__":
    main()

We need to define multiply and ntt inside main or globally. They can be global.

But we need to be careful: the function multiply uses P and poly, which are lists. The multiply function uses ntt which modifies the list in place. We need to ensure that the lists are not shared. In our code, we create new lists each time, so it's fine.

Now, we need to test with the sample N=3. We already did mentally.

Now, let's consider the time. The NTT size for the last multiplication is about 2^19. The inner loops in ntt are in Python, so it might be a bit slow. We can try to optimize by using local variables in the ntt function. Also, we can avoid the bit-reversal loop by using a precomputed table? But for a one-off, it's fine.

We can also use the fact that we only need to multiply a few times, so we can write the ntt function with some optimizations.

Let's test the code with a small N to ensure no errors.

We'll run through N=3:

N=3. inv: inv[1]=1, inv[2]=499122177, inv[3]=332748118.
fact: 1,2,6.
cnt[1]=3, S[1]=6. v[1]=9.
polys: [(3, [1,27,243,729])].
P = [1] * poly = multiply([1], [1,27,243,729]) = [1,27,243,729].
d=1: h[0]=1, h[1]=27-9=18, h[2]=243-162=81. integral = 1*1 + 18*inv2 + 81*inv3 = 1+9+27=37. total=6*37=222. answer=6*222=1332. Correct.

Now, for N=200000, the code should work.

One potential issue: The polynomial A_d has length cnt[d]+1. When we multiply, the result length is sum of degrees + 1 = N+1. So P has length N+1. That's correct.

Now, we need to ensure that the NTT size is large enough. In multiply, we compute size as the next power of 2 of n. For the first multiplication, if we start with [1] and poly of length c+1, n = c+1. Size is next power of 2 of c+1. That's fine.

Now, let's think about the memory. The lists are of size up to 2^19=524288, which is fine.

Now, we should consider if there is any off-by-one error in the integration. The integral is sum_{k=0}^{N-1} h[k] / (k+1). We used inv[k+1] for k from 0 to N-1. That's correct.

Now, we need to make sure that the modular inverse of k+1 is computed. We have inv[1..N] precomputed. So for k+1 from 1 to N, it's available.

Now, let's check the sample N=390. We can't compute manually, but we can assume it's correct.

Now, we should also consider the case when N=1, the polynomial multiplication: P = [1] * [1,9] = [1,9]. The h array has length 1 (since N=1, we need h[0] only). integral = h[0]*inv[1] = 1. total = 1*1=1. answer=1.

Now, the code should be correct.

We need to be careful with the variable names to avoid shadowing.

Now, let's write the final code with the ntt and multiply functions.

We'll define them outside main to avoid redefinition.

One more optimization: In the ntt function, the inner loop computes w = w * wlen % MOD. We can precompute the wlen for each length, but since we only do a few sizes, it's fine.

Now, let's produce the final code.</mm:think>### PLAN
We need to sum over all permutations P of (1..N) the integer formed by concatenating their decimal representations. The contribution of each element x in a permutation depends on the total number of digits of elements that appear after it. Using a generating function approach, we transform the problem into computing a polynomial P(t) = ∏_{d} (1 + v_d t)^{cnt[d]}, where v_d = 10^d − 1 and cnt[d] is the number of integers with d digits. The total sum equals N! times the integral from 0 to 1 of a rational function derived from P(t), which reduces to summing coefficients of a related polynomial. We compute P(t) via polynomial multiplication using NTT (since MOD = 998244353 is NTT-friendly), then recover the needed coefficients and sum.