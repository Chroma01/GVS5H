
## ideation
The game ends when the last untouched index is first chosen. Each index i needs exactly one "claiming" move to enter S; all other moves on i are filler. Total moves until game end = (number of filler moves before the last claim) + N. The player making the N-th claim wins.

Think of it as: players alternately pick piles with remaining tokens; the first pick on a pile claims it. The game ends when all N piles are claimed. Equivalently, the game lasts exactly T moves where T = sum over piles of (moves made on that pile before the final claim happens)... Actually total moves = sum of A_i' consumed, but players can always move, and the game ends at the moment of the Nth distinct claim. The total number of moves M satisfies: M = N + (extra moves on already-claimed piles). Players control extras.

Key reformulation: this is like a game where each pile i has A_i tokens; a move removes a token from a nonempty pile; the player who first removes a token from the last untouched pile wins. Since piles with A_i ≥ 1 always exist until end, the only strategic content is timing of claims vs filler.

Candidate: sort by A_i. The player who claims a pile "uses" it. Known result for this AtCoder problem (ARC/AGC "Fennec vs Snuke" style): answer depends on sorted A. I recall this is ABC/ARC problem where solution: sort A, then simulate: Fennec takes largest? Actually there's a known problem "Fennec vs Snuke" with coloring. This one resembles AGC problem where answer = Fennec iff after sorting, some condition on parity of (A_i - i) or similar.

Let me think small: N=1: Fennec claims index 1 on move 1, wins. Always Fennec.

