The game ends when each index has been "activated" at least once. Once an index i is in S, further decrements of A_i are free (they don't change the set). Each A_i can be thought of as: one "activation" cost followed by (A_i - 1) "free" decrements. The total number of moves is sum(A_i). The only strategic choice is the order in which indices are first activated. Each player wants to be the one to make the move that completes the set S.

The key observation: after all indices are activated, the remaining moves are forced (free decrements), and they happen in the same order they are played. The winner is determined by who makes the activation that adds the last new index to S.

If we think of each A_i as a pile of tokens, the first token activates index i, subsequent tokens are "free". Players can interleave activations of different indices. This is a classic impartial game: each pile's first move is "special" (activates), rest are normal. The last special move wins (since the player who activates the last index ends the game immediately on that turn, regardless of free moves).

To analyze: sort A_i. The largest pile's first token is "most valuable" because activating it late means more free moves after. Actually, optimal play: players will want to delay or accelerate activations. 

Let me think more carefully. The game is a normal-play impartial game. The Sprague-Grundy value: for pile of size A, the first move is special (activates), subsequent moves are not. But the interaction is complex because activations of different indices can be interleaved.

Simpler analysis: Consider the total number of moves T = sum A_i. The game ends when S is full. The last move is the one that adds the final index. After that point, no more moves happen (game ends immediately). So we need to determine who makes the last "first-time" activation.

Equivalently, ignore the "free" decrements - they are forced and the player who makes the k-th activation wins if k is the number of distinct indices. But free moves can be inserted between activations.

Actually, each pile of size A_i contributes: 1 "activation" move and (A_i - 1) "free" moves. Free moves are like pass moves that don't change game state. The player who makes the N-th activation wins (since game ends immediately).

So the game is: there are N "activation" moves (one per pile) and (sum A_i - N) "free" moves. Players alternate. The player who makes the N-th activation wins. Free moves can be played at any time (they don't affect who wins, they just delay).

A free move is equivalent to a "pass" - it skips your turn essentially, but the turn passes to opponent. Wait, free moves are still turns. So if you play a free move, opponent gets next turn.

The game: total T moves. Turn T is made by some player. The game ends at the N-th activation (not necessarily the last move). After the N-th activation, no more moves.

Let me reconsider. The player who makes the move that completes S wins. This is the N-th distinct activation. Moves after that don't happen.

Key insight: The last activation is more "powerful" because it immediately ends the game. If it's your turn and only one index remains unactivated, and A_i >= 1 (which it is by problem guarantee until game ends), you can activate it and win.

This is equivalent to a game where each pile has one "winning move" (activation) and the rest are "pass moves". The player who makes the N-th activation wins.

Let me think of it as: sort A_i. Consider the game where you must take tokens, and the first token from each pile is "special". A standard result: the first player wins iff the maximum A_i > sum of others, or something like that? No, this is a different game.

Actually, let me reconsider. This is similar to "Dawson's Kayles" or other take-away games, but simpler.

Alternative view: Each A_i = 1 means index i MUST be activated on its only move. So indices with A_i = 1 are forced activations.

Let's define: after sorting A_1 <= A_2 <= ... <= A_N. 

Claim: Fennec wins iff there exists i such that A_i > sum_{j>i} A_j + (N - i) ... no wait.

Let me think differently. This is a known problem from AtCoder. The answer involves comparing A_N (max) with sum of others.

Actually, the structure: each pile i has A_i tokens. The first token taken from pile i "activates" it. The game ends when all piles are activated. The player who activates the last pile wins.

Think of it as: each pile has a "cost" of A_i moves, the first being the activation. The total number of moves is sum A_i. The game ends at move number k where the k-th move is the last activation. Moves k+1, ..., sum A_i never happen.

If players play optimally, the last activation happens as early as possible for the winning player, or as late as possible for the losing player.

Standard analysis for this type of game (known as "token game" or similar): 

Consider the sorted array. The last activation will be of the pile with the largest A_i (or one of them, if tied). Why? Because to delay the game, you'd want to save the large pile's activation for last.

Wait, the activation is the FIRST move on a pile. So the pile with largest A_i: its first move is just 1 of its A_i moves. The last A_i - 1 moves are free.

Hmm, let me look at this from the perspective of: when is the game forced to end? It's not forced until all indices are activated. The losing player would want to delay, the winning player wants to end quickly.

Let's think about small cases:
- N=1, A=(a): Only one index, activation on first move. Fennec wins. ✓
- N=2, A=(a,b) with a<=b: 
  - Total moves = a+b. Fennec wants to be the one to activate index 2.
  - If Fennec activates index 1 first (move 1), then there are a-1 free moves on index 1, and b moves on index 2. The b-th move on index 2 (which is its activation, since not yet activated) ends the game. If Fennec activates index 1, Snuke can be forced to activate index 2? No, either player can choose.
  - This is complex. Let me think...

Actually, the key insight for this problem (it's a classic): 

Sort A in non-decreasing order. Fennec wins iff 2*A_N > sum(A) + 1, i.e., A_N > sum of rest + 1, or specifically some condition involving the largest and the rest.

Wait, I recall this problem. The answer is: let M = max A_i, S = sum A_i. The game is equivalent to Nim-like analysis.

Let me think again. Consider the sorted array. The optimal strategy involves the largest pile. 

New approach: think of each A_i as contributing 1 "activation" and (A_i - 1) "free" moves. The game is determined by who makes the N-th activation.

If we ignore the game-ending condition, the game lasts sum(A_i) moves, and the last move is by some player. But the game ends early at the N-th activation.

The N-th activation: the player who makes it wins immediately. So both players want to control when the N-th activation happens.

For the player who wants the N-th activation to happen on their turn: they want to make activations quickly.
For the opponent: they want to delay, playing free moves.

The last pile to be activated: the one whose activation is the N-th. Which pile is this? It's the pile that both players have been avoiding, OR the one that gets forced.

This is equivalent to: the game is a race to make N activations. Each turn, you can either make an activation (if unactivated piles remain) or a free move. But you can only make a free move on an already-activated pile.

So the game state is (activated, free_moves_available). The number of free moves available = sum of (A_i - 1) for activated i. The number of unactivated piles = N - |activated|.

A player on their turn can:
1. Activate an unactivated pile (if any), spending 1 of its A_i tokens.
2. Do a free move on an activated pile.

The game ends when all piles are activated (the activation move that completes this wins).

This is equivalent to: there are N "activation slots" and F = sum(A_i) - N "free slots". Players alternate choosing a slot. The player who fills the last activation slot wins.

The free slots don't matter for the win condition, but they determine whose turn it is when activations are made.

If a player always activates when possible, they make activations on turns 1, 3, 5, ... (odd turns). If they have to do a free move, it shifts parity.

The optimal strategy: a player will activate if doing so doesn't lose. Specifically, on turn k, if there's 1 unactivated pile left, the player to move wins by activating it.

So we can analyze backwards or think about parity.

Total moves: T = sum(A_i). The game ends at move k where k is the index of the N-th activation. Then the winner is Fennec if k is odd, Snuke if k is even.

Players control k. The winning player wants k to have their parity, the losing player wants the opposite.

The range of k: minimum is N (if all activations happen first, no free moves interspersed). Maximum is T (if free moves happen first, but free moves can only happen on activated piles, so the first move must be an activation...).

Wait, the first move is always an activation (no free moves available initially). After the first activation, there are free moves available.

The minimum k: all N activations are done first. Move N is the N-th activation. Winner: Fennec if N is odd, Snuke if N is even.

The maximum k: free moves are interspersed as much as possible. The pattern would be: activation, then all available free moves, then next activation, etc. But free moves on a pile can only happen after that pile is activated.

So the sequence of "available free moves" grows as piles are activated. After activating pile i (with A_i tokens), we have A_i - 1 new free moves.

The maximum k is achieved by: after each activation, do all available free moves before next activation. Then k = T (all free moves done before next activation means activations happen at moves 1, 1+(A_{(1)}-1)+1, ...). The last activation is at move T.

So k can range from N to T. Fennec wants k odd, Snuke wants k even.

This is a complex combinatorial game. Let me think about the structure differently.

Equivalent game: We have N piles. A move is either "activate pile i" (if not activated) or "take from pile i" (if activated). The game ends when all piles are activated; the player who activates the last pile wins.

This is known as a "poset game" or "subtraction game with activation". 

Standard result for this type: sort A_i ascending. Fennec wins iff 2*A_N > S + 1, where S = sum A_i... no, let me derive it.

Let's denote sorted A_1 <= A_2 <= ... <= A_N.

Consider the game from Snuke's perspective (he wants k even). He can delay by playing free moves. Fennec can speed up by activating.

If A_N is very large, Snuke can keep playing free moves on pile N, forcing the game to last a long time. If A_N is small, the game ends quickly.

Specifically, consider the "extra" tokens: A_i - 1 for each i. These are free moves. But they can only be used after activation.

Hmm, I think the correct analysis is:

The game outcome depends on the comparison between A_N (the maximum) and the sum of the rest plus 1.

Let me verify with samples:
Sample 1: A = (1, 9, 2), sorted = (1, 2, 9). A_N = 9, sum rest = 3. 9 > 3+1 = 4? Yes. Fennec wins. ✓
Sample 2: A = (25, 29), sorted = (25, 29). A_N = 29, sum rest = 25. 29 > 25+1 = 26? Yes. Fennec wins? But answer is Snuke. ✗

So that's wrong. Let me re-examine.

Sample 2: A=(25,29), sum=54, N=2. 54 moves total. Fennec wants k odd, Snuke wants k even. k ranges from 2 to 54.

If Fennec activates pile 1 on move 1. Then pile 1 has 24 free moves. Snuke can do free moves on pile 1, or activate pile 2. If Snuke activates pile 2 on move 2, k=2, Snuke wins. So Fennec shouldn't activate pile 1 first.

If Fennec activates pile 2 on move 1 (A_2=29). Then pile 2 has 28 free moves. Snuke can activate pile 1 on move 2, k=2, Snuke wins. Or Snuke does free moves on pile 2, extending the game.

So Fennec activating either pile first leads to Snuke being able to activate the other on move 2 and win.

Unless... Fennec can avoid this? No, the opponent always has the option to activate the remaining unactivated pile on their turn.

So when N=2, the first player (Fennec) activates one pile, and the second player (Snuke) can always activate the other and win (since k=2 is even). Unless there's a way to prevent this, but there isn't if A_i >= 1 for all i.

Wait, but the problem says N=2, A=(25,29), answer is Snuke. That matches: Fennec activates one, Snuke activates the other, k=2, Snuke wins. But then Fennec can never win with N=2? Only if the game forces a different sequence.

Hmm, let me reconsider. Fennec could also play a "free move" on turn 1? No, no free moves available initially. So Fennec must activate on turn 1. Then Snuke can activate the other on turn 2 and win.

So for N=2, Snuke always wins? But the problem might have cases where Fennec wins with N=2... Let's check constraints. The problem states both players play optimally, and it's determined who wins.

For N=2, Fennec is forced to activate one pile on turn 1 (no free moves exist). Snuke can then activate the other on turn 2 and win immediately. So Snuke always wins for N=2.

But sample 2 has N=2 and Snuke wins, consistent.

Now sample 1: N=3, A=(1,9,2). 
- Turn 1 (Fennec): must activate something. Say index 2 (A=9). 
- Turn 2 (Snuke): can activate index 1 (A=1) or index 3 (A=2), or free move on index 2.
- If Snuke activates index 1: k stays at 1 (1 activation done). 
- Turn 3 (Fennec): can activate index 3. k=2, game continues? No, k=2 means 2 activations done, not all. We need k=N=3.
  
Wait, I confused myself. k is the move number of the N-th activation. The game ends when N-th activation happens. The winner is the player who made that move.

For sample 1 with the given sequence: activations on moves 1 (i=2), 3 (i=1), 5 (i=3). So k=5, odd, Fennec wins. ✓

OK so back to the game tree. Fennec wants to reach a state where the N-th activation is on an odd move. 

For N=2: Fennec activates on move 1, Snuke can activate on move 2 (k=2, Snuke wins). Fennec can't prevent this. So Snuke wins for N=2.

For N=3: Fennec activates on move 1. Snuke can either:
- Activate an unactivated pile on move 2 (k stays at 1 activation). Then Fennec on move 3 can activate the last, k=3, Fennec wins. So Snuke shouldn't do this.
- Do a free move on move 2. Then move 3 is Fennec's, he can activate one of the 2 remaining. Say he activates. k=2 activations done. Then Snuke on move 4 must activate last, k=3, Snuke wins. So Fennec shouldn't activate on move 3.
- Fennec can do a free move on move 3. Then move 4 Snuke activates. k=2. Move 5 Fennec must activate last, k=3, Fennec wins. But wait, Fennec doing a free move on move 3 means move 4 is Snuke's. If Snuke activates on move 4 (k=2), then move 5 Fennec must activate (k=3, Fennec wins). So Fennec can win!

But Snuke wouldn't activate on move 4 if it leads to Fennec winning. On move 4, Snuke can do a free move instead. Then move 5 Fennec activates (k=2), move 6 Snuke activates last (k=3, Snuke wins). 

So the game becomes a battle of free moves. With A=(1,9,2) sorted (1,2,9):
- Fennec activates pile with A=9 on move 1. (Activations done: 1)
- Snuke wants to delay. Available free moves: 8 (from pile 3).
- If Snuke does free move, activations: 1, free: 1, turn 3 Fennec.
- Fennec wants to end. But activating on move 3 means k=2, then Snuke wins. So Fennec does free move too. Turn 4 Snuke.
- Continue... they keep doing free moves on the big pile.
- The big pile has 8 free moves. They alternate free moves.
- After Fennec's activation (move 1), Snuke can do up to 8 free moves before forced to activate.

Wait, the order of activation matters. Let me redo:

After Fennec activates pile 3 (A=9) on move 1, there are 8 free moves on pile 3. 

Snuke on move 2: if activates pile 1 or 2, then 2 activations done. Fennec on move 3 activates the other, k=3, Fennec wins. So Snuke does free move. (free moves used: 1, remaining: 7)

Fennec on move 3: if activates, k=2, then Snuke wins. So Fennec does free move. (free used: 2, remaining: 6)

Snuke on move 4: same analysis, free move. (free used: 3, remaining: 5)

... they alternate free moves ...

After free moves on moves 2,3,4,5,6,7,8,9 (Snuke's turns 2,4,6,8; Fennec's turns 3,5,7,9): 8 free moves used, 0 remaining. Now move 10 is Snuke's turn (since move 9 was Fennec's).

Wait, let me recount:
- Move 1: Fennec (activates pile 3)
- Move 2: Snuke (free)
- Move 3: Fennec (free)
- Move 4: Snuke (free)
- Move 5: Fennec (free)
- Move 6: Snuke (free)
- Move 7: Fennec (free)
- Move 8: Snuke (free)
- Move 9: Fennec (free)

That's 8 free moves (moves 2-9). Move 10 is Snuke. Free moves exhausted (pile 3 had 8 free moves after activation, A=9 means 8 free).

But pile 1 and 2 not activated. Snuke on move 10 must activate. Say pile 1 (A=1, so 0 free moves after activation). Activations: 2. Fennec on move 11 activates pile 2, k=3, Fennec wins.

So Snuke shouldn't have used all free moves. Let's see when Snuke should activate.

The situation: 1 activation done, 8 free moves on pile 3, 2 unactivated piles (1 and 2). 

Snuke wants the 3rd activation to be on an even move (his turn). Currently, Fennec just moved. Next move is Snuke's (even). 

If Snuke activates now (move 2), k=2 activations. Then Fennec on move 3 activates last, k=3 (odd), Fennec wins. Bad for Snuke.

If Snuke does free move, move 3 Fennec. Fennec faces: activate (bad, leads to k=2 then Snuke wins) or free move. So Fennec does free move. Move 4 Snuke.

Pattern: they alternate free moves. After k free moves (k even, done by Snuke), it's Snuke's turn? No, let me track parity.

After Fennec's move 1, move 2 is Snuke (even). 
- After Snuke's free move (move 2): move 3 Fennec (odd).
- After Fennec's free move (move 3): move 4 Snuke (even).
- After Snuke's free move (move 4): move 5 Fennec (odd).
...

The free moves alternate. Both players are forced to do free moves (if they activate, they lose). So the game continues until free moves exhaust or someone is forced to activate.

The free moves on pile 3: 8. If both do free moves alternately starting with Snuke on move 2:
- Snuke: moves 2, 4, 6, 8 (4 free moves)
- Fennec: moves 3, 5, 7, 9 (4 free moves)
Total 8 free moves. After move 9, it's Snuke's turn (move 10). 

Now Snuke must activate (no free moves left, but unactivated piles exist... wait, pile 3 is exhausted, but piles 1,2 unactivated. Free moves on piles 1,2 are 0 since A_1=1, A_2=2, meaning 0 and 1 free moves respectively, but only after activation).

Actually, pile 1 has A=1: no free moves. Pile 2 has A=2: 1 free move after activation. But they're not activated.

So after move 9, only pile 3 is activated and exhausted. Piles 1,2 unactivated. No free moves available. Snuke must activate on move 10. Say pile 1 (no free moves). Then move 11 Fennec activates pile 2 (1 free move, but game ends since k=3). Fennec wins.

Alternative for Snuke on move 10: activate pile 2. Then move 11 Fennec activates pile 1. k=3, Fennec wins.

So Snuke loses with this line. But can Snuke deviate earlier? The key is: once Fennec activates the big pile (9), the free moves on it are "trapped" - using them delays, but the parity works against Snuke.

The number of free moves after Fennec's activation is 8. These 8 moves alternate between players (Snuke first). After 8 free moves, it's Snuke's turn, and he must activate, leading to Fennec winning.

If instead, Fennec activates a small pile first (say pile 1, A=1), then:
- Move 1: Fennec activates pile 1. Free moves: 0 on pile 1.
- Move 2: Snuke. Can activate pile 2 or 3, or no free moves. If activates pile 2 (A=2, 1 free), then move 3 Fennec activates pile 3, k=3, Fennec wins. So Snuke should activate pile 3 (A=9, 8 free). Then move 3 Fennec. If Fennec activates pile 2, k=3, Fennec wins. So Fennec does free move on pile 3. Then we have the same situation as before (1 activation of big pile, alternating free moves).

So Fennec's winning strategy: activate pile 1 first, then on move 2 Snuke is forced to either activate pile 2 (Fennec wins on move 3) or activate pile 3 (leading to the free-move battle which Fennec wins).

Wait, if Snuke activates pile 3 on move 2, then move 3 Fennec. Fennec doesn't want to activate pile 2 (loses). Does free move on pile 3. Move 4 Snuke, etc. After 8 free moves (moves 3-10: Fennec 3,5,7,9; Snuke 4,6,8,10), move 11 is Fennec, must activate pile 2, k=3, Fennec wins.

Hmm, but Snuke on move 2 activating pile 3 leads to Fennec winning after 10 moves. What if Snuke activates pile 2 on move 2? Then move 3 Fennec activates pile 3, k=3, Fennec wins immediately. So Snuke's choices both lead to Fennec winning.

Can Snuke deviate by not activating on move 2? No free moves available (only pile 1 activated, A_1=1, no free). So Snuke must activate.

So Fennec wins for sample 1. ✓

Now I see the pattern. The game is about controlling parity via the "free moves" on the largest pile (or more generally, the extra moves).

Let me think of it as: the game is equivalent to a Nim heap of size A_N - 1 (the free moves on the largest pile after activation), and the rest are forced.

Actually, the standard reduction: sort A ascending. The game is equivalent to a single pile of size A_N - (sum of rest) - 1 or something.

Let me think. After the first activation of the largest pile, there are A_N - 1 free moves. The other N-1 piles need to be activated, each takes 1 move (their first move is activation). So the "subgame" is: A_N - 1 free moves and N-1 activations to do.

But activations of other piles can be delayed by free moves on the big pile.

This is getting complex. Let me recall the standard result.

For this problem (I believe it's AtCoder ABC or similar), the answer is:

Let M = max A_i, S = sum A_i. Then Fennec wins iff 2*M > S + 1, or equivalently M > S - M + 1, i.e., M > (sum of others) + 1.

Let me check:
Sample 1: M=9, sum others=3. 9 > 3+1=4. Fennec wins. ✓
Sample 2: M=29, sum others=25. 29 > 25+1=26. Fennec wins. But answer is Snuke. ✗

So that's not right. Let me try another formula.

Sample 2: N=2, A=(25,29). Snuke wins.
Sample 1: N=3, A=(1,9,2). Fennec wins.
Sample 3: N=6, A=(1,9,2,25,2,9). Sort: (1,2,2,9,9,25). Answer: Snuke.

For sample 3: M=25, sum=48, N=6. 25 vs others sum=23. 25 > 23+1=24? Yes (25>24). If formula were M > sum_others+1, Fennec would win. But Snuke wins. So not that.

Let me think about sample 3. A=(1,9,2,25,2,9) sorted (1,2,2,9,9,25). 

The key is the largest pile 25 vs the rest. But also, there are multiple large piles.

Actually, I think the correct formula involves comparing A_N with the sum of all A_i for i < N, or specifically:

Fennec wins iff A_N > sum_{i=1}^{N-1} A_i + (N-1) ... no.

Let me think about the game structure again.

The game: N piles, each with A_i tokens. First token of each pile is "activation". Game ends when all piles activated; player who activates last wins.

This is equivalent to a game on a sorted array. The key insight from combinatorial game theory: 

Sort A ascending. The game value is determined by A_N vs A_{N-1} + A_{N-2} + ... or the "gap".

Actually, I recall now: the game is equivalent to a Nim heap. The Grundy value or the winning condition is:

Fennec wins iff A_N > sum_{i=1}^{N-1} A_i + 1? Let me recheck sample 2: 29 > 25+1=26, yes, so Fennec. But Snuke wins. So no.

Wait, maybe it's: Fennec wins iff A_N >= sum_{i=1}^{N-1} A_i + N - 1? Sample 2: 29 >= 25+1=26, yes. Still Fennec. No.

Hmm. Let me think about sample 2 more carefully. N=2, A=(25,29). 
- Fennec on move 1 must activate one pile. Say pile 1 (25 tokens). 
- Snuke on move 2 can activate pile 2 and win.
- If Fennec activates pile 2 (29 tokens), Snuke activates pile 1 on move 2 and wins.
So for N=2, Snuke always wins. This means for N=2, the first player always loses.

Generalizing: if Fennec is forced to activate, and Snuke can always activate the last pile and win... no, for N>2, Snuke might not want to activate immediately.

For N=2, k=2 always (since first move activates, second move must activate the other). So Snuke (even) wins. 

For N=3, the first player can potentially win (sample 1). The condition must be about the free moves.

Let me think: the game reduces to whether the second player (Snuke) can "keep up" with the free moves to force the last activation on an even move.

Actually, here's a clean way to think about it:

After all activations, the game would last sum(A_i) moves. The actual game ends at the N-th activation. Between activations, free moves are inserted.

Think of the timeline: move 1, 2, ..., T. Some of these are activations (N of them), rest are free (T-N of them). The N-th activation is the winning move.

The set of activation moves is a subset of {1,...,T} of size N. The constraint: when a pile is activated, all previous moves on that pile must be... wait, the activation is the first move on that pile. So if pile i is activated on move m, then moves m+1, m+2, ... on pile i are free, and there are A_i - 1 of them. And no moves on pile i before move m.

So the constraint: the activation moves are ordered, and between move m_i (activation of pile i) and m_i + A_i - 1, those are the free moves on pile i. All moves 1..T are assigned to piles such that pile i's moves are a contiguous block [m_i, m_i + A_i - 1].

So the activations m_1, ..., m_N (distinct) determine the free moves. The game is: players choose the assignment of moves to piles, with the constraint that pile i occupies a contiguous block of length A_i, and the activation is the first move of the block.

The player who chooses m_N (the largest activation move) wins, because that's the N-th activation.

Wait, the activations happen in increasing order of m_i. The N-th activation is the one with the largest m_i.

So the game is: players alternately extend the timeline (assigning the next move to some pile, respecting the contiguity and that activation must come first for each pile). The player who makes the move that completes the last pile's block (i.e., starts the last unactivated pile, or equivalently, the move with the largest m_i) wins.

This is equivalent to: the last pile to be activated is the one started last. The player who starts it wins.

Hmm, I think there's a clean answer. Let me look up or derive.

Consider the sorted array. The optimal play involves the largest pile. The last pile activated is always the largest pile (or one of the largest). Why? Because the largest pile takes the most moves, so it should be started last to maximize delay, or first to minimize delay.

For the player who wants to win (say Fennec), he wants the last activation on an odd move. He can control when to start the last pile.

The last pile to be activated: say it's pile k. Its activation move is m_k. Before m_k, the other N-1 piles are activated, with A_i - 1 free moves each (for i ≠ k). So moves 1 to m_k - 1 consist of: N-1 activations and sum_{i≠k}(A_i - 1) free moves = sum_{i≠k} A_i - (N-1) free moves. Total moves before m_k: (N-1) + sum_{i≠k} A_i - (N-1) = sum_{i≠k} A_i. So m_k - 1 = sum_{i≠k} A_i, thus m_k = sum_{i≠k} A_i + 1.

Wait, that's if all other piles are fully completed before pile k starts. But the contiguity means pile k can't start until... no, pile k can start at any time as long as its block is contiguous. Other piles have their blocks too. The constraint is just that each pile i has its moves in a contiguous block of length A_i, with the activation first.

The total moves T = sum A_i. The last move is T. The last activation m_k is somewhere ≤ T. For the last pile k, its block is [m_k, m_k + A_k - 1], so m_k + A_k - 1 = T (since it's the last pile to finish, assuming no overlap... but blocks can overlap in time, they just need to be contiguous per pile).

Wait, the blocks are disjoint in time (each move is assigned to one pile). The blocks partition {1, ..., T}. The activation of pile i is the start of its block. The last block to start (largest m_i) is the winning move.

So we have N blocks of lengths A_1, ..., A_N partitioning {1,...,T}. The starts are m_1 < m_2 < ... < m_N (wlog). The winning move is m_N.

Now, m_N = T - A_N + 1 (since block N ends at T). So m_N = sum A_i - A_N + 1 = sum_{i<N} A_i + 1.

Wait, that would mean m_N is always sum_{i≠N} A_i + 1, independent of strategy! But that can't be right because the blocks can be in any order (any permutation of the piles determines the blocks). 

Oh I see: the blocks correspond to the piles, but the order of blocks in time is a permutation. The pile with the latest start is the one whose block comes last. The last block ends at T. The start of the last block is T - (length of last block) + 1.

If the last block is pile k (length A_k), then m_k = T - A_k + 1 = sum A_i - A_k + 1.

But the pile with the latest start is the one whose block is placed last in time. To maximize the latest start (delay the game), you place the longest block last. To minimize, place the shortest last.

The winning player wants m_k to be on their turn. m_k = T - A_k + 1, where k is the pile placed last.

The players choose the permutation (order of blocks). The last block is the one started on move m_k. The winner is determined by the parity of m_k.

Fennec wants m_k odd, Snuke wants m_k even.

m_k = T - A_k + 1 = sum A_i - A_k + 1.

Fennec chooses the permutation to make this odd, Snuke chooses to make it even. But they alternate placing blocks? No, the permutation is built over time as moves are made.

This is the key: the game is not about choosing a permutation; it's about the sequential play. The blocks are determined by the sequence of moves.

Let me reconsider the sequential game. The state is: which piles are activated, and the current "time" (move number). The next move: a player chooses to start a new pile (activation) or continue an existing pile (free move).

This is equivalent to the Nim-like game I described. The free moves are like passes that don't change the activation count, but shift whose turn it is.

I think the correct analysis is:

The game value is determined by A_N (the maximum). Specifically, the "free moves" on the largest pile determine the outcome.

Let me try this: sort A ascending. Fennec wins iff A_N > sum_{i=1}^{N-1} A_i + (something).

For N=2: Fennec loses always. Condition: A_2 ≤ A_1 + something. With A_2 = 29, A_1=25, Snuke wins. 
For N=3, sample 1: A=(1,2,9), Fennec wins. A_3=9 > 1+2=3. 
For N=6, sample 3: A=(1,2,2,9,9,25), Snuke wins. A_6=25, sum others=23. 25 > 23. Fennec would win by the "M > sum_others" rule, but Snuke wins. So not that.

Hmm. Let me think about sample 3.

Sample 3: N=6, A=(1,2,2,9,9,25). The 25 is the largest. There are two 9s. 

Maybe the condition involves comparing A_N with A_{N-1} or the second largest.

For sample 3: second largest is 9. 25 vs 9+2+2+1+9 = 23. 25 > 23+1=24? 25>24 yes. But Snuke wins.

Let me try: A_N > sum of others + 1. Sample 2: 29 > 25+1=26 yes, but Snuke wins. So no.

OK so the "M > sum_others" is wrong. Let me think about why sample 2 is Snuke.

For sample 2, N=2: as analyzed, Snuke wins because he moves second and k=2 is even. For N=2, the first player always loses.

For N=3, sample 1, Fennec wins. The large pile (9) gives enough free moves.

I think the answer is: sort A. Fennec wins iff A_N > sum_{i=1}^{N-1} A_i + 1? No, sample 2 contradicts.

Wait, for N=2, the first player loses. So Fennec (first) loses. The condition for N=2 to be a Fennec win would be... never. But by the formula A_2 > A_1 + 1, with A=(25,29), 29>26, Fennec wins. Contradiction.

So the formula is not simply about the max vs sum of others.

Let me reconsider. Maybe the condition is A_N > sum_{i=1}^{N-1} A_i + 1 for N≥3, and Snuke wins for N=2? But that's arbitrary.

Actually, for N=2, the game is trivial: k=2, Snuke wins. For N>2, it depends on the array.

I think the correct condition is: Fennec wins iff 2*A_N > sum A_i + 1, i.e., A_N > (sum - A_N) + 1 = sum of others + 1.

Sample 1: A_N=9, sum others=3. 9 > 4. Fennec. ✓
Sample 2: A_N=29, sum others=25. 29 > 26. Fennec? But Snuke. ✗

Still wrong. Unless the condition is A_N > sum of others + N - 1 or something.

Let me re-examine sample 2 with the theory. For N=2, the first player (Fennec) must activate on move 1. The second player (Snuke) can activate the other pile on move 2, making k=2, and wins. Fennec cannot prevent this. So for N=2, Snuke wins.

But if the formula says Fennec wins when A_N > sum_others + 1, then for N=2 with A=(25,29), it would say Fennec wins, which is wrong.

So the formula must include N somehow. Or my derivation is wrong.

New idea: the game is equivalent to a single pile of size A_N - 1 (the free moves after activating the largest pile) and some other structure.

Actually, I recall now. This problem is "Fennec vs Snuke" from AtCoder. The answer is:

Fennec wins iff 2 * A_N > sum(A_i) + 1? Let me check:
Sample 1: 2*9=18, sum+1=13. 18>13, Fennec. ✓
Sample 2: 2*29=58, sum+1=55. 58>55, Fennec? But Snuke. ✗

Hmm. Let me check the actual answer for this problem.

This is AtCoder ABC 267 F? No. Let me think. The problem statement mentions Fennec and Snuke, which are AtCoder mascots. This is likely ABC 247 F or similar. Actually, I think this is "Fennec vs Snuke" from some contest.

Upon reflection, I believe the answer is:

Sort A. Let S = sum A_i, M = max A_i. Fennec wins iff 2*M > S + 1.

But sample 2 contradicts. Let me double-check sample 2: N=2, A=(25,29). M=29, S=54. 2*29=58, S+1=55. 58>55, so Fennec wins. But the answer is Snuke.

So that formula is wrong. Let me think again.

Wait, maybe the condition is 2*M > S + 1 is for the first player to win in a different game. For this game with N=2, the first player loses.

Let me look at this from a different angle. The game is: the first player wants the last activation on an odd move. 

Total moves if game went to completion: T = S. The game ends at the N-th activation. The N-th activation is at move m_N = T - A_k + 1, where A_k is the size of the last pile activated.

Wait, I think the key is: the last pile to be activated is not necessarily the largest. It depends on play. The players choose the order.

But the total moves is fixed at T. The last move is T. The last pile activated is the one whose block contains move T. Its start is T - A_k + 1.

The winner is the player who moves on T - A_k + 1. The parity of T - A_k + 1 = S - A_k + 1.

Fennec wins iff S - A_k + 1 is odd, where A_k is the size of the last pile.

Fennec chooses the permutation (order of blocks) to control A_k and the parity.

The last pile activated: the one placed last in the permutation. Fennec wants to choose k such that S - A_k + 1 is odd, and Snuke wants it even. But they alternate placing blocks.

Actually, the permutation is built move by move. The last block placed is the last pile activated. The size of that pile determines the winning move parity.

The game: players take turns placing blocks. A block of length A_i can be placed at the end of the current sequence, extending it. The game ends when all blocks are placed; the last block placed is the winning move.

Wait, no. The blocks are placed over time, but they can be placed at any time, not just appended. Hmm, but in the sequential game, a move either starts a new block (activation) or extends the current block (free move). But free moves extend a specific block.

Let me think of it as: the sequence of piles for each move is determined. The blocks are contiguous. The game ends when all blocks are started (N activations). After that, the game continues with free moves until all blocks end? No, the game ends when S is full, i.e., all piles activated. The free moves after that still happen, but they don't change S.

Wait, the game ends as soon as S = {1,...,N}. The move that activates the last pile ends the game immediately. So subsequent free moves don't happen.

So the game ends at the N-th activation. The N-th activation is the start of the last block. Its move number is m_N.

The blocks after m_N (the free moves of the last pile and possibly others if they weren't finished)... no, only the last pile's free moves are after m_N, because all other piles are fully activated and possibly have free moves, but wait.

The constraint: pile i's moves are contiguous. The activations are the starts of these contiguous blocks. The N activations are distinct moves m_1 < m_2 < ... < m_N. The pile with the largest start is the last activated.

The moves after m_N: only moves of the last pile (its free moves). But the game ends at m_N. So the last pile's free moves don't happen.

The moves before m_N: moves 1 to m_N - 1. These are the activations of the other N-1 piles and their free moves. Each pile i (i ≠ last) has its block [m_i, m_i + A_i - 1] contained in [1, m_N - 1] (since m_i < m_N and the block is contiguous, and the block doesn't overlap with the last pile's block which starts at m_N).

So the blocks of the first N-1 piles partition [1, m_N - 1]. Thus m_N - 1 = sum_{i ≠ last} A_i, so m_N = sum_{i ≠ last} A_i + 1.

The last pile is some pile k. m_N = S - A_k + 1.

The winner is Fennec iff m_N is odd, i.e., S - A_k + 1 is odd, i.e., S - A_k is even, i.e., S and A_k have the same parity.

Fennec chooses the last pile (by choosing when to activate the final pile). He wants A_k to have the same parity as S.

But the choice of the last pile is made during play. The last pile is the one activated on the N-th activation. Fennec controls this if it's his turn when only one pile remains unactivated, or he can force it.

Specifically, on any turn, if only one pile is unactivated, the current player can activate it and win (if it's the N-th activation, which it is). So the player who faces "one pile left" wins.

The game reduces to: a game where players take tokens from a pile (or something). Let me think of the free moves as tokens.

Actually, here's a cleaner formulation. Consider the sorted array. The largest pile A_N dominates. The game is equivalent to a game of Nim on the free moves.

I think the answer for this problem is:

Let S = sum A_i, M = max A_i. Fennec wins iff 2*M > S + 1.

But sample 2 fails. Unless I have the samples wrong. Let me re-read.

Sample 2: N=2, A=(25,29). Output: Snuke.

2*29=58, S+1=55, 58>55. So formula says Fennec. Contradiction.

So the formula is not 2*M > S+1.

Another thought: maybe the formula is 2*M > S + N - 1 or 2*M > S + something.

For N=2 to give Snuke: 2*29 > 54 + c implies 58 > 54+c, so c < 4. c=1: 58>55, Fennec. c=2: 58>56, Fennec. c=3: 58>57, Fennec. c=4: 58>58, false, Snuke. So c=4 works for sample 2.

Check sample 1: 2*9=18, S=12, N=3. 18 > 12+c. c=4: 18>16, Fennec. c=5: 18>17, Fennec. c=6: 18>18, false, Snuke. But answer is Fennec. So c<6 for sample 1. c=4 or 5.

Check sample 3: N=6, A=(1,2,2,9,9,25), S=48, M=25. 2*25=50, S+c. 50>48+c. c=1: 50>49, Fennec? But Snuke. So for sample 3, need 50 ≤ 48+c, c≥2. 

So c is not constant. It depends on N or the array.

I think the correct condition is: Fennec wins iff 2*A_N > S + 1 is not the right one. Let me search my memory for this problem.

This is AtCoder Beginner Contest 267 - F? No. Let me think. "Fennec and Snuke" game. I think it's from a recent contest. The problem might be "Fennec vs Snuke" from ABC 297 or similar.

Upon careful thought, I believe the answer is:

Sort A. Fennec wins iff A_N > sum_{i=1}^{N-1} A_i + 1? No, we saw that fails.

Wait, I think I had it backwards. Let me reconsider the sample 1 analysis.

Sample 1: A=(1,9,2) sorted (1,2,9). S=12, M=9, N=3.
sum others = 3. M=9 > 3+1=4. Fennec.

Sample 2: A=(25,29) sorted (25,29). S=54, M=29, N=2.
sum others = 25. M=29 > 25+1=26. Fennec. But Snuke.

So for N=2, the formula gives wrong answer. The issue is that for N=2, the first player loses regardless (since k=2 always).

For N=2, the last pile activated has A_k where k is the second pile activated. The second player (Snuke) activates it, and the pile he activates has some A value. m_N = S - A_k + 1 = 54 - A_k + 1. If A_k=25, m=30, even, Snuke wins. If A_k=29, m=26, even, Snuke wins. So Snuke wins either way for N=2.

For the formula M > sum_others + 1 to give the right answer for N=2, it would need to say Snuke, but it says Fennec when 29>26. So the formula is wrong for N=2.

Unless the game allows the first player to win for N=2 in some cases? But we showed Fennec must activate on move 1, Snuke activates the other on move 2, k=2, Snuke wins. Always.

So for N=2, Snuke always wins. The formula should give Snuke for N=2.

Maybe the formula is: Fennec wins iff 2*M > S + 1 AND N > 2, or 2*M > S + N - 1?

Let me try 2*M > S + N - 1:
Sample 1: 18 > 12+2=14, Fennec. ✓
Sample 2: 58 > 54+1=55, Fennec? But Snuke. ✗

Try 2*M >= S + N:
Sample 1: 18 >= 12+3=15, Fennec. ✓
Sample 2: 58 >= 54+2=56, Fennec. ✗

Hmm.

Let me reconsider whether for N=2, Fennec can ever win. With A=(a,b), a,b≥1. Move 1 Fennec activates one. Move 2 Snuke activates the other, wins. So Fennec never wins for N=2.

So the answer for N=2 is always Snuke. For N>2, it depends.

For N=3, when does Fennec win? Sample 1: yes. Let me think of a case where Snuke wins with N=3. A=(1,1,2)? 
- Fennec move 1: activates. Say pile 3 (A=2). 
- Snuke move 2: can activate pile 1 or 2, or free on pile 3. If activates pile 1, move 3 Fennec activates pile 2, k=3, Fennec wins. If activates pile 2, same. If free on pile 3, move 3 Fennec: if activates pile 1, k=2, move 4 Snuke activates pile 2, k=3, Snuke wins. If free on pile 3, move 4 Snuke must activate (pile 1 has 0 free, pile 2 has 0 free since not activated, pile 3 has 0 free). So Snuke activates pile 1, k=2, move 5 Fennec activates pile 2, k=3, Fennec wins.

So with A=(1,1,2), Fennec wins. Let me try A=(1,1,1). S=3, M=1.
- Fennec move 1: activates. 
- Snuke move 2: activates.
- Fennec move 3: activates last, k=3, Fennec wins.

So for N=3 with A=(1,1,1), Fennec wins. The condition is that with small arrays, Fennec wins.

For N=3, Snuke wins when? Maybe when the largest pile is not large enough. A=(2,2,2)?
- Fennec move 1: activates pile 1. 
- Snuke move 2: can activate or free. If activates pile 2, move 3 Fennec activates pile 3, k=3, Fennec wins. If free on pile 1, move 3 Fennec. If activates pile 2, same as above. If Fennec does free on pile 1, move 4 Snuke. 
- Let's say Fennec move 1 activates pile 1 (0 free). Snuke move 2 activates pile 2 (0 free). Fennec move 3 activates pile 3, k=3, wins.
- Or Snuke move 2 free on pile 1? No free moves. Must activate.
So Fennec wins for A=(2,2,2).

Hmm, when does Snuke win for N=3? A=(1,1,100)?
- Fennec move 1: activates pile 3 (A=100, 99 free). 
- Snuke move 2: if activates pile 1, move 3 Fennec activates pile 2, k=3, Fennec wins. If activates pile 2, same. If free on pile 3, move 3 Fennec. If Fennec activates, k=2, move 4 Snuke activates last, k=3, Snuke wins. If Fennec does free, move 4 Snuke. They alternate free moves on pile 3. 99 free moves. 
- After Fennec's move 1 and Snuke's move 2 (free), 98 free moves remain. They alternate: Snuke moves 4,6,8,... (even after 2); Fennec moves 3,5,7,... (odd).
- After 99 free moves total: moves 2,3,4,...,100. Move 2 Snuke, 3 Fennec, ..., 100 is even so Snuke. 99 free moves: from move 2 to move 100, that's 99 moves. Last free move on move 100 by Snuke. Then move 101 Fennec, but free moves exhausted, must activate pile 1 or 2, k=2, then Snuke on move 102 activates last, k=3, Snuke wins.
- But Snuke might not want to use all free moves. Let's see: the game is, after move 1 (Fennec activates pile 3), it's a game of free moves on pile 3. There are 2 unactivated piles (1 and 2). 
- If a player activates a small pile, they make progress toward the end, but the opponent wins if it's the last one.
- Specifically, if Snuke activates pile 1 on move 2, then Fennec on move 3 must activate pile 2 (last), k=3, Fennec wins. So Snuke shouldn't activate.
- If Snuke does free move on move 2, Fennec on move 3 must decide: activate (bad, leads to Snuke winning) or free. So Fennec does free.
- They continue free moves. The parity: move 1 Fennec, move 2 Snuke (free), move 3 Fennec (free), ..., until free moves exhaust or someone is forced.
- Free moves: 99. They alternate starting with Snuke. After k free moves (k≥1), the next move is: if k is odd, next is Fennec (since Snuke did kth free move? Let me track.
- Move 1: F (activation)
- Move 2: S (free, k=1)
- Move 3: F (free, k=2)
- Move 4: S (free, k=3)
- ...
- Move 2j: S (free, k=2j-1)
- Move 2j+1: F (free, k=2j)
- After 98 free moves (k=98), move 99 is F (free, k=98). Move 100 is S (free, k=99). Free moves done. Move 101 is F, must activate. 
- Move 101: F activates pile 1 or 2. Say pile 1. k=2 activations. Move 102: S activates pile 2, k=3, S wins.
- So Fennec loses if they play free moves all the way. Can Fennec deviate? On move 3, Fennec could activate instead of free. Then k=2, move 4 S activates last, k=3, S wins. So Fennec loses either way.
- So for A=(1,1,100), Snuke wins.

Now, A=(1,1,100): M=100, sum others=2. 100 > 2+1=3. By the "M > sum_others+1" rule, Fennec wins. But Snuke wins. So the rule is wrong, or I have the direction wrong.

Maybe Fennec wins iff M ≤ sum_others + 1? For sample 1: 9 ≤ 4? No, 9>4. But Fennec wins. So no.

For A=(1,1,100): Snuke wins, M=100, sum_others=2. 100 > 3.
For sample 1: Fennec wins, 9 > 4.

Both have M > sum_others+1, but different winners. So it's not just about M vs sum_others.

The difference: in A=(1,1,100), the free moves are 99, and the game lasts. In sample 1 A=(1,2,9), free moves on largest are 8.

The condition might be: Fennec wins iff M ≤ sum_others + 1, but sample 1 contradicts. Or M > sum_others + 1, but A=(1,1,100) contradicts.

Let me compute: for A=(1,1,100), S=102. 2*M=200. S+1=103. 200>103, Fennec by that rule. But Snuke.

I'm confused. Let me re-examine A=(1,1,100).

A=(1,1,100), sorted (1,1,100). 
- Fennec move 1: must activate. Options: pile 1 (A=1), pile 2 (A=1), pile 3 (A=100).
  - If activates pile 1: move 2 Snuke. Snuke can activate pile 2 (k=2), then move 3 Fennec activates pile 3, k=3, Fennec wins. Or Snuke activates pile 3 (A=100, 99 free), then move 3 Fennec. If Fennec activates pile 2, k=3, Fennec wins. If Fennec does free on pile 3, they alternate free moves. 99 free moves. After free moves exhaust, move is... let's see.
    - Move 1: F activates pile 1 (0 free).
    - Move 2: S activates pile 3 (99 free).
    - Move 3: F. If activates pile 2, k=3, F wins. So S wouldn't activate pile 3 on move 2.
  - So if Fennec activates pile 1, Snuke activates pile 2 on move 2, Fennec wins. So Snuke activates pile 3 on move 2.
    - Move 2: S activates pile 3 (99 free).
    - Move 3: F. If activates pile 2, k=3, F wins. So F does free on pile 3.
    - Now 98 free moves. Move 4: S. If activates pile 2, k=3, S wins. If free, continue.
    - They alternate free moves. After 99 free moves total (starting move 3? no, move 2 is activation, free moves start move 3).
    - Free moves available: 99. Used on moves 3,4,5,...,101. That's 99 moves. Move 101 is the 99th free move. 
    - Parity: move 3 is F, move 4 is S, ..., move 101 is F (since 101 is odd, 101=3+98, 98 even, so same parity as 3, F).
    - After move 101, free moves done. Move 102: S. Must activate pile 2, k=3, S wins.
    - So Fennec loses this line.
  - Can Fennec do better? On move 3, instead of free, activate pile 2. Then k=3, Fennec wins! Wait, k=3 means 3 activations done, game ends, Fennec wins. So if Fennec activates pile 2 on move 3, Fennec wins.
  - So the line: F activates pile 1, S activates pile 3, F activates pile 2 on move 3, k=3, F wins.
  - But Snuke wouldn't activate pile 3 on move 2 if it leads to loss. On move 2, Snuke's options: activate pile 2 or pile 3. If pile 2, then F on move 3 activates pile 3, k=3, F wins. If pile 3, then F on move 3 activates pile 2, k=3, F wins. Either way, F wins.
  - So if Fennec activates pile 1 on move 1, Fennec wins!
  
Wait, that means for A=(1,1,100), Fennec wins by activating a small pile first. Let me re-examine.

A=(1,1,100). F move 1: activates pile 1 (A=1, 0 free). S move 2: must activate (no free). Options: pile 2 (A=1) or pile 3 (A=100).
- If S activates pile 2: F move 3 activates pile 3, k=3, F wins.
- If S activates pile 3: F move 3 activates pile 2, k=3, F wins.
So F wins.

What if F activates pile 3 (A=100) on move 1? Then S move 2: if activates pile 1, F move 3 activates pile 2, k=3, F wins. So S would do free on pile 3. Then F move 3: if activates, S wins. If free, continue. Eventually S wins. So F shouldn't activate pile 3.

So F wins for A=(1,1,100) by activating small pile first.

Now, can F always win for N=3? Let me try A=(1,1,1). F move 1 activates any. S move 2 activates. F move 3 activates last, wins.

A=(2,2,2). F move 1 activates pile 1 (1 free). S move 2: can free on pile 1, or activate. If activates pile 2, F move 3 activates pile 3, wins. If free on pile 1, F move 3: if activates pile 2, S move 4 activates pile 3, S wins. If free on pile 1, S move 4: must activate (pile 1 has 0 free now). S activates pile 2, F move 5 activates pile 3, F wins.
- Move 1: F activates pile 1 (1 free).
- Move 2: S does free on pile 1 (0 free left).
- Move 3: F does free? No free left on pile 1. F must activate. Activates pile 2 (1 free). k=2. Move 4: S. If activates pile 3, k=3, S wins. If free on pile 2, move 5 F activates pile 3, k=3, F wins.
- So S on move 4 should activate pile 3 and win. So F loses this line.
- Can F do better on move 3? F could activate pile 2 or pile 3. If pile 3, k=2, S on move 4 activates pile 2, k=3, S wins. If pile 2, S on move 4 can activate pile 3 and win, or free. If S frees, F activates pile 3 and wins. So S activates and wins.
- So if S does free on move 2, F is forced to activate on move 3 (no free moves), and S wins.
- What if S activates on move 2? If S activates pile 2, F activates pile 3 on move 3, wins. If S activates pile 3, F activates pile 2 on move 3, wins. So S activating on move 2 loses.
- Therefore S does free on move 2, and wins.
- So for A=(2,2,2), Snuke wins.

Interesting. So for N=3, A=(1,1,1) F wins, A=(2,2,2) S wins, A=(1,1,100) F wins, sample 1 F wins.

The condition for N=3: when does F win? 
A=(1,1,1): S=3, M=1. F wins.
A=(2,2,2): S=6, M=2. S wins.
A=(1,1,100): S=102, M=100. F wins.
A=(1,2,9) sample 1: S=12, M=9. F wins.

For A=(2,2,2), M=2, sum others=4. M=2 ≤ 4+1=5. For A=(1,1,1), M=1 ≤ 1+1=2. For A=(1,1,100), M=100 > 1+1=2. For sample 1, M=9 > 3+1=4.

So when M is large relative to others, F wins. When M is small, S wins. The threshold might be M > sum_others + 1 or similar.

For A=(2,2,2): M=2, sum_others=4. 2 ≤ 4+1=5. By "M > sum_others+1", F would lose. ✓
For A=(1,1,100): M=100, sum_others=2. 100 > 3. F wins. ✓
For sample 1: 9 > 4. F wins. ✓
For sample 2 (N=2): 29 > 26. Would say F, but S. So for N=2, it's different.

Maybe for N=2, the first player always loses, and for N>2, the condition is M > sum_others + 1.

Let me verify with sample 3: N=6, A=(1,2,2,9,9,25), M=25, sum_others=23. 25 > 24? 25>24 yes. F wins? But S wins. ✗

So sample 3 contradicts. Let me re-examine sample 3.

Sample 3: A=(1,9,2,25,2,9). N=6. Sorted: (1,2,2,9,9,25). M=25, sum_others=23.

If F wins by the rule, but answer is S. So the rule is wrong.

Hmm. Let me think about sample 3. The second largest is 9. There are two 9s.

Maybe the condition involves the top two: M + M2 > sum_rest + 1 or something.

For sample 3: M+M2=25+9=34, sum_rest=14. 34>15, F wins? But S.

Or M > sum_rest + 1 where sum_rest excludes M: 25>24, F wins. But S.

I'm stuck. Let me look for a pattern.

Sample 1: N=3, sorted (1,2,9). F wins. 
Sample 2: N=2, sorted (25,29). S wins.
Sample 3: N=6, sorted (1,2,2,9,9,25). S wins.

For sample 1, the largest is 9, which is > sum of others (3). F wins.
For sample 2, largest 29 > others 25. S wins.
For sample 3, largest 25 > others 23. S wins.

So having M > sum_others doesn't guarantee F win. The difference is N or the distribution.

I think the correct condition is: F wins iff 2*M > S + 1, but only when N is odd or something? Sample 1 N=3 odd, F wins. Sample 2 N=2 even, S wins. Sample 3 N=6 even, S wins. But A=(1,1,1) N=3, S=3, M=1, 2*1=2, S+1=4, 2<4, F wins by "F wins iff 2*M ≤ S+1"? That's the opposite.

Let me try: F wins iff 2*M > S + 1.
Sample 1: 18>13, F. ✓
Sample 2: 58>55,