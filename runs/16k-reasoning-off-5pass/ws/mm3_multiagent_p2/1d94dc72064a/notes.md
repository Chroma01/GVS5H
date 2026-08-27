
## ideation
The game ends on the move that first makes `S = {1,…,N}`.  
A move can either:
- activate a new index `i` (if `i ∉ S`), paying 1 unit from `A_i` and adding `i` to `S`.
- spend a unit on an already active index, adding nothing to `S`.

Thus, before the game can finish, exactly `N` *activating* moves must be performed (one for each index). These use `N` units of `A_i` in total. After all indices are activated, only “spending” moves remain, each costing 1 unit of some `A_i` that is still positive. The player who makes the last possible spending move (i.e. the move that brings the total number of moves to `sum A_i`) wins, because after that no move is possible and the game would have already ended on the activating move that completed `S`.  

Equivalently, total moves in the whole game = `total = Σ A_i`. The winner is determined by the parity of `total`:
- If `total` is odd, the first player (Fennec) makes the last move → Fennec wins.
- If `total` is even, the second player (Snuke) makes the last move → Snuke wins.

We must check whether optimal play can force a win earlier. Could a player intentionally delay activation to change parity? The rule “players can always make a move until the game ends” guarantees that as long as some `A_i > 0`, a move exists. The only strategic choice is which index to pick. However, the game ends immediately when `S` becomes full; no further moves are allowed. So the total number of moves is exactly `total = Σ A_i`, because every move reduces some `A_i` by 1 and eventually all `A_i` become 0. The only way to finish earlier is to have `S` become full before all `A_i` are exhausted, but the extra remaining decrements (if any) are still moves that happen after `S` is full. Wait, the rule says: the game ends as soon as `S` becomes full. So if after activating all indices there are still positive `A_i`, the game would have already ended on the move that activated the last missing index. That means the total number of moves is exactly the number of moves needed to make `S` full, which is at most `total`, but could be less if we don't need to use all `A_i`. However, the problem statement says: “until a winner is determined and the game ends, players can always make a move (there exists some i such that 1 ≤ A_i)”. This is a guarantee that the game cannot stall, but not that all `A_i` are consumed. Actually, the game ends as soon as `S` is full. So the total number of moves is the move count when the last index is added to `S`. Let `k` be the number of moves up to that point. After that the game stops. So we need to determine who makes that move.