N=2, A=(1,1): Fennec must claim one pile (move1), Snuke claims other (move2), Snuke wins. A=(2,1): Fennec can claim pile1? Move1 claim pile1 (A1=2→1). Snuke: can move on pile1 (filler) or claim pile2 (loses immediately? claiming pile2 ends game, Snuke would win!). Wait claiming the last pile wins, so Snuke claims pile2 and wins. So Fennec instead: move1 claim pile2 (A=(2,0)). Snuke: only pile1 has tokens; moving on pile1 claims it → Snuke wins. Hmm, so Fennec loses? A=(2,1): any Fennec move claims some pile; then Snuke claims the other and wins (both piles have ≥1 tokens after Fennec's move? If Fennec claims pile2, pile2 becomes 0, pile1=2; Snuke must pick pile1, claims it, wins). So Snuke wins N=2 always? A=(2,2): Fennec claims pile1 (1,2)... wait A1=2→1. Snuke can filler on pile1 (→0), then Fennec must claim pile2 → Fennec wins! So with A=(2,2), Fennec wins. So filler moves matter: parity of total tokens?

Total moves M = N + filler. Filler possible on pile i after claim, up to A_i - 1 times. Players choose. The game is: players alternately either claim an unclaimed pile (with tokens) or filler on a claimed pile. The player making the Nth claim wins. Equivalent to: there are N claims to distribute among turns; between claims, players may insert filler moves, total filler bounded by sum(A_i - 1) over piles claimed before... filler on pile i only after it's claimed, and at most A_i - 1 total on pile i (since each move consumes a token; pile i supports A_i moves total, one of which is the claim).

So total moves M ≤ sum A_i, and M = N + F where F = total filler. The game ends at the Nth claim; remaining tokens are irrelevant. Players' strategies: the player who wants to win wants parity of M favorable: Fennec wins iff M is odd (Fennec makes moves 1,3,5,...). So Fennec wants the Nth claim to occur on an odd move number, Snuke on even.

This is a game of timing: claims are "events"; filler moves are "passes" (limited). Each pile, once claimed, provides up to (A_i - 1) passes total (shared resource, either player can use). Unclaimed piles can't be used for passes.

So state: set of claimed piles, remaining pass-budget per claimed pile. Players choose to pass (if budget available) or claim a new pile.

This is like: at each turn, if any claimed pile has remaining tokens, a player may pass; otherwise must claim. The Nth claim's parity decides.

Think of total pass budget B = sum over claimed piles of (A_i - 1) at moment before final claim: the last claim happens when N-1 piles claimed. Before the final claim, available passes = sum over those N-1 piles of remaining tokens. The player who is forced to claim the last pile loses... no wait, the player who claims the last pile WINS. So players may want to claim it! It's not misère on claims; the final claim is a winning move. So players will try to be the one to make the final claim, using passes to adjust parity.

Simplify: game = players alternate; moves: claim a new pile (there are N claims total) or pass using budget from claimed piles. The player making the last claim wins. Since claiming last wins, players won't avoid claiming per se; it's a race with pass options.

Consider it as: the game ends exactly at move number = N + (passes used before final claim). Passes available before final claim ≤ sum over first N-1 claimed piles of (A_i - 1). Both players can use passes to flip parity.

This is a known AtCoder problem: "Fennec and Snuke" board game — I believe it's from AGC or typical contest; solution: sort A descending? Let me try to derive.

Let f(S, turn) be winner. Too big. Look for invariant: Suppose we sort A. Claim: optimal play involves claiming smallest piles first? Intuition: claiming a pile with large A_i gives opponent more pass budget, which is bad? Passes benefit whoever needs parity fix.

Alternative angle: total moves M = N + F, F = passes used. The game ends when a player chooses to claim the last pile — they will do so only if it makes them win, i.e., if it's their move and claiming wins immediately (it always does!). Wait — claiming the last pile always wins the game for the claimer. So if it's your turn and exactly one pile remains unclaimed, you claim it and win. So the real fight: who faces the position with one pile left on their turn... they win. Equivalently, the player who makes the (N-1)th claim may hand the win to opponent unless they can pass... but passes require claimed piles with tokens.

So: after N-1 claims, if it's opponent's turn, they win by claiming last. So you want to make the (N-1)th claim such that... actually you want to be the one to make the Nth claim. After you make the (N-1)th claim, if you have a pass available (some claimed pile with tokens left), you could pass instead of claiming earlier... Let's think recursively: define position by (unclaimed set U, pass budget vector). Player to move wins if they can force.

Simplify with "pass budget" abstraction: total passes P = sum_{i claimed}(A_i - 1) remaining. Since passes are identical (only count matters for parity? Not exactly—budget per pile, but total count is what matters for move counting; any pass consumes one unit; availability only requires some claimed pile with tokens). Since all passes are equivalent, state = (k = number of unclaimed piles, p = total remaining pass budget). Moves: claim → k decreases by 1, p increases by (A_i - 1) for chosen pile i (choose which pile to claim — matters!). Pass → p decreases by 1 (requires p ≥ 1). Game ends when a player claims with k=1 → that player wins.

So the only choice that matters: when claiming, which pile (its A_i - 1 adds to budget). Players will claim strategically: to manage budget.

Fennec wins iff the final claim (k: 1→0) is made by Fennec.

This is now a clean game. Let's compute small cases to guess pattern.

Let me define piles sorted. Intuition: claiming a big pile gives more passes. Passes let you skip your turn effectively, transferring the move to opponent. With k piles left and budget p, whose turn, determine winner W(k, p, player) — but also which piles remain matters (their sizes). However maybe optimal: always claim smallest remaining? Let's test.

N=2, A=(2,2): Fennec turn, k=2, p=0. Must claim (p=0). Claims pile (A-1=1): k=1, p=1, Snuke turn. Snuke can claim last and win immediately! Wait k=1 means Snuke claims last pile and wins. But earlier I computed Fennec wins for (2,2)! Let me recheck: A=(2,2). Fennec claims pile1: A=(1,2), S={1}. Snuke: if Snuke claims pile2, S={1,2} → Snuke wins! Earlier I said Snuke fillers on pile1 — that's a mistake: Snuke would rather win. So Snuke wins (2,2). Let me redo: any first move claims one pile, opponent claims the other and wins. So N=2: Snuke always wins? A=(1,1): yes Snuke. (2,1): Snuke. (2,2): Snuke. Indeed for N=2, second player always wins because after Fennec's first claim, the other pile still has ≥1 token (A_i ≥ 1 always). So Snuke wins all N=2. Sample 2 (N=2, 25 29) → Snuke. Consistent.

N=3, sample1: (1,9,2) → Fennec. Let's test hypothesis with model. k=3,p=0,Fennec. Fennec claims some pile. Options: claim A=1 (budget+0): k=2,p=0,Snuke. Snuke must claim: claims A=2 (budget+1): k=1,p=1,Fennec. Fennec claims last → Fennec wins! Wait k=1, Fennec's turn, Fennec claims and wins. But Snuke would choose better: Snuke claims A=9 (budget+8): k=1,p=8,Fennec claims last wins anyway. So after Fennec claims the 1, Snuke claims anything, Fennec claims last and wins?? That gives Fennec wins trivially for N=3? But then parity: N odd → Fennec always wins? Check N=1: Fennec wins. N=3: Fennec claims, Snuke claims, Fennec claims last — but Snuke can pass if budget allows to change parity! After Fennec claims pile (say A=1, p=0), Snuke claims A=2 pile → p=1, k=1, Fennec's turn: Fennec could pass (p→0) then Snuke forced to claim last → Snuke wins! Oh right, Fennec will choose to win: Fennec claims last and wins. Fennec won't pass. So Fennec wins. Hmm but Snuke's choice of which pile to claim second affects p but Fennec just claims last immediately and wins regardless. So for N=3, Fennec always wins?? Sample 3: N=6 → Snuke. Sample1 N=3 Fennec. Conjecture: odd N → Fennec, even N → Snuke? But then A values irrelevant — unlikely for a problem with A_i up to 1e9. Let me test N=3 more carefully with passes: could Snuke, instead of claiming second pile, pass? After Fennec's first claim, p = A_claimed - 1. If Fennec claims a pile with A≥2, p≥1, Snuke can pass: then Fennec turn with k=2, p = p-1... Fennec can pass back if p≥1. Passes burn budget. Eventually someone must claim. With k=2 and it's your turn: if you claim, k=1, opponent claims last and wins — bad. So with k=2, players will pass as long as possible; the player unable to pass (p=0) must claim and loses (opponent claims last). So k=2 is a "poisoned" state: the player to move with k=2, p passes: passes alternate; the one facing k=2,p=0 to move loses (must claim, handing win). Actually with k=2, p=0, player to move must claim → other claims last → other wins → player to move loses. With k=2,p≥1: pass → k=2,p-1, opponent to move. So k=2: player to move loses iff p even (p=0 loses; p=1 → opponent faces p=0 loses, so p odd wins). So k=2: current player wins iff p odd.

Back to N=3: Fennec claims pile i, p = A_i - 1, k=2, Snuke to move. Snuke wins iff p odd iff A_i even. Fennec chooses which pile to claim: Fennec wants Snuke to lose → p even → A_i odd. So Fennec wins iff there exists a pile with odd A_i. Sample1: A=(1,9,2): odd piles exist → Fennec. ✓. If all A_i even, N=3 → Snuke? Let's sanity check with A=(2,2,2): Fennec claims pile1 (p=1), Snuke passes (p=0), Fennec must claim pile2 (p=1... wait after claiming pile2, budget adds A2-1=1, p=1, k=1, Snuke claims last wins). Alternatively Fennec at p=0,k=2 must claim; yes Snuke wins. Could Fennec do something else first move? All symmetric. So Snuke wins (2,2,2). So A parity matters! Good, conjecture dead; real structure emerges.

Now general: state (k, p) with choice of which pile to claim adding (A_i - 1) to p. Define game: positions with multiset of remaining pile sizes, pass budget p, player to move. Terminal: a player claiming when k=1 wins immediately.

Let me think recursively: Let the remaining piles be a multiset. Player to move options:
- If k=1: claim → win.
- Pass (p≥1): p-=1.
- Claim pile i: remove i from piles, p += A_i - 1.

Goal: be the one to claim at k=1.

Equivalent normal-play transformation: define "losing position" = player to move loses. Compute Grundy-like? Since only win/lose matters, do recursion on k.

Let me hypothesize that only parity of A_i matters? From N=3 analysis: Fennec wins iff ∃ odd A_i. Check N=2: Fennec wins iff? k=2, p=0, Fennec to move: loses always (p=0 even). So Snuke always, regardless of parity. Hmm so N=2: Fennec never wins. N=1: Fennec always wins (claims immediately).

N=3: Fennec wins iff ∃ odd A_i. N=4? Let's compute. Fennec claims pile i → k=3, p=A_i-1, Snuke to move. Need to solve k=3 positions: player to move (call P) with piles multiset M (|M|=3), budget p. P wants to win. P's moves: pass (p≥1) → (k=3, p-1, opponent); claim j → k=2, p' = p + A_j - 1, opponent to move at k=2. Recall k=2: player to move wins iff p' odd. So P claiming j makes opponent win iff p + A_j - 1 odd. P wants opponent to lose → p + A_j - 1 even → A_j parity = parity of (p+1)... p + A_j - 1 even ⟺ A_j ≡ 1 - p (mod 2) ⟺ A_j odd iff p even. So if there exists pile j with A_j parity = (p even ? odd : even), P can claim it and win (assuming this leads to win — opponent at k=2 with even p' loses, yes since k=2 player to move with even p loses... wait k=2 player to move wins iff p odd; so even p' → opponent loses → P wins). Also P could pass: then opponent faces k=3, p-1 — need to know if that's losing for opponent.

So define W3(M, p) = player to move wins. W3 = true if ∃j: parity(A_j) = (1 if p even else 0) [claim and win], OR (p ≥ 1 AND NOT W3(M, p-1)).

Base: p=0: W3(M,0) = ∃j with A_j odd.

Hmm, this is getting complex but maybe there's a pattern: conjecture W_k(M, p) depends only on parities and count. Let's try to find pattern via "strategy stealing": passes are like a shared pile of p tokens where taking is optional; this resembles the game of "Dawson's"? Not exactly.

Alternative known approach: I now recall this problem! It's from AtCoder Grand Contest? "Fennec and Snuke are playing a board game" — this is ABC 249? No... It's "Ex - Directed Substring"? No. Let me think: it's likely AGC or "typical" — I recall a problem where solution is: sort A, then winner determined by first index where A_i parity differs... Actually I recall ARC111? Hmm.

Let me just solve the abstract game. Observations: only parities of A_i matter for the win/lose? Budget p can be huge (up to 1e9 * 2e5), but maybe W depends on p parity and whether p>0? Let's test: k=2: W = p odd. Depends on parity only. k=3: W3(M, p): claim option gives win if ∃ pile with parity ≠ parity(p)... (A_j odd iff p even) i.e. ∃ pile with parity different from p's parity? A_j parity needed: p even → need odd A_j; p odd → need even A_j. So claim-win available iff M contains a pile whose parity ≠ p parity. Pass option: W3(M,p) true if p≥1 and W3(M,p-1) false.

Let q = p parity, and c = number of odd piles in M (|M|=3). Claim-win condition: (q=0 and c≥1) or (q=1 and c≤2).

Pass recursion: W(p) = claim_win(q) OR (p≥1 AND NOT W(p-1)). Note claim_win depends only on q.

Case c≥1 (some odd pile): 
- p=0: claim_win (q=0, c≥1) = true. W=true.
- p=1: claim_win: q=1, need even pile: c≤2? If c≤2, true. If c=3 (all odd): claim_win false; pass: NOT W(0)=NOT true=false. So W(1)=false for c=3! Interesting.
- p=2, c=3: claim_win: q=0, c≥1 true → W=true.
- p=3, c=3: claim_win false; pass: NOT W(2) = false. W=false.
So c=3: W = (p even). c≤2 (and c≥... let's do c=0): all even.
- p=0: claim_win: q=0 need odd pile: none → false. No pass. W=false.
- p=1: claim_win: q=1 need even pile: yes → true.
- p=2: claim_win q=0 need odd: no. pass: NOT W(1)=false. W=false.
So c=0: W = p odd.
c=1 or 2:
- p=0: true (odd pile exists).
- p=1: claim_win: need even pile: c≤2 yes → true.
- Inductively W(p)=true for all p? p=2: claim_win q=0 need odd: c≥1 yes → true. So W=true ∀p when 1≤c≤2.

So k=3 summary: W = [c=0: p odd] [c=3: p even] [c∈{1,2}: always win].

Interesting! So for k=3, if both parities present, player to move always wins. If all same parity, W = (p parity ≠ pile parity)... c=0 (even piles): W = p odd. c=3 (odd piles): W = p even. So W = (p parity != pile parity)? c=0: piles even, W=p odd → p parity ≠ pile parity (p odd vs even piles) yes. c=3: W = p even, piles odd → p even ≠ odd yes. So uniform parity: W = (p%2 != pile_parity). Mixed: always win.

Now k=2 with this lens: piles M, |M|=2, but wait at k=2 the claim also adds budget. Let me redo k=2 generally: player to move, piles {a,b}, budget p. Moves: pass (p≥1) → (k=2, p-1, opp). Claim a → k=1, p' = p + a - 1, opponent to move at k=1: opponent claims last and WINS immediately regardless of p'! Wait — at k=1, player to move just claims and wins. So claiming at k=2 hands the win to opponent. So at k=2, claiming always loses (opponent claims last). So the only sensible moves are passes; when p=0, must claim and lose. So W2 = (p odd). Matches earlier. Good — so at k=2, pile parities irrelevant; claiming is always losing; it's pure pass-war.

Hold on, that contradicts my k=3 analysis where I had "claim j → k=2, opponent at k=2 wins iff p' odd". Yes consistent: at k=2 the player to move wins iff p odd (they can pass-parity-force the other to claim first). Good.

Now general k: define W_k(M, p). Claiming j leads to W_{k-1}(M\{j}, p + A_j - 1) for opponent. Passing leads to W_k(M, p-1) for opponent. Player wins if ∃ move making opponent lose.

Terminal: k=1: W_1 = true always (claim and win). Actually also could pass but claiming wins.

We need W_N(A, 0) for Fennec.

The structure: conjecture W_k(M, p) depends only on (k, multiset of parities of M, parity of p, and maybe whether p=0 vs p>0?). Let's test k=3 results: depended on c (count of odd) and p parity only. k=2: p parity only. Let's try to inductively hypothesize: W_k(M,p) depends only on (c = #odd piles, k, p mod 2). Let me attempt induction.

Define f(k, c, q) where q = p mod 2, assuming sufficient p? Problem: pass requires p≥1; for large p fine, but p=0 vs p=1 both... p parity plus p=0 edge. Since A_i up to 1e9, p can be large, but early game p=0. Hmm, but note: if W depends only on parity of p for p in some range, recursion W(p) = g(q) OR (p≥1 AND NOT W(p-1)) can create period-2 patterns stabilized. Let's just attempt to compute f(k,c,q) for "p large enough" and handle p=0 specially? Actually initial p=0 exactly. But after claims p grows.

Alternative: think about it differently. Known technique for such "pass budget" games: the total game length parity is what matters, and players' strategies revolve around claiming order. Let me think about optimal play as ordering: Since passes only depend on total budget, and claiming adds A_j - 1 to budget, the game is: players alternately claim piles (order π_1, ..., π_N interleaved with passes). Total moves = N + total passes used. Passes used ≤ sum_{t<N} (A_{π_t} - 1) (budget from all but last claimed; last pile's budget irrelevant). Players choose passes to force the final claim on their turn.

Hmm, let me think about the endgame: suppose all piles claimed except last, budget p_remaining. Player to move claims and wins. So the fight is about who moves when k=1. Before that, at k=2, player to move wants p odd (to win the pass war). At k=3, players choose claims to set up.

Let me just try to inductively compute f(k, c, q) assuming p sufficiently large (≥ some bound like k) so pass always available, and separately handle small p. Actually maybe there's a cleaner global strategy argument.

Alternative known result: I strongly suspect this is AtCoder AGC ??? problem "Fennec vs Snuke" — actually I think this is from "AtCoder Regular Contest 123"? Let me recall... There's a known problem "Snuke and Fennec playing with piles, first to color all" — hmm.

Let me try to just compute f via recursion symbolically. Assume p ≥ 1 always available when needed (large p regime), find f(k,c,q) for q∈{0,1}, 0≤c≤k.

Moves from (k,c,q):
- Pass: → opponent (k, c, 1-q) [large p].
- Claim odd pile (c≥1): c→c-1, p adds A-1 where A odd → A-1 even → q unchanged. → opponent (k-1, c-1, q).
- Claim even pile (c≤k-1): A-1 odd → q flips. → opponent (k-1, c, 1-q).

Base: k=1: f(1, c, q) = true (claim and win). Wait but at k=1, c∈{0,1}; claiming wins regardless. f(1,·,·)=W.

Hmm wait, but claiming the last pile wins immediately — yes f(1,c,q)=true.

But careful: at k=2, this large-p regime formula: f(2,c,q): pass → opp (2,c,1-q); claim odd → opp f(1,·,q)=true (bad, gives opponent win); claim even → opp true (bad). So f(2,c,q) = NOT f(2,c,1-q) (from pass) → f(2,c,0) = NOT f(2,c,1), f(2,c,1) = NOT f(2,c,0). Underdetermined! Because pass leads to pass-back loop; the recursion is on p decreasing, so large-p regime needs base at p=0. The parity recursion: W(p) = moves... with pass: W(p) = NOT W(p-1) if no winning claim. So W alternates, and base W(0) determines all. So we need W at p=0 as base and parity determines rest (when claims don't interfere). But claims add to p, changing things. Ugh, but note: claim moves change k, and the added budget's parity is what matters (A_j - 1 parity), plus the magnitude could matter for availability? Once p ≥ 1, pass available; the exact magnitude only matters for long pass wars at fixed k. Since each pass decreases p by 1 and claims increase k... The pass war at level k lasts at most p moves before someone claims. So magnitude matters when p is small relative to... hmm, actually in the pass war, players may also choose to claim mid-war. The recursion W_k(M,p) with pass: W_k(M,p) = claim_options(p) OR (p≥1 AND NOT W_k(M,p-1)). If claim_options depends only on parities (via recursion), then W_k(M,p) for p≥1: W(p) = C(q) OR NOT W(p-1), where C(q) = claim winning availability given parity q. Then: if C(q)=true, W=true. The pattern: W(0)=C(0). W(1)=C(1) OR NOT W(0). W(2)=C(0) OR NOT W(1). Etc. So W(p) depends only on q and C(0),C(1): W(0)=C0; W(1)=C1 OR ¬C0; W(2)=C0 OR ¬W(1)=C0 OR (¬C1 ∧ C0)=C0; so W(even p)=C0, W(odd p)=C1 OR ¬C0. Great — depends only on parity! So by induction, W_k(M,p) depends only on (k, parity multiset c, q=p%2). 

So define f(k, c, q) ∈ {W, L} = player to move wins.

Recursion:
f(1, c, q) = W (c ∈{0,1}).
For k ≥ 2:
- Claim odd (if c ≥ 1): leads to opponent f(k-1, c-1, q) [A odd → A-1 even → q unchanged]. Winning if f(k-1,c-1,q) = L.
- Claim even (if c ≤ k-1): leads to opponent f(k-1, c, 1-q) [A-1 odd flips]. Winning if f(k-1,c,1-q) = L.
- C(q) = above disjunction.
- f(k,c,0) = C(0).
- f(k,c,1) = C(1) OR (f(k,c,0) = L)... from W(odd) = C1 OR ¬C0. But careful: C depends on q, and C(1) uses f(k-1,...) which are fixed. So compute C0, C1 then f0=C0, f1 = C1 OR NOT f0.

Wait but also need p≥1 for pass at odd p — odd p ≥ 1 yes. And the derivation W(odd)=C1 OR ¬W(even)... we derived W(2)=C0 meaning W(even)=C0 for all even p including 0. And W(odd)=C1 OR ¬C0. But hold on: W(1) = C(1) OR NOT W(0) = C1 OR ¬C0. W(3) = C1 OR NOT W(2) = C1 OR ¬C0. Same. Good, consistent. So f depends only on (k,c,q). 

But wait — is the claim option's effect on q only parity? Claim adds A_j - 1 to p. Yes parity of A_j - 1 = opposite parity of A_j. And the new p' = p + A_j - 1; opponent's position f(k-1, ·, q') with q' = q + (A_j-1) mod 2. By induction f(k-1) depends only on parity. 

Also need: does f(k-1) apply when the budget p' might be... p' parity determines it fully per induction. But induction hypothesis: W_{k-1}(M', p) depends only on (c', q). Base k=1 trivially true (always W). The derivation of W(even)=C0, W(odd)=C1∨¬C0 used only parity dependence of C — but C(q) at level k uses f(k-1) values which by induction are parity-only. And pass availability: at p=0 no pass, formula W(0)=C0 correct. At odd p≥1 pass available. Good. Also one more subtlety: at k≥2, is claiming ever mandatory... no, if p≥1 can pass. And when k=1, player claims and wins — but what if p large, could they pass? They'd rather win. f(1)=W fine.

Hmm wait, one more subtlety at k=1: f(1,c,q)=W means the player to move wins by claiming. Yes.

So compute f(N, c0, 0) where c0 = number of odd A_i, initial p=0 → q=0. O(N) to count odds, then DP over k=1..N, c=0..k, q∈{0,1}: O(N^2) states — too many for N=2e5! Need closed form.

Let's compute the DP pattern. Let me denote states (k,c): pair (f0,f1).

Base k=1: c=0: (W,W); c=1: (W,W).

k=2:
- c=0: claim odd: no. claim even (c≤1 yes): opp f(1,0,1-q). f(1,0,·)=W → not winning. C0=L, C1=L. f0=C0=L. f1=C1 OR ¬f0 = L OR T = W. So (L,W). Matches W2 = p odd. ✓
- c=1: claim odd: opp f(1,0,q)=W no. claim even: opp f(1,1,1-q)=W no. C0=C1=L. f0=L, f1=W. (L,W).
- c=2: claim odd: opp f(1,1,q)=W. claim even: none. C=L. (L,W).
So k=2 all c: (L,W). ✓ (pile parities irrelevant at k=2, matches).

k=3: use f(2,c,q): f(2,c,0)=L, f(2,c,1)=W for all c.
- c=0: claim even: opp f(2,0,1-q): q=0→f(2,0,1)=W; q=1→f(2,0,0)=L → C1 winning! C0: opp W → no. C0=L, C1=W. f0=L, f1=C1∨¬f0=W. (L,W). Matches c=0: W=p odd ✓.
- c=1: claim odd: opp f(2,0,q): q=0→L → C0 winning! So C0=W. f0=W. f1 = C1 ∨ ¬f0 = C1. C1: claim odd: opp f(2,0,1)=W no; claim even: opp f(2,1,0)=L → winning! C1=W. f1=W. (W,W) ✓ matches.
- c=2: claim odd: opp f(2,1,q): q=0 → L → C0=W. f0=W. C1: claim odd opp f(2,1,1)=W; claim even opp f(2,2,0)=L → W. f1=W. (W,W) ✓.
- c=3: claim odd: opp f(2,2,q): q=0→L → C0=W?? But earlier we found c=3: W = p even, i.e., f0=W, f1=L. Let me recheck: C0 = claim odd → opp f(2,2,0)=L → winning → C0=W → f0=W ✓. f1 = C1 OR ¬f0 = C1 OR false = C1. C1: claim odd → opp f(2,2,1)=W → not winning. No even piles. C1=L. f1=L. (W,L) ✓ matches.

Great, DP works. Now find pattern. Let me tabulate (f0,f1) for k=1..: 

k=1: c0:(W,W) c1:(W,W)
k=2: all (L,W)
k=3: c0:(L,W) c1:(W,W) c2:(W,W) c3:(W,L)
k=4: compute. Need f(3,c,q):
c0: f0=L,f1=W. c1:(W,W). c2:(W,W). c3:(W,L).
k=4,c=0: only even claims: opp f(3,0,1-q). C0: opp f(3,0,1)=W → no. C1: opp f(3,0,0)=L → yes. C0=L,C1=W. f0=L, f1=W∨T=W. (L,W).
k=4,c=1: claim odd: opp f(3,0,q): q0→L → C0=W. f0=W. C1: claim odd opp f(3,0,1)=W no; claim even opp f(3,1,0)=W no → C1=L. f1 = L ∨ ¬W = L. (W,L)!
k=4,c=2: claim odd: opp f(3,1,q): both W → no. claim even: opp f(3,2,1-q): f(3,2,·)=W → no. C0=C1=L. f0=L, f1 = L ∨ ¬L = W. (L,W).
k=4,c=3: claim odd: opp f(3,2,q)=W no. claim even: opp f(3,3,1-q): q0→f(3,3,1)=L → C0=W. f0=W. C1: claim odd opp f(3,2,1)=W; claim even opp f(3,3,0)=W → L. f1= L∨¬W = L. (W,L).
k=4,c=4: claim odd: opp f(3,3,q): q0→W, no. C0=L. C1: opp f(3,3,1)=L → W. f0=L, f1= W∨T=W. (L,W).

k=4: c0:(L,W) c1:(W,L) c2:(L,W) c3:(W,L) c4:(L,W).

Interesting! k=4: f0 = W iff c odd; f1 = W iff c even.

k=3: f0: c0 L, c1 W, c2 W, c3 W → f0 = W iff c≥1. f1: c0 W,c1 W,c2 W,c3 L → f1 = W iff c≤2.

Hmm k=3 doesn't follow k=4's pattern. Let me compute k=5.
f(4,c,q): c0:(L,W) c1:(W,L) c2:(L,W) c3:(W,L) c4:(L,W).

k=5,c=0: even claim: opp f(4,0,1-q). C0: opp f(4,0,1)=W no. C1: opp f(4,0,0)=L yes. f0=L, f1=W. (L,W).
k=5,c=1: claim odd: opp f(4,0,q): q0→L → C0=W. f0=W. C1: claim odd opp f(4,0,1)=W no; claim even opp f(4,1,0)=W no → C1=L. f1 = L∨¬W=L. (W,L).
k=5,c=2: claim odd: opp f(4,1,q): q0→W no. C0: claim even opp f(4,2,1)=W no. C0=L. C1: claim odd opp f(4,1,1)=L → W. f0=L, f1=W∨T=W. (L,W).
k=5,c=3: claim odd: opp f(4,2,q): q0→L → C0=W. f0=W. C1: claim odd opp f(4,2,1)=W; claim even opp f(4,3,0)=W → L. f1=L∨¬W=L. (W,L).
k=5,c=4: claim odd: opp f(4,3,q): q0→W no; even: opp f(4,4,1)=W no. C0=L. C1: claim odd opp f(4,3,1)=L → W. f0=L,f1=W. (L,W).
k=5,c=5: claim odd: opp f(4,4,q): q0→L → C0=W. f0=W. C1: opp f(4,4,1)=W → L. f1=L∨¬W = L. (W,L).

k=5: c0:(L,W) c1:(W,L) c2:(L,W) c3:(W,L) c4:(L,W) c5:(W,L).
So k=5: f0 = W iff c odd; f1 = W iff c even. Same as k=4!

k=4 was same pattern. Let me double check k=4 c2: (L,W): f0=L (c even), f1=W (c even) ✓ pattern f0=W iff c odd, f1=W iff c even.

So conjecture: for k ≥ 4: f(k,c,0) = W iff c odd; f(k,c,1) = W iff c even. Let me verify induction step generally.

Assume for k-1 (≥4): f(k-1,c,0)=W iff c odd; f(k-1,c,1)=W iff c even.

At level k, state c:
C0 (q=0): 
- claim odd (c≥1): opp f(k-1,c-1,0)=W iff (c-1) odd iff c even. So winning iff c even (and c≥1).
- claim even (c≤k-1): opp f(k-1,c,1)=W iff c even. Winning iff c odd (and c≤k-1).
So C0 = W iff [c even and c≥1] or [c odd and c≤k-1] = W iff (c even, c≥1) or (c odd, c≤k-1). For 1≤c≤k-1: C0=W always?? c even≥1 → yes; c odd ≤k-1 → yes. So for 1≤c≤k-1, C0=W. For c=0: only even-claim term: c odd? no → C0=L. For c=k: only odd-claim: c even and ≥1 → C0=W iff k even.

Hmm that contradicts the pattern (expected f0 = W iff c odd). But wait — f0 = C0, and pattern said f0 = W iff c odd. Contradiction for 1≤c≤k-1! Let me recheck with k=5,c=1: C0: claim odd → opp f(4,0,0)=L → winning → C0=W. Pattern f0=W iff c odd: c=1 odd → W ✓. c=2: claim odd → opp f(4,1,0)=W (c-1=1 odd → W) → not winning. claim even → opp f(4,2,1): f1 at c=2 = W (c even) → not winning. C0=L ✓ (c even → L). 

But my general derivation above: claim odd winning iff c even — for c=2: c even → claim odd should be winning? opp f(k-1, c-1, 0) = f(4,1,0) = W iff (c-1)=1 odd → W. So opp wins → not winning for us. I made an error: winning means opp LOSES. Claim odd is winning move iff f(k-1,c-1,0) = L iff (c-1) even iff c odd. Let me redo:

C0:
- claim odd (c≥1): winning iff f(k-1,c-1,0)=L iff (c-1) even iff c odd.
- claim even (c≤k-1): winning iff f(k-1,c,1)=L iff c odd.
So C0 = W iff c odd (given the move exists; if c odd then c≥1 so odd-claim exists). C0 = W iff c odd. ✓

C1 (q=1):
- claim odd (c≥1): opp f(k-1,c-1,1)=L iff (c-1) odd iff c even. Winning iff c even (c≥1).
- claim even (c≤k-1): opp f(k-1,c,0)=L iff c even. Winning iff c even (c≤k-1).
C1 = W iff c even and (c≥1 or c≤k-1) → c even and (if c=0 need even-claim: c≤k-1 yes for k≥1) → c=0: even-claim exists (c≤k-1), winning iff c even → yes W. c=k even: odd-claim exists (c≥1) → W. So C1 = W iff c even. ✓

Then f0 = C0 = (c odd). f1 = C1 OR NOT f0 = (c even) OR (c even) = (c even). ✓ Pattern holds for k≥4 given k-1≥4. Base k=4 verified. But wait, the induction for f1: f1 = C1 OR ¬f0 = (c even) ∨ (c even) = c even. ✓.

So for k ≥ 4: f(k,c,0) = W ⟺ c odd; f(k,c,1) = W ⟺ c even.

Now initial position: k=N, c = #odd A_i, p=0 (q=0). Fennec wins iff f(N, c, 0) = W.

Cases:
- N=1: f=W always → Fennec.
- N=2: f0=L always → Snuke.
- N=3: f0 = W iff c≥1 (i.e., at least one odd A_i). 
- N≥4: Fennec iff c odd.

Check samples: Sample1: N=3, A=(1,9,2): c=2 ≥1 → Fennec ✓. Sample2: N=2 → Snuke ✓. Sample3: N=6, A=(1,9,2,25,2,9): odds: 1,9,25,9 → c=4 → even → Snuke ✓. 

Wait, but I should double check the k=3 case and whether N=3 with c=0 gives Snuke: A all even, e.g., (2,2,2) → earlier analysis Snuke ✓.

Also double-check k=4 pattern with a brute-force small example mentally? Let's test N=4, A=(1,1,1,1): c=4 even → Snuke predicted. Simulate: Fennec must claim (p=0) → claims pile, p=0 (A-1=0), k=3, Snuke. Snuke claims (p=0), k=2, Fennec, p=0. Fennec must claim → k=1, Snuke claims last wins. Yes Snuke. ✓. A=(1,1,1,2): c=3 odd → Fennec predicted. Fennec claims the 2 (p=1), k=3, Snuke, piles (1,1,1), p=1. Snuke: pass → p=0, Fennec k=3: claims (p=0), k=2 Snuke p=0: must claim, k=1 Fennec claims wins. Snuke instead claims at k=3: claims a 1 (p stays... A-1=0, p=1), k=2, Fennec p=1: Fennec passes (p=0), Snuke k=2 must claim → k=1 Fennec wins. So Fennec wins ✓.

Edge: N=3, c≥1 → Fennec; c=0 → Snuke. Note for N≥4 even c → Snuke, odd c → Fennec. For N=2 always Snuke (c even→consistent with "c odd→Fennec"? c odd for N=2: f0=L still. So N=2 special). N=1: Fennec (c could be 0 with A_1 even — still Fennec since claims immediately). N=3: different rule (c≥1).

Hmm wait, let me double-check N=3, c=2 case via the DP: (W,W) yes Fennec. And also verify the DP base k=1 f(1,0,q)=W: pile even, player claims it (A≥1, claim → S full → wins). Yes.

But wait — I should double check the claim that f(k,c,q) is well-defined, i.e., independent of the actual values beyond parity, including the magnitude of p. We proved W(even p)=C0, W(odd p)=C1∨¬C0 given C depends only on q. C depends on f(k-1) at parities — by induction fine. But one more subtlety: when claiming, p' = p + A_j - 1. The parity q' = q ⊕ (A_j - 1)%2. Fine. But is f(k-1, ...) applicable — the opponent's budget is p', and we claim f(k-1) depends only on q'. Yes by induction. Also the base case k=1: f(1,c,q)=W regardless of p — yes since claim wins immediately.

One more check: the pass move requires p ≥ 1. In W(odd) formula, odd p ≥ 1 ✓. In W(even)=C0: for p≥2 even, W(p) = C0 OR ¬W(p-1) = C0 ∨ ¬(C1 ∨ ¬C0) = C0 ∨ (¬C1 ∧ C0) = C0. ✓. So f0=C0 for all even p. Good.

Also need to double check the derivation W(1) = C1 ∨ ¬W(0): W(1) = C(1) OR (pass → opp at W(0)) = C1 ∨ ¬f0. ✓.

So solution:
- c = count of odd A_i.
- If N == 1 → Fennec.
- elif N == 2 → Snuke.
- elif N == 3 → Fennec if c ≥ 1 else Snuke.
- else (N ≥ 4) → Fennec if c odd else Snuke.

Wait, N=3 rule: c≥1 → Fennec. Can we unify? N=3: f0 = W iff c≥1. Hmm interesting. Let me re-verify k=3 c=2 (W) via simulation: A=(1,1,2)? c=2. Fennec claims 2 (p=1), k=3? No wait N=3, k=3 initially. Fennec claims the pile A=2 → p=1, k=2, Snuke to move, piles (1,1). k=2: player to move wins iff p odd → p=1 → Snuke wins?! That contradicts f(3,2,0)=W. Let me recheck: Fennec should claim an odd pile instead: claim A=1 → p=0, k=2, Snuke, piles (1,2), p=0: Snuke must claim (k=2, p=0 → loses): claims one, Fennec claims last → Fennec wins ✓. Good, Fennec chooses odd pile. And in the DP, claim odd at (3,2,q=0): opp f(2,1,0)=L ✓ winning. Good.

Now double-check k=3, c=1, e.g., A=(1,2,2): Fennec claims the 1 → p=0, k=2, Snuke piles (2,2) p=0 → Snuke must claim → Fennec claims last wins ✓.

N=3, c=3, A=(1,1,1): Fennec claims → p=0,k=2,Snuke p=0 must claim → Fennec claims last wins ✓ (c=3≥1 → Fennec ✓).

N=3, c=0, A=(2,2,2): shown Snuke ✓.

Now N≥4 rule: c odd → Fennec. Let me sanity check N=4, A=(2,2,2,2) (c=0 → Snuke): Fennec claims (p=1), k=3, Snuke, c=0 (all even remaining), p=1 → f(3,0,1)=W → Snuke wins. Snuke's strategy: at k=3,c=0,q=1: winning move: claim even → opp f(2,0,0)=L. Snuke claims a 2 → p = 1+1=2, k=2, Fennec, p=2 even → Fennec loses: Fennec passes (p=1), Snuke passes (p=0), Fennec must claim → Snuke claims last. ✓.

Everything consistent. Also verify sample3 with rule: N=6≥4, c=4 even → Snuke ✓.

Now, is the N=3 special case actually right per DP, or did I miscompute k=3 c=1 f0? f(3,1,0): C0: claim odd → opp f(2,0,0)=L → winning → W ✓.

Let me also double check k=4 base more carefully since induction starts there; I computed using k=3 values which are exact (not pattern). k=4,c=1: (W,L). Let me re-verify f(4,1,0): C0: claim odd → opp f(3,0,0). f(3,0,0)=L (c=0: (L,W)) → winning → C0=W → f0=W ✓ (c odd → W ✓ pattern). f(4,1,1): C1: claim odd → opp f(3,0,1)=W → no; claim even → opp f(3,1,0)=W → no. C1=L. f1 = C1 ∨ ¬f0 = L ∨ L = L ✓ (c odd → f1=L ✓ pattern c even? c=1 odd → f1 should be L ✓).

Great. Also verify k=4,c=3 f0: claim odd → opp f(3,2,0)=W no; claim even → opp f(3,3,1)=L → winning → W ✓ (c odd). f1: C1: claim odd → opp f(3,2,1)=W; claim even → opp f(3,3,0)=W → L; f1 = L ∨ ¬W = L ✓ (c odd → L ✓).

Induction solid for k≥4.

Hmm, but wait: I should double-check the k=3 values once more via direct game reasoning for c=3, p=0 (A all odd, e.g., (1,1,1)): Fennec claims (p=0 since A-1=0), k=2, Snuke p=0 → Snuke loses → Fennec ✓ (f0=W ✓). c=3,p odd e.g. A=(3,3,3) after... not needed.

Also N=2 with c odd, e.g., A=(1,1): Snuke ✓ (Fennec claims, Snuke claims last). A=(3,1): Fennec claims 3→p=2,k=1?? No wait N=2: Fennec claims pile1 (A=3→2), k=1, Snuke claims pile2 and wins. Fennec claims pile2 first: p=0, k=1, Snuke claims pile1 wins. Snuke ✓.

So final rules:
- N=1: Fennec
- N=2: Snuke
- N=3: Fennec iff at least one odd A_i
- N≥4: Fennec iff (#odd A_i) is odd

Hmm, wait. Let me reconsider whether N=3 rule could be expressed as "c odd or ..." c≥1 means c∈{1,2,3}. c=2 (even) → Fennec. So genuinely different.

Let me also double check N=4 c=2 → Snuke (pattern: c even → f0=L). Example A=(1,1,2,2): Fennec's options: claim odd (A=1): p=0, k=3, Snuke, remaining c=1 (one odd among (1,2,2)), p=0: f(3,1,0)=W → Snuke wins. Claim even (A=2): p=1, k=3, Snuke, c=2, f(3,2,1)=W → Snuke wins. So Snuke ✓.

Let me brute-force-verify a couple more with actual token counts to ensure parity-only reduction is right, e.g., N=4, A=(1,1,1,1) c=4 → Snuke (simulated above ✓). N=5, A all ones: c=5 odd → Fennec. Simulate: all A=1, no passes ever (A-1=0). Players must claim each turn; claims: F,S,F,S,F — 5th claim by Fennec → Fennec ✓. N=5 all twos: c=0 → Snuke. A=(2,2,2,2,2): Fennec claims (p=1), k=4, Snuke c=0 p=1: f(4,0,1)=W (c even → f1=W) → Snuke winning. Snuke move: claim even → opp f(3,0,0)=L: Snuke claims (p=1+1=2), k=3, Fennec c=0 p=2: f(3,0,0)=L. Fennec options: claim even → p=3, k=2, Snuke p=3 odd → Snuke wins; pass → p=1, Snuke k=3 c=0 p=1: f(3,0,1)=W → Snuke. So Snuke wins ✓.

Now also confirm the problem statement's note "players can always make a move until winner determined" — consistent since unclaimed piles have ≥1 token.

Implementation: read N, list A, count odd. Apply rules. O(N). 

Actually wait, I want to be extra careful about the k=3 case c≥1 → Fennec, and whether N=3, c=0 truly Snuke even with large even A like (10, 8, 6). Fennec claims some pile, say A=10 → p=9, k=2, Snuke p=9 odd → Snuke wins pass war: yes k=2 player to move with odd p wins. Any Fennec claim gives p = A_i - 1 odd → Snuke wins. ✓ Snuke.

And N=3 c=1 with the odd pile being A=1 vs large odd — Fennec claims odd pile → p = A_odd - 1 even, k=2, Snuke with even p loses. ✓ Fennec regardless of magnitude. 

One more: N≥4, the rule only uses parity of c. Let me test N=4, c=1, e.g., A=(1,2,2,2): predicted Fennec. Fennec claims the 1: p=0, k=3, Snuke, remaining c=0, p=0: f(3,0,0)=L → Snuke loses → Fennec wins ✓. Snuke at (3, {2,2,2}, p=0): must claim (p=0): claims a 2 → p=1, k=2, Fennec p=1 odd → Fennec wins pass war: Fennec passes (p=0), Snuke must claim, Fennec claims last. ✓.

Test N=4, c=3, A=(1,1,1,2): predicted Fennec (c odd). Fennec claims even pile (the 2): p=1, k=3, Snuke, c=3, p=1: f(3,3,1)=L → Snuke loses ✓. Check Snuke at (3,{1,1,1},p=1): options: claim odd → p=1, k=2, Fennec p=1 odd wins. Pass → p=0, Fennec (3,c=3,p=0): f(3,3,0)=W → Fennec. So Snuke loses ✓.

Great, confident in the solution.

Actually, let me reconsider whether I've correctly identified that at k=1 the player to move always wins. At k=1, one unclaimed pile remains with ≥1 token. Player claims it → S becomes full → player wins. Yes.

Also the very first move: p=0, k=N. If N=1, Fennec claims and wins ✓.

Now write the code:

def solve():
    import sys
    input = sys.stdin.readline
    N = int(input())
    A = list(map(int, input().split()))
    c = sum(1 for a in A if a % 2 == 1)
    if N == 1:
        win = True
    elif N == 2:
        win = False
    elif N == 3:
        win = c >= 1
    else:
        win = (c % 2 == 1)
    print("Fennec" if win else "Snuke")

Hmm, wait. Let me reconsider N=3 once more. Actually, let me re-derive k=3, c=2, f0 via the general k≥4-style logic to see why k=3 differs: at k=3, C0 uses f(2, ·, ·): f(2,c,0)=L for all c, f(2,c,1)=W for all c. C0: claim odd (c≥1): opp f(2,c-1,0)=L → winning (if c≥1). claim even (c≤2): opp f(2,c,1)=W → no. So C0 = (c≥1). f0 = c≥1 ✓. f1 = C1 ∨ ¬f0: C1: claim odd: opp f(2,c-1,1)=W no; claim even: opp f(2,c,0)=L → winning if c≤2. C1=(c≤2). f1 = (c≤2) ∨ (c=0) = (c≤2). So k=3: f0 = c≥1, f1 = c≤2 ✓ matches earlier table.

Everything checks. But let me also sanity-check the induction base k=4 doesn't need k=3 to satisfy any pattern — correct, I computed k=4 directly from k=3 exact values. ✓.

Also, what about N≥4 but with c odd — Fennec; c even — Snuke. Note N=4, c=0 → Snuke; N=4, c=4 → Snuke (simulated (1,1,1,1) ✓).

Edge: N=2e5, A_i=1e9 — fine, just parity.

Let me also verify sample 1 again: N=3, A=(1,9,2), c=2 ≥1 → Fennec ✓.

I'm fairly confident. But let me reconsider the problem once more: "Choose an index i such that 1 ≤ A_i. Subtract 1. If i ∉ S, add i to S. If S = {1..N}, game ends, player who performed last operation wins." Yes matches model.

One more consideration: passes require a claimed pile with remaining tokens — in my model p = sum of remaining tokens over claimed piles, and a pass decrements p by 1. But is any pass always available when p≥1? Yes: p≥1 means some claimed pile has a token; pick it (it's in S already, so S unchanged). ✓. And claiming pile j: requires A_j ≥ 1 — unclaimed piles always have A_j ≥ 1 (untouched). ✓. After claim, p increases by A_j - 1 (remaining tokens on j). ✓.

Also subtle: when a player claims the last pile (k=1), game ends immediately — remaining budget irrelevant. ✓ modeled.

Also: could a player want to claim even when at k=1 they could also pass? They claim and win; f(1)=W ✓.

Alright. Also handle input parsing robustly (A may span lines — but per format it's one line; use sys.stdin.read for safety).

Let me write final code with sys.stdin.read().split().

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1:1+n]
    c = sum(1 for x in a if int(x) & 1)
    if n == 1:
        w = True
    elif n == 2:
        w = False
    elif n == 3:
        w = c >= 1
    else:
        w = (c & 1) == 1
    sys.stdout.write("Fennec\n" if w else "Snuke\n")

main()

Wait — I want to double-check the n=2 case isn't actually following "c odd → Fennec" in some sub-case I dismissed. f(2,c,0)=L for c=0,1,2 — verified via DP and direct simulation. ✓.

And n=1 with even A_1: Fennec claims index 1, S={1}={1..N} → Fennec wins ✓.

I'm confident. Let me also reflect: is there any chance the DP's parity-only claim breaks when p is large but a claim adds a huge amount changing... no, only parity matters per proof. The proof: by induction on k, W_k(M,p) depends only on (k, c, p mod 2). Base k=1 trivial. Inductive step: C(q) depends on f(k-1) at known parities only. W(0)=C0; W(p odd)=C1∨¬C0; W(p even ≥2)=C0∨¬W(p-1 odd)=C0∨¬(C1∨¬C0)=C0. ✓. So f well-defined. Done.

Final answer code as above. Time O(N).

## worker: Cross-check the derived rule (N=1→Fennec; N=2→Snuk
- **Model**: Each index needs exactly one "claiming" move to enter S; all other moves on it are passes consuming its remaining tokens. State reduces to (k = unclaimed piles, multiset of remaining pile sizes, total pass budget p). Claiming the last pile wins immediately.
- **Derived rule** (proved by induction on k, showing win/lose depends only on k, the count c of odd-sized remaining piles, and p mod 2):
  - k=1: player to move always wins (claims last pile).
  - k=2: player to move wins iff p odd (claiming hands the win to opponent; pure pass war).
  - k=3, p=0: first player wins iff c ≥ 1.
  - k≥4, p=0: first player wins iff c is odd.
- **Initial position** has p=0, k=N, c = number of odd A_i, giving the rule implemented in `rule()`/`main()`.
- **Cross-check**: `cross_check()` enumerates all N∈{1,2,3,4}, A_i∈{1,2,3} (120 instances) and compares the exact recursive game solver `solve_game` (full game-tree search over (token tuple, claimed mask) states with memoization) against the closed-form `rule`. Running `python program.py check` prints `mismatches = 0`, confirming the rule on all small cases, including edge sub-cases: N=1 with even A_1 (Fennec), N=2 with odd counts (Snuke), N=3 all-even (Snuke) vs ≥1 odd (Fennec), N=4 parity-of-c cases.
- Spot verifications by hand simulation also matched: (2,2,2)→Snuke, (1,1,1,1)→Snuke, (1,1,1,2)→Fennec, (1,2,2,2)→Fennec, all-ones N=5→Fennec, all-twos N=5→Snuke; plus all three samples (Fennec/Snuke/Snuke).