Since activating an index requires one unit of that index, we need at least 1 unit per index. The total sum `S = Σ A_i` is an upper bound on the number of moves (if we keep spending after `S` is full, but we can't because game ends). The game will last exactly `N + extra` moves, where `extra` is the number of “spending” moves performed before the final activation. After the final activation the game ends immediately; no further moves occur. So total moves = `N + extra`. The extra moves are those performed before the last activation, i.e., spending on already active indices. The remaining decrements after the last activation are never executed. So we only need to decide who makes the `(N + extra + 1)`-th move? Wait, the game ends on the move that completes `S`. So the winning move is exactly the move that adds the last missing index. That move is the `(N + extra)`-th move, where `extra` is the number of prior spending moves. So the winner is determined by the parity of `N + extra`. But `extra` can be chosen by the players up to `S - N` (the number of units beyond the first unit of each index). Since players are optimal, the one who moves second in the “spending” phase may try to control parity.

This is a combinatorial game that can be analyzed via the Sprague‑Grundy or simple parity if the game is symmetric. However, there is a known solution: the game is equivalent to Nim with heap sizes `A_i`, but with a twist: a heap of size `A_i` is “special” because the first time you take from it you also “fill” a token. Actually, this is similar to “Turning Turtles” or “Dawson's Kayles”? Let's think carefully.

Simplify: Each index `i` is like a pile of `A_i` tokens. The first token taken from pile `i` also “collects” a unique prize (the index). The game ends when all prizes are collected. The player who collects the last prize wins. After a prize is collected, the remaining tokens in that pile are just normal Nim tokens (you can take them anytime, but they don't affect the win condition). However, the game ends immediately upon collecting the last prize, so tokens taken after that are irrelevant. So effectively, each pile contributes 1 “activation” move and `(A_i - 1)` “extra” moves. The total number of moves before the game ends is at least `N` (one per pile) and at most `N + Σ(A_i - 1) = Σ A_i`. The players choose the order of these moves. The winner is the player who makes the `N`th activation move (the one that completes the set). The extra moves are interspersed, and the player who makes the last extra move before the final activation may influence parity.

This is a game of “take‑away with a finish line”. A known result: The first player wins iff `Σ A_i` is odd? Or maybe `Σ (A_i - 1)` parity matters. Let's test with small cases.

Case N=1. A = [a]. Moves: only one pile. The first move must take from pile 1. Since i=1 is not in S, it adds 1 to S, making S={1}. The game ends on that move, and the player who made it wins. So regardless of a (as long as a≥1, which holds), the first player always wins. Sum = a. Parity of a: if a is odd, first player wins (odd total moves, but game ends on move 1). If a is even, first player also wins (game ends on move 1, not on move a). So parity of sum does NOT determine winner for N=1. So the simple parity of total sum is wrong.

Let's examine: N=1, A=[2]. Moves: only index 1. First player: choose i=1, A becomes (1), S={1} → game ends, first player wins. So indeed first player wins. But if we continued (which we can't), there would be 2 moves total, but game ends on move 1. So the relevant number is the move number at which the set becomes full, which is exactly the number of moves performed until the N-th distinct index is chosen. Since the set becomes full as soon as each index has been chosen at least once, the game lasts exactly the length of the shortest sequence of moves that covers all indices. The players can choose to waste moves on already chosen indices, increasing the total number of moves, but the game ends at the moment the last new index is chosen. So the winner is the player who makes the move that selects the last uncovered index.

Thus the game is: we have N “required” selections (one per index). Between them, we may insert any number of “waste” selections on already covered indices, as long as their `A_i` values permit. The game ends when the last required selection is made. The total number of moves is `N + W`, where `W` is the number of waste moves inserted before the final required move. The player who makes the `(N+W)`-th move wins. Since players alternate, the parity of `N+W` determines the winner. The players can influence `W` by choosing to waste or not. The question: can the first player force a win regardless of the second player's actions? This is a typical impartial game: the set of allowed moves is all i with A_i>0. A move on an already active i is a “pass” that consumes a token but doesn't progress the goal. The goal is to make the last move that completes the set.

This is equivalent to a game of Nim where each heap has size A_i, and the “terminal” condition is that one token has been taken from each heap. Actually, we can think of each heap i having a “mandatory” first token that must be taken to “cover” the heap, and `A_i - 1` optional tokens. The game ends when the last mandatory token is taken. The optional tokens can be taken before the last mandatory token, but after that the game ends. So the game is like: there are `N` mandatory tokens, and `total_extra = Σ (A_i - 1)` optional tokens. Players alternate taking any token (either a mandatory one that hasn't been taken yet, or an optional one from a heap that already gave its mandatory token). The game ends when all mandatory tokens are taken. The player who takes the last mandatory token wins. The optional tokens are just “extra moves” that delay the finish.

This is a known impartial game: the outcome is determined by whether the total number of tokens (mandatory + optional) is odd or even? Not exactly, because the game could end before all optional tokens are taken. However, the players can choose to take optional tokens at any time (subject to availability). The key is: if there is at least one optional token available before the last mandatory token is taken, a player can choose to take it (waste a move) to flip parity. The second player can mirror the first player's strategy to force a win? Let's analyze.

Let M = N (mandatory tokens), E = total_extra = Σ (A_i - 1). The game is: start with M uncovered, E extra. On a turn, a player either covers a new index (mandatory move) or spends an extra token. The game ends when M=0. The player who makes the move that makes M=0 wins.

This is a simple take-away game: the set of positions is (remaining_mandatory, remaining_extra). But extra tokens are not replenished; they are finite. Actually, each heap i has a_i-1 extra tokens. They are not interchangeable; you can only spend from a heap that has already been activated. So the state is more detailed: for each heap, whether it is active and how many tokens remain. But since extra tokens are only usable after activation, and after activation they are just like a pile of tokens that can be taken one by one, and they don't affect the win condition (the game ends when all are activated). However, the distribution of extra tokens across heaps matters for who can take them when. But if a heap is not yet active, you cannot take its extra tokens; you can only take the mandatory token. So the game is: there are N piles, each initially with a_i tokens. The first token taken from pile i “activates” it. The game ends when all piles have been activated. The player who activates the last pile wins.

This is exactly the game of “Nim with a pass” or “Nim with a finishing move”. There is a known result: the first player wins if and only if there is at least one pile with size > 1? Or something like that. Let's test small cases.

N=1, A=[1]: total moves=1, mandatory=1, extra=0. Game ends on first move, first player wins. So first player wins.

N=1, A=[2]: mandatory=1, extra=1. Moves: first player can take the mandatory (activate) and win immediately, or take the extra? But to take the extra, the pile must be activated. So first move must be mandatory. So first player wins. So for N=1, first player always wins.

N=2, A=[1,1]: M=2, E=0. Moves: 2 mandatory moves total. First player takes one (say pile 1), second player takes the other (pile 2) and wins. So second player wins. Sum=2 (even). Parity of sum? Even -> second player wins. So for N=2, A=[1,1], second wins.

N=2, A=[1,2]: M=2, E=1 (since A2-1=1). Moves: 
- Fennec can take from pile 1 (mandatory). Now S={1}, remaining mandatory=1, extra=1 (from pile 2, but not yet active). 
- Snuke must take mandatory from pile 2 (only move). Game ends, Snuke wins. So Snuke wins. Sum=3 (odd) -> but Snuke wins. So parity of sum is not the determinant.

N=2, A=[2,2]: M=2, E=2. 
Possible plays: Fennec can take mandatory from pile 1 (A1 becomes 1). Now active: {1}, mandatory left: 1 (pile 2), extra available: 1 (from pile 1). 
- Snuke can now either take mandatory from pile 2 (wins immediately), or take extra from pile 1 (A1 becomes 0). If Snuke takes extra, then state: active {1,2? no, still only {1} because pile 2 not activated}, but wait, after Snuke takes extra from pile 1, pile 1 has no tokens left, but pile 2 still has 2 tokens and is not active. So mandatory left: 1 (pile 2), extra left: 1 (from pile 2, but not yet active). 
- Fennec must take mandatory from pile 2 (only move). Game ends, Fennec wins. So Snuke would not take extra; Snuke will take mandatory and win. So Snuke wins. Sum=4 (even) -> Snuke wins. So parity matches here.

N=2, A=[2,3]: M=2, E=3. 
- Fennec mandatory on pile1 (A1=1). State: active {1}, mandatory left: 1 (pile2), extra available: 1 (from pile1), plus pile2 has 3 tokens, 1 mandatory and 2 extra (but not active yet). 
- Snuke can take mandatory from pile2 and win. So Snuke wins. Sum=5 (odd) -> Snuke wins. Parity of sum fails.

N=2, A=[3,3]: M=2, E=4. 
- Fennec mandatory on pile1 (A1=2). State: active {1}, mandatory left: 1 (pile2), extra available: 2 (from pile1), pile2 has 3 tokens (1 mandatory, 2 extra) inactive.
- Snuke can take mandatory from pile2 and win. So Snuke wins. Sum=6 (even) -> Snuke wins.

N=2, A=[1,3]: M=2, E=2. 
- Fennec mandatory on pile1 (A1=0). State: active {1}, mandatory left: 1 (pile2), extra available: 0. 
- Snuke mandatory on pile2 and wins. Sum=4 (even) -> Snuke wins.

It seems for N=2, if both A_i >= 1, Snuke wins? Let's test N=2, A=[1,4]: M=2, E=3. 
- Fennec mandatory on pile1. Then Snuke mandatory on pile2 and wins. So Snuke wins.

What about N=2, A=[2,1]? Same as [1,2] by symmetry, Snuke wins.

So for N=2, Snuke seems to always win? Let's test N=2, A=[100,100]. Fennec takes mandatory on one, Snuke takes mandatory on the other and wins. So Snuke wins. So for N=2, Snuke always wins? But sample input 1 is N=3, A=[1,9,2], output Fennec. So for N=3, maybe first player can win.

Let's test N=3, small values to see pattern.
A=[1,1,1]: M=3, E=0. Moves: 3 mandatory moves. Fennec, Snuke, Fennec. Fennec takes the 3rd and wins. So Fennec wins. Sum=3 (odd) -> Fennec wins. Parity matches.

A=[1,1,2]: M=3, E=1. 
Possible optimal play? 
- Fennec mandatory on pile3 (size 2) or pile1? Let's think. If Fennec takes mandatory on pile3 (A3 becomes 1), state: active {3}, mandatory left: 2 (p1,p2), extra available: 1 (from pile3). 
- Snuke can take mandatory on pile1 (A1=0). State: active {1,3}, mandatory left: 1 (p2), extra available: 1 (from p3). 
- Fennec can take mandatory on pile2 and win. So Fennec wins. 
Alternatively, Snuke could take extra from pile3? If Snuke takes extra from pile3, A3 becomes 0. Then mandatory left: 2, extra available: 0. Then Fennec mandatory on p1, Snuke mandatory on p2, Snuke wins. So Snuke will choose to take extra to flip parity. So from state (M=2, E=1) with player to move being Snuke, Snuke can force a win? Let's analyze: state (M=2, E=1) means there are two unactivated piles and one extra token available (from an already activated pile). The player to move can either:
- take a mandatory: reduces M to 1, E stays 1. Then opponent can take mandatory and win? Wait, if player takes mandatory, M becomes 1, E=1. Then opponent can either take mandatory (M=0) and win, or take extra (E=0, M=1). If opponent takes extra, then M=1, E=0, and the next player must take mandatory and win. So the player who moves in (M=2, E=1) loses? Let's compute properly.
From (M=2, E=1) to move:
Option A: take mandatory. New state: (M=1, E=1) with opponent to move.
From (M=1, E=1):
- Opponent can take mandatory: M=0, game ends, opponent wins.
- Opponent can take extra: (M=1, E=0) to move. Then current player must take mandatory and win.
So from (M=1, E=1), the player to move can win by taking extra. So if you give opponent (M=1, E=1), they can win. Thus Option A is losing.
Option B: take extra. New state: (M=2, E=0) with opponent to move. From (M=2, E=0), opponent must take mandatory (only move). New state: (M=1, E=0) to move. Then current player must take mandatory and win. So Option B is winning. So the player to move in (M=2, E=1) can win by taking extra. So Snuke would take extra and win. Thus in A=[1,1,2], Fennec loses? Let's simulate:
- Fennec mandatory on pile3 (M=2, E=1) to move: Snuke. Snuke takes extra from pile3 (E=0). State: M=2, E=0, active {1,2? no, only pile3 is active? Wait, Fennec activated pile3. Snuke took extra from pile3, so pile3 still active, A3 becomes 0. So active set = {3}. Mandatory left: pile1 and pile2. Extra left: 0.
- Fennec must take mandatory on pile1 or pile2. Say pile1. State: active {1,3}, M=1, E=0.
- Snuke takes mandatory on pile2 and wins. So Snuke wins. So A=[1,1,2] is a win for Snuke. Sum=4 (even) -> Snuke wins. So parity of sum matches here.

A=[1,2,2]: M=3, E=2 (A2-1=1, A3-1=1). 
Let's see if Fennec can force win. 
- Fennec could take mandatory on pile2 (A2 becomes 1). State: active {2}, M=2, E=1 (from pile2). 
- Snuke can take extra from pile2? Then A2=0, active {2}, M=2, E=0. Then Fennec mandatory on p1, Snuke mandatory on p3, Snuke wins. Or Snuke could take mandatory on p3. Let's explore:
Option 1: Snuke takes mandatory on p3. State: active {2,3}, M=1 (p1), E=2 (p2 has 1 extra, p3 has 1 extra). 
- Fennec can take mandatory on p1 and win (since M=0). So if Snuke takes mandatory on p3, Fennec wins. So Snuke would not do that. 
Option 2: Snuke takes extra from p2. State: active {2}, M=2, E=0. Then Fennec mandatory on p1, Snuke mandatory on p3, Snuke wins. So Snuke can force win by taking extra. So Fennec loses? Let's see if Fennec has a better first move.
- Fennec mandatory on p1. State: active {1}, M=2, E=0. Then Snuke mandatory on p2, Fennec mandatory on p3, Fennec wins. Wait: after Fennec activates p1, M=2, E=0. Snuke must activate p2 (mandatory). State: active {1,2}, M=1, E=1 (from p2). Fennec can now either activate p3 and win, or take extra from p2. If Fennec takes extra, then M=1, E=0, Snuke activates p3 and wins. So Fennec will activate p3 and win. So Fennec wins by first activating p1. So A=[1,2,2] is a win for Fennec. Sum=5 (odd) -> Fennec wins. Parity matches.

A=[2,2,2]: M=3, E=3. 
- Fennec mandatory on p1 (A1=1). State: active {1}, M=2, E=1 (from p1). 
- Snuke can take extra from p1 (E=0, M=2) -> then Fennec mandatory on p2, Snuke mandatory on p3, Snuke wins. Or Snuke can take mandatory on p2. State: active {1,2}, M=1, E=2 (p1 has 1 extra, p2 has 1 extra). 
- Fennec can now take mandatory on p3 and win. So Snuke will take extra from p1 to force win. So Snuke wins? Let's check: after Fennec activates p1, Snuke takes extra from p1. Then active {1}, M=2, E=0. Fennec must activate p2. State: active {1,2}, M=1, E=1 (from p2). Snuke can now either activate p3 and win, or take extra from p2. If Snuke takes extra, M=1, E=0, Fennec activates p3 and wins. So Snuke will activate p3 and win. So Snuke wins. 
Alternatively, Fennec could first take mandatory on p2 or p3; by symmetry, same result. So A=[2,2,2] is a win for Snuke. Sum=6 (even) -> Snuke wins. Parity matches.

A=[1,1,3]: M=3, E=2. 
- Fennec mandatory on p3 (A3=2). State: active {3}, M=2, E=2 (from p3). 
- Snuke can take extra from p3 (E=1). State: M=2, E=1. Then Fennec can take extra? Let's see: from (M=2, E=1) to move, as we saw earlier, the player to move can win by taking extra? Wait, we need to analyze (M=2, E=1). We determined that from (M=2, E=1) to move, taking extra leads to (M=2, E=0) with opponent to move, which is a win for the opponent? Let's re-evaluate (M=2, E=1) carefully.
We have two unactivated piles and one extra token from an activated pile. The player to move can:
1. Take mandatory on an unactivated pile: reduces M to 1, E remains 1. Opponent now faces (M=1, E=1). As we saw, from (M=1, E=1), the player to move can win by taking extra (leaving M=1, E=0) so the other player must take mandatory and win? Wait, need to be precise.
From (M=1, E=1) to move:
- If you take mandatory: M=0, you win immediately.
- If you take extra: M=1, E=0, opponent must take mandatory and win.
So from (M=1, E=1), the player to move can win by taking mandatory. So the player to move in (M=1, E=1) wins. So if you give opponent (M=1, E=1), they win. Thus taking mandatory from (M=2, E=1) is a losing move.
2. Take extra: reduces E to 0, M stays 2. Opponent faces (M=2, E=0). From (M=2, E=0), opponent must take mandatory. Then you face (M=1, E=0) and must take mandatory and win. So taking extra from (M=2, E=1) is a winning move. So the player to move in (M=2, E=1) wins by taking extra. So Snuke, from (M=2, E=2) after Fennec's move? Wait, in A=[1,1,3], after Fennec activates p3, state is (M=2, E=2) with Snuke to move. 
From (M=2, E=2), Snuke can:
- Take mandatory: (M=1, E=2) to Fennec. From (M=1, E=2), Fennec can take mandatory and win. So taking mandatory is losing.
- Take extra: (M=2, E=1) to Fennec. As we just saw, (M=2, E=1) to move is a win for the player to move (Fennec). So Snuke taking extra gives Fennec a winning position. So Snuke loses? Let's see if Snuke has any other move. The only extra is from p3. So Snuke is forced to give Fennec a win. So Fennec wins. Sum=5 (odd) -> Fennec wins. Parity matches.

A=[1,3,3]: M=3, E=4. 
- Fennec mandatory on p2 (A2=2). State: active {2}, M=2, E=4? Wait, p2 has 2 extra, but only 1 is available? Actually, p2 had 3 tokens: mandatory used, 2 extra remain. So E=2? Wait, we need to track per pile. But since extra tokens are only usable after activation, and there are other piles with extra tokens that are not yet active. The total extra is sum (A_i - 1) = (1-1)+(3-1)+(3-1) = 0+2+2 = 4. But after activating p2, the extra tokens from p2 are available (2), but extra tokens from p1 and p3 are not yet available because they are not active. So the available extra is 2, not 4. So the state is not just (M, total_E), but also how many extra are available (i.e., from active piles). However, the total extra is fixed, but availability depends on which piles are active. So the game is more complex.

Let's analyze A=[1,3,3] properly.
Piles: p1:1, p2:3, p3:3.
Fennec moves. Options:
1. Activate p1. Then p1=0. Active {1}. M=2. Available extra: 0 (since p1 had no extra). Total extra: 4, but none available. Then Snuke must activate a pile, say p2. Active {1,2}, p2 becomes 2. M=1. Available extra: 2 (from p2). Then Fennec can activate p3 and win. So if Fennec activates p1, Fennec wins? Let's see: after Fennec activates p1, Snuke activates p2. State: M=1 (p3), available extra=2. Fennec can now either activate p3 and win, or take extra from p2. If Fennec takes extra, M=1, available extra=1, Snuke can activate p3 and win. So Fennec will activate p3 and win. So Fennec wins by activating p1 first. 
2. Activate p2. p2 becomes 2. Active {2}. M=2. Available extra: 2 (from p2). Snuke's turn.
- Snuke could activate p3. Then active {2,3}, p3 becomes 2. M=1. Available extra: 4 (2 from p2, 2 from p3). Fennec must activate p1 and win.
- Snuke could take extra from p2. Then p2 becomes 1. Active {2}. M=2. Available extra: 1. Fennec's turn.
   - Fennec could activate p3. Then active {2,3}, p3=2. M=1. Available extra: 3 (1 from p2, 2 from p3). Snuke must activate p1 and win? Wait, M=1 means p1 is unactivated. Snuke can activate p1 and win. So Fennec activating p3 is losing.
   - Fennec could take extra from p2. Then p2=0. Active {2}. M=2. Available extra: 0. Snuke must activate a pile, say p1. Then active {1,2}, p1=0. M=1. Available extra: 0. Fennec must activate p3 and win. So Fennec can win by taking extra after Snuke took extra? Let's trace: 
     Fennec activates p2 (M=2, avail=2). 
     Snuke takes extra from p2 (p2=1, avail=1). 
     Fennec takes extra from p2 (p2=0, avail=0). 
     Snuke must activate a pile, say p1 (p1=0, active {1,2}, M=1, avail=0). 
     Fennec activates p3 and wins. 
   - Fennec could activate p1. Then active {1,2}, p1=0. M=1. Available extra: 1 (from p2). Snuke can now either activate p3 and win, or take extra from p2 and then Fennec activates p3? Wait, if Snuke takes extra, M=1, avail=0, Fennec activates p3 and wins. So Snuke will activate p3 and win. So Fennec loses if he activates p1 after Snuke took extra.
So from (M=2, avail=2) with Snuke to move, Snuke can take extra, leading to (M=2, avail=1) with Fennec to move. From (M=2, avail=1), Fennec can take extra, leading to (M=2, avail=0) with Snuke to move. Then Snuke is forced to activate a pile, and Fennec wins. So Fennec can force a win. So overall, Fennec wins A=[1,3,3]. Sum=7 (odd) -> Fennec wins. Parity matches.

Let's test a case where sum is odd but second player wins. N=2, A=[1,2] sum=3 odd, Snuke wins. N=2, A=[2,3] sum=5 odd, Snuke wins. N=3, A=[1,1,2] sum=4 even, Snuke wins. N=3, A=[2,2,2] sum=6 even, Snuke wins. N=3, A=[1,1,3] sum=5 odd, Fennec wins. N=3, A=[1,2,2] sum=5 odd, Fennec wins. So far, parity of total sum matches the winner in all tested cases except N=1 where first player always wins regardless of parity. Let's test N=1, A=[2] sum=2 even, but first player wins. So the rule "if sum is odd, first wins; if even, second wins" fails for N=1. But the problem constraints say N >= 1, and N can be 1. Let's check sample 1: N=3, A=[1,9,2] sum=12 even, but output is Fennec. Wait! Sample 1: N=3, A=[1,9,2]. Sum = 1+9+2 = 12 (even). Output: Fennec. But according to the parity rule, even sum would predict Snuke. So the simple parity rule is incorrect.

Let's verify sample 1. A=[1,9,2], sum=12 even, but Fennec wins. So my earlier conjecture that parity of sum determines winner is false. The sample output is Fennec, so Fennec wins despite even sum. So the plan I wrote is wrong.

I need to reconsider. The plan I had was: "Compute total sum S = ΣA_i, then check parity of (S - N). If (S - N) is odd → Fennec wins, else Snuke wins." Let's test that on sample 1: S=12, N=3, S-N=9, odd -> Fennec. That matches sample 1. Let's test sample 2: N=2, A=[25,29], S=54, S-N=52, even -> Snuke. Matches sample 2. Sample 3: N=6, A=[1,9,2,25,2,9], S=48, S-N=42, even -> Snuke. Matches sample 3. So the rule "parity of (S - N)" matches the samples.

But does it hold for the small cases we tested?
- N=1, A=[2]: S=2, S-N=1, odd -> Fennec. Correct.
- N=1, A=[3]: S=3, S-N=2, even -> Snuke? But we argued N=1 always first player wins. Wait, N=1, A=[3]: first player must activate the only pile. After that, S={1}, game ends. So first player wins. But S-N = 2, even, would predict Snuke. So this is a counterexample! Let's double-check the rules for N=1, A=[3]. The only index is 1. Fennec chooses i=1. A_1 becomes 2. Since i=1 is not in S, add 1 to S. Now S={1}. Condition S={1,2,...,N} is satisfied (since N=1). The game ends and the player who performed the last operation wins. So Fennec wins. So for N=1, regardless of A_1, the first player always wins. But the formula S-N parity gives odd/even based on A_1-1. For A_1=3, S-N=2 even -> predicts Snuke, but actually Fennec wins. So the formula fails for N=1.

But is N=1 allowed? Constraints: 1 ≤ N ≤ 2×10^5. So yes, N=1 is possible. Let's check if the problem statement has any nuance: "Choose an index i such that 1 ≤ A_i." For N=1, that's always true until A_1 becomes 0, but the game ends as soon as S becomes full, which is after the first move. So indeed first player wins. So any solution must handle N=1 correctly.

But the plan I wrote says: "Compute total sum S = ΣA_i, then check parity of (S - N). If (S - N) is odd → Fennec wins, else Snuke wins." This fails for N=1, A=[3]. So the plan is incomplete.

Wait, maybe the rule is: Fennec wins if S is odd? Let's test: N=1, A=[3], S=3 odd -> Fennec. N=1, A=[2], S=2 even -> Fennec? No, would be Snuke. So not that.

Maybe the rule is: Fennec wins if there is at least one A_i = 1? No, sample 1 has A_1=1 and Fennec wins, sample 2 has no 1 and Snuke wins, sample 3 has 1s but Snuke wins. So not that.

Let's think more carefully. The game is impartial, and we can compute the Grundy number or winning position. However, the game ends when all indices are covered. This is a "poset" game: the covering condition is a set of N elements. Each move can either add a new element to the set (if not already present) or do nothing to the set but consume a token from an already present element. The game ends when the set is full. The number of tokens is finite. This is similar to the game of "Nim with a pass" or "Nimble"? Actually, it's like each heap has a "key" token that opens a lock. Once all locks are opened, the game stops.

We can think of the game as: we have N locks. Each lock i requires one key to open. Lock i has a_i keys. The keys are identical, but you can only use a key from lock i after that lock is opened? No, the keys are tokens in the heap. The first key taken from heap i opens lock i. After that, you can take more keys from that heap, but they are just extra moves. The game ends when all locks are opened. The player who opens the last lock wins. The extra keys can be taken at any time after the lock is opened, but taking them does not change the lock state. So the game is: there are N "required" moves (one per lock) and E = Σ (a_i - 1) "optional" moves. The optional moves can only be played on locks that are already opened. So the availability of optional moves depends on which locks are opened.

This is a partisan game? No, both players have the same moves. It's impartial. The state can be described by a binary vector of which locks are opened, and a vector of remaining keys for each lock. The game ends when all locks are opened. The player who makes the last move (opens the last lock) wins.

We can try to find a simple characterization. Let's denote by a_i the size of heap i. The first player wins if and only if the XOR of something? Or maybe it's related to the parity of the number of heaps with odd size? Let's test.

Sample 1: A=[1,9,2] -> odd sizes: 1,9 are odd, 2 even. Two odd. Sample 1: Fennec wins.
Sample 2: A=[25,29] -> both odd. Two odd. Snuke wins.
Sample 3: A=[1,9,2,25,2,9] -> odds: 1,9,25,9 -> four odd. Snuke wins.
So not just parity of odd count.

Another idea: The game is equivalent to a Nim heap where each heap i contributes a Grundy value of a_i mod 2? But the game ends condition is special.

Let's consider the game as a normal play impartial game where the terminal positions are those where all locks are opened and no keys remain? Actually, the game ends as soon as all locks are opened, regardless of remaining keys. So it's a "shortened" game. The winning condition is to make the move that opens the last lock. This is similar to the game of "Dawson's Kayles" or "Treblecross"? Not exactly.

We can model the game as: start with N unopened locks. Each lock i has a_i - 1 "extra" tokens that become available only after the lock is opened. The move options:
- Open an unopened lock i: this consumes 1 token from i and opens the lock. (This is always possible as long as a_i >= 1, which is given.)
- If lock i is open and has remaining tokens, you can consume one token.

The game ends when all locks are open. The player who opens the last lock wins.

This is a typical impartial game that can be solved by computing the Grundy value of the starting position, or by finding a simpler invariant. Since N can be up to 2e5 and A_i up to 1e9, we need an O(N) or O(N log N) solution.

Observation: The extra tokens are like "passes" that can be used to flip the turn, but they are only available after the corresponding lock is opened. So the game is about controlling the parity of the number of moves remaining until the last lock is opened.

Let’s define a state by the set of open locks and the number of remaining tokens on open locks. However, we can simplify: Since the only thing that matters is the total number of moves played before the last lock is opened, and the players can choose to play extra moves or not, the key is whether the second player can force the last lock to be opened on their turn.

Consider the total number of moves if both players play "optimally". Actually, we can think of the game as: the players will open locks until all are open. Between opening locks, they can insert extra moves. The player who is forced to open a lock when there are no extra moves available (i.e., all extra moves have been exhausted) will determine the parity based on the number of locks left.

Specifically, suppose we ignore the availability constraint and think of the game as having N "key" moves and E extra moves. The key moves must be played in some order, and extra moves can be played at any time. However, an extra move from lock i can only be played after the key move for lock i. So the extra moves are "colored" by the lock they belong to. They can be played only after that lock is opened. This is a crucial restriction.

Let’s define for each lock i, after it is opened, it provides a_i - 1 extra moves that can be used immediately or later. The game ends when all N locks are opened. So the sequence of moves is: open some lock, then maybe use some of its extras, then open another, etc. The last move must be opening the final lock.

We can think of the game in reverse: The last move is opening the last unopened lock. Before that, there is some number of extra moves available from the already opened locks. The player who makes the second-to-last move might want to either open a lock or use an extra move, depending on the parity of the remaining moves.

Let k be the number of locks that are still unopened at some point. Let e be the number of extra moves available from the currently opened locks. The state is (k, e) plus the distribution of extras among locks? But since extras from different locks are indistinguishable in effect (they just consume a move and don't change k), the exact distribution doesn't matter, only the total number of extras available. However, the distribution matters for future availability: when you open a new lock, you add its extras to the pool. So the state is more detailed: for each lock, whether it is open and how many extras it has. But we can think of the game as: we have a set of closed locks, each with a certain number of "future extras" that will become available when opened. The open locks have some available extras.

A known result for this type of game: The first player wins if and only if the XOR of (A_i - 1) is non-zero? Or something like that. Let's test.

Sample 1: A=[1,9,2] -> A_i-1: [0,8,1]. XOR: 0 xor 8 = 8, 8 xor 1 = 9. Non-zero -> Fennec wins. 
Sample 2: A=[25,29] -> A_i-1: [24,28]. XOR: 24 xor 28 = 4 (since 24=11000, 28=11100, XOR=00100=4). Non-zero -> predicts Fennec, but sample says Snuke. So not that.

Maybe XOR of A_i? Sample 1: 1 xor 9 = 8, 8 xor 2 = 10 (non-zero) -> Fennec. Sample 2: 25 xor 29 = 4 (non-zero) -> predicts Fennec, but Snuke. So no.

Maybe the game reduces to Nim with heap sizes A_i, but the last move is special? Actually, this game is known as "The game of Euclid" or "Turning Turtles"? Let's search memory: There is a game where you have piles, and you can take any number of objects from a pile, and the player who takes the last object wins. That's Nim. Here, the first object taken from a pile also "opens" it, and the game ends when all piles are opened. This is similar to "Nim with a pass" but with a finishing condition.

Consider the total number of moves: each move reduces some A_i by 1. The game ends when all indices have been chosen at least once. So the number of moves is at least N, and at most Σ A_i. The players can choose to prolong the game by taking from already opened piles, but they cannot shorten it below N. The winner is determined by who makes the N-th distinct move (the one that opens the last unopened pile). Let M be the total number of moves actually played. Then M = N + W, where W is the number of "waste" moves (taking from already opened piles). The player who makes the N-th distinct move wins. Since moves alternate, the parity of N + W determines the winner. The first player wants N + W to be odd (i.e., W even if N is odd, W odd if N is even). The second player wants the opposite.

The question is: can the second player force W to have a certain parity? This depends on the availability of waste moves at the right times. The game is a race to the N-th distinct move, with the ability to "pass" by taking from opened piles, but passes are limited by the sizes of the piles.

This is similar to a game where you have N "tokens" to collect, and each pile i gives you one token (the first time you take from it) and then gives you (A_i - 1) passes. The passes can be used at any time after the token is collected. The game ends when all tokens are collected. The player who collects the last token wins. The passes are like extra turns that can be inserted.

We can think of the game as: there are N "mandatory" moves (collecting tokens) and E = Σ (A_i - 1) "optional" moves (passes). The passes are initially locked; they become available only after the corresponding token is collected. The game ends when all N tokens are collected. The player who collects the last token wins. The passes can be used to change who makes the next move.

This is a classic impartial game: "Turning Turtles" or "Nim with a key"? I recall a problem: "Fennec and Snuke" from AtCoder? Actually, this looks like an AtCoder problem. The solution might be to compute the XOR of (A_i - 1) or something, but we saw that fails for sample 2.

Let's analyze the game more formally. We can consider the game as a normal play impartial game on a graph. The state can be represented by a bitmask of opened piles and the remaining tokens. But N is up to 2e5, so we need a simpler invariant.

Observe that the game is symmetric except for the A_i. The key is that each pile i contributes a "mandatory" move and A_i - 1 "optional" moves. The optional moves are only available after the mandatory move. So the game is equivalent to: we have N "stars" to collect. Each star i is located on a path of length A_i. To collect star i, you must move along the path from the start to the star (one step). After collecting the star, you can continue moving on the path (extra steps). The game ends when all stars are collected. The player who makes the step that collects the last star wins. The paths are independent; you can move on any path as long as you have steps left. But you can only move on path i if you are currently on path i? No, you can choose any index i with A_i > 0, regardless of whether it's collected. So you can jump between paths arbitrarily. So the paths are independent but you can switch.

This is similar to a game where you have N piles, and you can take one object from any pile. The first object taken from pile i "scores" a point. The game ends when all piles have scored at least one point. The player who scores the last point wins. The objects taken after the first from a pile are just extra moves.

This is known as the "game of Nim with a scoring condition". I think the solution is to compute the XOR of (A_i - 1) for all i, and if it's 0, the second player wins, else first player wins. But we saw sample 2 contradicts that. Wait, sample 2: A=[25,29], A_i-1 = [24,28], XOR=4 ≠ 0, so first player would win, but Snuke wins. So maybe the XOR is of A_i? 25 xor 29 = 4 ≠ 0 -> Fennec. No.

Maybe the condition is on the parity of the number of piles with even A_i? Or something with the number of A_i that are 1?

Let's compute for the small cases we tested:
- N=1, A=[2]: A_i-1 = [1], XOR=1. First player wins.
- N=1, A=[3]: A_i-1 = [2], XOR=2. First player wins.
- N=2, A=[1,1]: A_i-1 = [0,0], XOR=0. Second player wins. (Matches)
- N=2, A=[1,2]: A_i-1 = [0,1], XOR=1. First player? But Snuke wins. So XOR non-zero but second wins. So not that.
- N=2, A=[2,2]: A_i-1 = [1,1], XOR=0. Second wins. (Matches)
- N=2, A=[2,3]: A_i-1 = [1,2], XOR=3. First? But Snuke wins.
- N=2, A=[1,3]: A_i-1 = [0,2], XOR=2. First? Snuke wins.
- N=2, A=[2,4]: A_i-1 = [1,3], XOR=2. First? Let's simulate: A=[2,4], M=2, E=1+3=4. Fennec mandatory on p1 (A1=1). State: active {1}, M=1, avail=1. Snuke can take mandatory on p2 and win, or take extra from p1. If Snuke takes extra, M=1, avail=0, Fennec mandatory on p2 and wins. So Snuke will take mandatory and win. So Snuke wins. So XOR=2 non-zero but Snuke wins.

So XOR of (A_i-1) is not the answer.

Maybe the game is equivalent to a Nim heap where the size is A_i mod 2? Let's test parity of A_i. 
Sample 1: odds: 2 (1,9). Sample 1: Fennec wins.
Sample 2: odds: 2. Sample 2: Snuke wins.
Sample 3: odds: 4. Sample 3: Snuke wins.
So not just parity of odd count.

Maybe the rule is: Fennec wins if and only if the number of A_i that are 1 is odd? 
Sample 1: number of 1s: 1 (A1=1). Fennec wins.
Sample 2: number of 1s: 0. Snuke wins.
Sample 3: number of 1s: 1 (A1=1). But Snuke wins. So no.

Wait, sample 3 has a 1, but Snuke wins. So not that.

Let's think about the game as a combinatorial game with passes. There is a known theorem: In a game where you have a set of "options" and "passes", the outcome is determined by the parity of the number of options modulo something. Actually, we can model the game as: each pile i is a "subgame" that can be played in two phases: first you must play the "opening" move, which gives you access to a Nim heap of size A_i - 1. The opening move is a move that ends the subgame if it's the last opening? Not exactly.

This is similar to the game of "Dawson's Kayles" where you have a row of pins, but not.

Another approach: Since the game is impartial and the moves are symmetric, we can try to compute the Grundy value of a single pile. However, the piles are not independent because the game ends when all are opened. This is a "disjunctive sum" of subgames with a global termination condition. This is not a standard disjunctive sum because the game ends when all subgames are "initialized". This is more like a "conjunctive" game: the game ends when all subgames reach a certain state. In combinatorial game theory, this is called a "conjunctive sum" or "all-play" condition. The theory for such games is more complex.

However, there is a known result for this specific game: It is equivalent to a Nim heap of size (Σ (A_i - 1)) and the first player wins if that sum is odd? Let's test: 
Sample 1: Σ(A_i-1) = 0+8+1 = 9 (odd) -> Fennec wins.
Sample 2: Σ(A_i-1) = 24+28 = 52 (even) -> Snuke wins.
Sample 3: Σ(A_i-1) = 0+8+1+24+1+8 = 42 (even) -> Snuke wins.
This matches all samples! And earlier we saw N=2, A=[1,2]: Σ(A_i-1) = 0+1 = 1 (odd) -> first player? But we found Snuke wins. Let's double-check A=[1,2]. 
A=[1,2], N=2. Σ(A_i-1) = 1. If the rule is "first player wins iff Σ(A_i-1) is odd", then Fennec should win. But earlier I simulated and got Snuke wins. Let's re-simulate carefully.
A=[1,2]. Fennec moves.
- Option 1: Fennec chooses i=1. A1 becomes 0, S={1}. Now S is not full. Remaining mandatory: i=2. A2=2. Snuke's turn. Snuke must choose i=2 (only i with A_i>0). A2 becomes 1, S={1,2}. Game ends. The player who performed the last operation is Snuke. So Snuke wins.
- Option 2: Fennec chooses i=2. A2 becomes 1, S={2}. Remaining mandatory: i=1. A1=1. Snuke's turn. Snuke must choose i=1 (only i with A_i>0). A1 becomes 0, S={1,2}. Game ends. Snuke wins.
So in both cases, Snuke wins. So Σ(A_i-1) = 1 is odd, but Snuke wins. So the rule "Fennec wins iff Σ(A_i-1) is odd" fails for [1,2].

But wait, in my earlier test of [1,2], I said Snuke wins, and Σ(A_i-1)=1 odd, so if the rule were that, it would predict Fennec, which is wrong. So the rule cannot be just parity of Σ(A_i-1).

However, note that in [1,2], N=2, and Σ(A_i-1) = 1. The total sum S = 3, which is odd. The rule "S odd -> Fennec" would predict Fennec, but Snuke wins. So the simple parity rules are insufficient.

Let's analyze the game more carefully. The game ends when the last unopened pile is opened. The number of moves is at least N. The players can insert extra moves. The critical point is that extra moves can only be played on already opened piles. So if at some point, all remaining unopened piles have size 1 (i.e., no extra moves available even after opening), then the game will end in exactly the number of remaining unopened piles moves, with no chance to insert extras. So the parity of the number of remaining unopened piles when the game enters a "no extras" state determines the winner from that state.

More systematically, we can think of the game as: we have piles. The game proceeds in "phases". Initially, some piles may have size > 1. The first player can choose to open a pile with size > 1, thereby creating extra moves. The second player can then use those extra moves to flip parity. This is similar to the game of "Nim with a pass" where the number of passes is determined by the sizes of the piles you open.

In fact, this game is known as "The Game of Nim with a Pass" or "Nim with a Free Move"? No, there is a specific game: "Fennec and Snuke" is likely from an AtCoder contest. I recall a problem where the answer is based on the parity of the number of piles with even size, or something like that. Let's search memory: There is an AtCoder problem "Fennec and Snuke" (maybe from ABC or ARC). The solution might be: If there is at least one pile with size > 1, then the first player can force a win by making a certain move, else the winner is determined by parity of N. But sample 1 has A=[1,9,2], which has >1, and Fennec wins. Sample 2 has all >1 (25,29), and Snuke wins. Sample 3 has >1, and Snuke wins. So not simply existence of >1.

Maybe the condition is on the number of piles with odd size? Sample 1: 2 odd, 1 even. Sample 2: 2 odd, 0 even. Sample 3: 4 odd, 2 even. So not clear.

Let's compute for A=[1,2] (N=2): odd count: 1 (only 1 is odd? 1 is odd, 2 is even. So 1 odd). Parity of odd count is odd. Sample 1: odd count 2 (even) -> Fennec. So opposite? Sample 1: odd count even -> Fennec. Sample 2: odd count even -> Snuke. So not that.

Let's compute the XOR of A_i for [1,2]: 1 xor 2 = 3 (non-zero) -> Fennec? But Snuke wins. So not that.

Maybe the game is equivalent to a Nim heap where the heap size is the number of piles with A_i = 1? No.

Let's try to compute the Grundy value for small N and see pattern.
Define a state by a tuple (a1, a2, ..., an) with ai >= 1. The game ends when all indices have been chosen at least once. This is complex.

Alternatively, we can think of the game as: the players are building a set S. Each move either adds a new element to S (if possible) or not. The game ends when S is full. The only constraint is that to add element i, you must have A_i >= 1, and each move reduces some A_i by 1. So it's like a game of "collecting coupons" with limited supply.

This is reminiscent of the "coupon collector" game. I think the solution is to compute the XOR of (A_i - 1) for all i, but with a twist: if all A_i = 1, then the game is just taking turns, and the winner is determined by parity of N. If there is at least one A_i > 1, then the first player can force a win if and only if the XOR of (A_i - 1) is non-zero? But sample 2 has A_i > 1 and XOR of (A_i-1) is 24 xor 28 = 4 != 0, but Snuke wins. So not that.

Wait, sample 2: A=[25,29]. A_i-1 = [24,28]. XOR=4. Non-zero. So if the rule were "non-zero XOR -> first player wins", sample 2 would be Fennec, but it's Snuke. So maybe the XOR is of something else: maybe A_i mod 2? 25 mod 2 = 1, 29 mod 2 = 1. XOR = 0. Snuke wins. Sample 1: [1,9,2] mod 2: [1,1,0]. XOR = 0. Fennec wins. So no.

Maybe the rule is: Fennec wins if the number of A_i that are odd is odd? Sample 1: 2 (even) -> Fennec. Sample 2: 2 (even) -> Snuke. So no.

Let's think about the game as a normal play game on a directed graph. The state can be represented by a bitmask of opened piles and a vector of remaining tokens. But we can simplify by noting that the order of opening piles doesn't matter except for the sizes. Actually, the sizes matter because opening a large pile gives extra moves that can be used immediately or later.

Consider the total number of moves if both players play "optimally". The first player wants to control the parity of the total moves. The second player wants the opposite. The total moves is N + W, where W is the number of waste moves. The players can influence W by choosing when to take waste moves. However, waste moves are only available after the corresponding pile is opened. So the game is about who gets to use the waste moves.

This is similar to a game where you have N "keys" and E "coins". Each key i gives you a_i - 1 coins when opened. The game ends when all keys are opened. You can spend coins at any time (one per turn) to pass. The player who opens the last key wins. This is exactly the game of "Nim with a pass" where the number of passes is the total number of coins. However, the coins are not all available at the start; they are locked behind keys. So the game is like: you have a set of locked coins. To use the coins from a key, you must first use a key to open it. This is similar to the game of "Dawson's Chess"? Not.

We can solve this by dynamic programming on the number of keys? But N is up to 2e5, so we need a closed form.

Observe that the game is symmetric under renaming indices. The only thing that matters is the multiset of A_i. The game is determined by the values A_i. We can try to see if there is an invariant like the XOR of the A_i or something, but we saw counterexamples.

Let's compute the outcome for all small N and small A_i to see a pattern. We can write a small program to compute the winning positions for small N (N=1,2,3) and A_i up to small values. But since I'm not running code, I'll try to reason.

From our tests:
N=1:
A=1: Fennec wins.
A=2: Fennec wins.
A=3: Fennec wins.
So for N=1, Fennec always wins.

N=2:
A=[1,1]: Snuke wins.
A=[1,2]: Snuke wins.
A=[1,3]: Snuke wins.
A=[1,4]: Snuke wins.
It seems for N=2, if one pile is 1 and the other is anything, Snuke wins. What about both >1?
A=[2,2]: Snuke wins.
A=[2,3]: Snuke wins.
A=[2,4]: Snuke wins.
A=[3,3]: Snuke wins.
A=[3,4]: Snuke wins.
It appears for N=2, Snuke always wins? Let's test A=[2,5] maybe. But from our analysis, for N=2, the first player opens a pile. Then the second player can always open the last pile and win, unless the first player opens a pile and then the second player is forced to open the last pile? Actually, after first player opens a pile, there is one pile left. The second player can open it and win. The only way the first player could win is if after opening a pile, the second player is forced to take a waste move instead of opening the last pile. But that requires that after the first move, there is a waste move available and the second player chooses to take it, and then the first player opens the last pile. But the second player is optimal, so they will not take a waste move if it allows the first player to win. So the second player will always open the last pile if possible. The only exception is if after the first move, there are no waste moves available (i.e., the opened pile had A_i=1, so no extras), and also the other pile has A_j=1, so the second player must open it and wins. If the opened pile had A_i>1, then there is a waste move available. The second player could choose to take the waste move instead of opening the last pile. If they do, then the first player will open the last pile and win. So the second player will not take the waste move; they will open the last pile and win. So indeed, for N=2, the second player always wins, regardless of A_i. Wait, is there any case where the first player can force a win? Suppose A=[1,1]. First player opens one (wins? No, game doesn't end until both opened. So after first move, one opened, one left. Second player opens last and wins. So Snuke wins. A=[1,2]: first opens 1, then second opens 2 and wins. First opens 2 (A2 becomes 1), then second opens 1 and wins. So Snuke wins. A=[2,2]: first opens one, A becomes 1, extras available. Second can open the other and win. If second takes extra, first opens last and wins, so second will not. So second wins. So indeed, for N=2, Snuke always wins. This is a strong observation: For N=2, Snuke always wins. Let's verify with N=2, A=[1,100]. Fennec opens 1. Then Snuke opens 100 and wins. So yes.

Now N=3. We saw:
A=[1,1,1]: Fennec wins.
A=[1,1,2]: Snuke wins.
A=[1,1,3]: Fennec wins.
A=[1,2,2]: Fennec wins.
A=[1,2,3]: ? Let's analyze A=[1,2,3]. 
Fennec moves. Options:
- Open 1: then state: opened {1}, M=2, A=[0,2,3]. Snuke can open 2 or 3.
  * If Snuke opens 2: state opened {1,2}, M=1, A=[0,1,3]. Fennec can open 3 and win.
  * If Snuke opens 3: state opened {1,3}, M=1, A=[0,2,2]. Fennec can open 2 and win.
  So if Fennec opens 1, Fennec wins? But wait, Snuke might not open a pile; Snuke could take a waste move. After Fennec opens 1, there are no waste moves (since A1 was 1). So Snuke must open a pile. So Fennec wins. So opening 1 is a winning move.
- Open 2: A2 becomes 1. State: opened {2}, M=2, A=[1,1,3]. Snuke's turn.
  * Snuke could open 1: state opened {1,2}, M=1, A=[0,1,3]. Fennec opens 3 and wins.
  * Snuke could open 3: state opened {2,3}, M=1, A=[1,1,2]. Fennec opens 1 and wins.
  * Snuke could take waste from 2: A2 becomes 0. State: opened {2}, M=2, A=[1,0,3]. No waste available. Fennec must open a pile. Fennec can open 1: then Snuke opens 3 and wins. Or Fennec opens 3: then Snuke opens 1 and wins. So if Snuke takes waste, Snuke wins. So Snuke will take waste and win. So opening 2 is losing.
- Open 3: A3 becomes 2. State: opened {3}, M=2, A=[1,2,2]. Snuke's turn.
  * Snuke could open 1: state opened {1,3}, M=1, A=[0,2,2]. Fennec opens 2 and wins.
  * Snuke could open 2: state opened {2,3}, M=1, A=[1,1,2]. Fennec opens 1 and wins.
  * Snuke could take waste from 3: A3 becomes 1. State: opened {3}, M=2, A=[1,2,1]. Now Snuke has taken one waste, leaving one waste. Fennec's turn.
      - Fennec could open 1: state opened {1,3}, M=1, A=[0,2,1]. Waste available: 1. Snuke can take waste or open 2. If Snuke takes waste, M=1, waste=0, Fennec opens 2 and wins. So Snuke will open 2 and win. So opening 1 is losing.
      - Fennec could open 2: similarly, Snuke will open 1 and win.
      - Fennec could take waste from 3: A3 becomes 0. State: opened {3}, M=2, A=[1,2,0]. No waste. Fennec took waste, so now Snuke's turn. Snuke opens a pile, Fennec opens last and wins? Wait: after Fennec takes waste, state: opened {3}, M=2, A=[1,2,0]. Snuke must open a pile, say 1. Then opened {1,3}, M=1, A=[0,2,0]. Fennec opens 2 and wins. So if Fennec takes waste, Fennec wins. So from state after Snuke took waste (opened {3}, A=[1,2,1], M=2), Fennec can win by taking waste. So Snuke taking waste leads to a win for Fennec. So Snuke will not take waste. Thus opening 3 is a winning move (since Snuke's other moves lose).
So for A=[1,2,3], Fennec has winning moves (open 1 or open 3). So Fennec wins. Sum=6 even. So parity of sum fails.

Now A=[2,2,3] for

## worker: Continue analyzing the game to derive the correct 
I wrote a brute-force program to compute the winning positions for small N and A_i. I will run it to see the output and then analyze the pattern.

## worker: Run the brute-force program (already started) to g
The brute-force program is run to generate the full table of winning/losing positions for N=1,2,3 and A_i in {1,2,3,4}. The output will be analyzed to find a pattern.
