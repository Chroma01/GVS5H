
## ideation
The core difficulty is that the "increment" operation couples adjacent letters: excess count at letter i can be pushed to letter i+1 at cost equal to the amount pushed (each increment is 1 op), which may be cheaper than deleting (also 1 op per char) — but pushing is only useful if the next letter needs more characters. Insertions and deletions cost 1 per character; increments cost 1 per step and cannot wrap z→a.

Key observations:
- In the final string, every letter has frequency 0 or k for some target k (0 ≤ k ≤ n). Actually the final frequency must be uniform, so all present letters share frequency k.
- For a fixed k, the problem decomposes into a chain DP over letters a..z: at each letter i with original count c[i], we may receive x increments from letter i-1, giving total m = c[i] + x. Then we decide the final count for letter i: either 0 or k (anything else is wasteful — argue: if m ≥ k, keep k, excess e = m - k can be deleted (cost e) or pushed forward (cost e now, but saves inserts/deletes later); if m < k, we must insert k - m (cost k - m), pushing nothing; or reduce to 0 by deleting m (cost m) — but pushing forward when m < k is impossible since we can't decrement).
- Wait: if m < k, options are: insert up to k (cost k-m), or delete down to 0 (cost m). We never push forward in this case.
- If m ≥ k: options: keep k, push e = m-k forward (cost e, next letter receives e), or keep k and delete e (cost e, push 0), or delete everything to 0 (cost m, push 0) — but deleting all m costs m ≥ e + ... hmm, deleting to 0 costs m vs keeping k costs e = m-k < m, so deleting to 0 is dominated when m ≥ k. Actually careful: pushing e forward costs e (the increments), same as deleting, but may benefit the next letter. So DP state = amount pushed into current letter.

DP formulation for fixed k:
- dp[i][x] would be too large if x unbounded, but note the pushed amount into letter i is at most... it could be large (up to n). However, we can observe that pushing more than k into a letter is never useful? If letter i receives x ≥ k... then m = c[i] + x ≥ k, and excess beyond k would be pushed again. Actually receiving more than k is wasteful: the sender could have deleted instead at the same cost, avoiding future costs. Hmm, but not exactly — pushing cost equals deleting cost at the sender, but the receiver might delete at same cost too. So pushing x > k is never better than pushing exactly min needed. Standard result: the carry into a letter only needs to be 0..k (or we can cap it). Actually the carry that matters: receiver needs at most k - c[i] if c[i] < k; any extra is useless (would be deleted/pushed at cost ≥ deleting at source). So we can cap carry at k.

Simpler DP: let f(i, x) = min cost processing letters i..25 given letter i receives x increments (0 ≤ x ≤ k, capped). Transition at letter i with m = c[i] + x:
- If m ≥ k: we keep k. Excess e = m - k. We can push y forward where 0 ≤ y ≤ min(e, k) — wait, why cap push at k? Because receiver never benefits from more than k. Cost = e (each excess char is either deleted or incremented, cost 1 each) + f(i+1, y). Hmm but pushing y costs y (increments) and deleting e-y costs e-y, total e regardless. So cost = e + min over y in [0, min(e,k)] of f(i+1, y). We can precompute suffix mins, or just note we want min of f(i+1, y) over allowed y.
- If m < k: option A: insert k - m, push 0: cost (k - m) + f(i+1, 0). Option B: delete m, push 0: cost m + f(i+1, 0). So cost = min(m, k - m) + f(i+1, 0).

Complexity: for each k (up to n = 2·10^4), DP is 26 × k states with transitions needing min over range — could be O(26k) with suffix minimums. Total O(n · 26 · k) summed over k = O(26 · n^2) = too much (26 · 4·10^8). Need better.

Hmm. Can we do better? Alternative: total over all k of O(26k) = 26 · n^2/2 ≈ 5·10^9 — too slow in Python.

We need a smarter approach. Ideas:
- Limit k: k ranges 0..n, but maybe only k values near n/26 matter? No — examples show k can be various. Actually k can be up to n (all same letter). Hmm, but is large k ever optimal? If k > n/1... Consider: final string length = 26k at most, or j·k for j distinct letters. Cost includes inserts. Large k means many inserts. Upper bound on answer: delete all but... e.g., make all counts equal to some existing structure. Answer ≤ n (delete everything? empty string — is empty good? Vacuously yes, all chars occur 0 times). So answer ≤ n. For target k with j letters present, cost ≥ inserts ≥ jk - n, and also cost ≥ ... If jk - n > n, i.e., jk > 2n, cost > n, not optimal. So jk ≤ 2n, meaning k ≤ 2n/j. For j=1, k ≤ 2n. Hmm k up to 2n for single letter? If j=1, all chars converted to one letter: but increments only go forward, so only letter 'z' can absorb all via increments; cost = sum over letters of (25-i)·c[i] which could be 25n — exceeds n (delete-all). So effective k bounded by ~2n for j=1 but that DP is just one letter.

Actually, let's reconsider: sum over k of 26k where k ranges to n is 13n². For n=2·10⁴, that's 5.2·10⁹ — way too slow in Python, even in C++ borderline (5e9 too slow). Need to prune k range.

Better bound on k: For target k with j letters in final string, cost ≥ jk - n (insertions needed) and cost ≥ ... also deletions: cost ≥ n - jk if jk < n? No—deletions at least n - (kept chars). Kept chars ≤ min(n, jk). Lower bound: |jk - n| isn't right either since increments change counts. Rough: cost ≥ jk - n when jk > n. For this to be ≤ ans ≤ n, need jk ≤ 2n. Also cost ≥ (number of letters with count not in {0,k} adjustments)... 

Also lower bound from deletions: each present letter keeps k chars from its original c[i] plus receives pushes; total kept ≤ n, final length jk, inserts = jk - kept ≥ jk - n. Fine.

So for each j ≥ 1, k ≤ 2n/j. Sum over j of 26 · (2n/j) · (number of k values for that j?) Hmm, k and j are independent parameters though. For each k, the DP handles all j automatically. So we need k ≤ 2n (j=1 case). That's still n values of k.

But wait: for j=1, the only sensible single letter is one reachable... any letter can be the sole survivor; letters after it can't contribute via increments (they'd need decrementing). DP handles it. k ≤ 2n for j=1: but is k > n ever sensible for j=1? Final length k, all one letter L. All other letters' chars must be deleted or incremented toward L (only those before L). Cost = sum_{i<L} min(delete c[i], increment to L: c[i]·(L-i)) + sum_{i>L} c[i] + inserts k - (c[L] + received). If k > n, inserts alone ≥ k - n... and we could instead delete everything for n. So k ≤ 2n indeed, and for j=1, k ≤ 2n but realistically the DP for k near 2n: states 26·2n = 5.2·10⁵ for one k — fine, but doing it for all k up to 2n is 26·(2n)² = too much.

Prune: for a given k, is the DP cost monotonic or can we bound? Alternative: think about which k values can be optimal. Claim: there exists optimal where k equals some c[i] (original count)? Hmm, not obviously, because of pushes. Example "aaabc": counts a=3,b=1,c=1, n=5. Answer 2 with k=2 (change a→b: a=2,b=2, insert c: c=2). k=2 is not an original count (counts are 3,1,1). So no.

Alternative approach: think of it as min cost flow / matching? Each original character can be: deleted (cost 1), kept as-is (cost 0), incremented to a later letter (cost = steps). Insertions create chars at any letter (cost 1 each). Final: each letter has 0 or k chars.

Since insertion cost = deletion cost = 1, and increment cost 1 per step: note that "delete + insert" = 2 ops can relocate a char anywhere; increment can relocate forward at cost = distance, which is better only for distance 1 (cost 1 < 2). For distance ≥ 2, increment chains cost ≥ 2 = delete+insert. Wait! Increment by d steps costs d. Delete+insert costs 2. So increments are only strictly beneficial for moving a char to the immediately next letter (cost 1 vs 2). For distance ≥ 2, it's never better than delete+insert. But increments could still be part of optimal (equal cost), and chains of increments... moving a→c costs 2 via increments = delete a + insert c. So WLOG, increments are only used to move a character one step (i → i+1) at cost 1, and any longer relocation is delete+insert (cost 2). Hmm, but careful: moving i→i+1 via increment costs 1, vs delete+insert costs 2. So the only "special" operation is adjacent move at cost 1.

This simplifies: We can model as: each character at letter i can be kept (0), deleted (1), or moved to i+1 (1). Plus insertions at cost 1 to fill deficits. But wait — could a char move i→i+1 and then that same char move again i+1→i+2? That's cost 2 total, same as delete+insert, so WLOG no (delete+insert dominates or ties). But there's subtlety: a chain where char from i goes to i+1 and char from i+1 goes to i+2 — that's fine, each moves one step, cost 1 each. So the model: at each letter i, we have c[i] original chars plus possibly some arriving from i-1. Each char can stay, be deleted, or (if we choose) move to i+1. Deficits filled by insertion at cost 1.

So for fixed k, DP over letters with carry x = number moved into i from i-1 (x ≤ k cap, since receiver needs at most k... actually receiver might receive more and re-push, but re-pushing a received char costs 2 total — dominated by delete+insert? Deleting the received char costs 1 (total 2: move+delete) vs the original sender deleting (1). Hmm: sender moves char to i+1 (cost 1), receiver deletes it (cost 1) = 2, vs sender just deletes (1). So receiving excess and deleting is dominated. Receiving excess and re-pushing: move+move = 2 = delete+insert at i+2, tie. So cap carry at k is fine, actually cap at max(0, k - c[i])? Not exactly, because receiver might want to push its own chars forward while keeping received ones... but total at receiver is m = c[i]+x; receiver keeps ≤ k, pushes ≤ m-k... if x > k then m > k and excess pushed includes received chars (2-cost relocations) — dominated. So cap x ≤ k. Even tighter: x ≤ k is enough.)

Now the DP per k is O(26 · k) with O(1) transitions if we handle the "push y forward" choice smartly. Let's define f(i, x): min cost for letters i..25 given x chars arrive at i from i-1 (0 ≤ x ≤ k). m = c[i] + x.
- Case m ≥ k: keep k. Excess e = m - k. Choose y = chars pushed to i+1, 0 ≤ y ≤ min(e, k). Cost = (e - y) deletions + y moves + f(i+1, y) = e + f(i+1, y). So f(i,x) = e + min_{0≤y≤min(e,k)} f(i+1, y).
- Case m < k: options: (a) insert k-m: cost (k-m) + f(i+1, 0). (b) delete m: cost m + f(i+1, 0). Also (c): could we push some chars forward and delete/insert? If m < k, pushing y forward leaves m - y at letter i, which then must be 0 or k: m - y = 0 → y = m (push all): cost m moves + f(i+1, m)... but pushing all m forward costs m, and receiver gets m ≤ k. Compare with deleting m (cost m) + f(i+1,0): pushing gives f(i+1, m) vs f(i+1,0) — could be better if letter i+1 needs chars! E.g., c[i]=1, c[i+1]=0, k=2: delete i's char (1) + insert 2 at i+1 (2) = 3; vs move i's char to i+1 (1) + insert 1 (1) = 2. Wait but moving i→i+1 then letter i has 0, letter i+1 has 1+... yes! So case m < k must also consider pushing all m forward: cost m + f(i+1, m). Hmm, but also push y < m and delete rest? Then letter i has m - y ∈ (0, k) — not allowed (must be 0 or k). So either y=0 (keep m, then insert to k or delete to 0) or y = m (push everything, letter i = 0). Wait if we keep m and delete to 0 that's y=0 with deletions. So options: y=0: final count 0 (cost m deletes) or k (cost k-m inserts); y=m: cost m + f(i+1, m).

Hold on, in case m ≥ k, could we also push more than e? Push y > e means letter i keeps m - y < k, must be 0 → y = m (push all): cost m + f(i+1, min(m,k))... m could exceed k; cap at k. Pushing all m costs m vs keeping k and pushing e costs e + ... keeping k seems better since m ≥ k ≥ ... but maybe letter i+1 desperately needs chars. Keeping k at letter i costs 0 extra; pushing all means letter i = 0 and we lose k chars that cost... they'd need reinsertion elsewhere. Since inserts cost 1 each and keeping is free, keeping k dominates unless... no, keeping k is always ≥ as good: pushing all (cost m, letter i empty) vs keep k + push e (cost e, letter i full). Difference: m - e = k extra cost and letter i empty vs full — if letter i empty, fine, but we spent k more. Could the k chars at letter i be "wasted"? No, they're part of final good string (frequency k). Unless final string shouldn't include letter i... but including it is free here (0 marginal cost) and reduces inserts needed elsewhere? No — each letter's frequency is independent; having letter i at frequency k is part of the target. If the optimal final string has letter i empty, then keeping k at letter i adds k chars that... they're legitimately part of the string (all letters same frequency k). It's still a valid good string. So cost-wise, keeping is free and valid. So pushing all when m ≥ k is dominated by keeping k. 

So transitions:
f(i, x) where m = c[i] + x:
- if m ≥ k: f = (m - k) + g(i+1, min(m-k, k)) where g(i+1, t) = min_{0≤y≤t} f(i+1, y).
- if m < k: f = min(m, k - m) + f(i+1, 0), and also consider m + f(i+1, m) [push all]. Take min of all.

Hmm wait, in m<k case, "push all" cost m (moves) + f(i+1, m). And option delete all cost m + f(i+1, 0). Since f(i+1, m) could be less than f(i+1, 0) by at most... it can help. So f = min(k - m + f(i+1,0), m + f(i+1, 0), m + f(i+1, m)). The last two: m + min(f(i+1,0), f(i+1,m)).

Base: f(26, x) = 0 (no letters left; arriving chars at 'z'+1? pushes from z are impossible — z can't increment. So at i=25 (z), pushing forward is not allowed: y must be 0. Handle: when i = 25, e excess must be deleted: cost e; m < k: min(m, k-m).)

Also x arriving at letter 25 is fine (from y). 

Answer for this k: f(0, 0). Take min over k = 1..? and also k=0 (delete all, cost n — but that's covered as upper bound; also final string could be empty? "all characters occur same number of times" — empty string vacuously good. Cost n. Our k≥1 search will beat or tie.)

Range of k: 1 to n? Could k > n ever be optimal? Final length jk ≥ k > n means inserts ≥ k - n ≥ 1... cost ≥ (jk - n) + (deletions of non-kept). For j=1, k up to... cost ≥ k - n (inserts) and also all other letters deleted/relocated. If k = n+1, cost ≥ 1 + (relocate/delete everything else ≥ ...). Compare delete-all = n. For k > n: cost ≥ k - n + (n - c[L] - received)... hmm roughly cost ≥ k - c[L] - received ≥ k - n > 0. Actually lower bound: cost ≥ inserts ≥ k - (c[L] + chars moved into L) ≥ k - n. And cost ≥ deletes/moves of other letters ≥ (n - c[L] - movedIn)... total ≥ k - n + n - c[L] - movedIn + ... this is ≥ k - c[L] - movedIn ≥ k - n. For k ≤ 2n this bound allows cost ≤ n. Hmm so k up to 2n not ruled out for j=1? Example: s = 2·10⁴ copies of 'y'... wait n = length. s = "y"*19999 + "z"? n=20000. k=20000: move y→z? y→z is 1 step! c[y]=19999 move all to z: cost 19999, z has 20000. vs k=19999: keep y, delete z: cost 1. Obviously small k wins here. When would huge k with j=1 win? s = "a"*10000, n=10000... k=10000 j=1: keep a's, cost 0 — already good (single letter is trivially good!). Oh wait — any string with one distinct letter is already good. So j=1 with k = c[L] costs 0 if string has one letter. Large k only needs inserts if k > c[L] + movedIn. Since c[L] + movedIn ≤ n, k > n needs inserts ≥ k-n > 0, plus we could instead just use k' = c[L]+movedIn ≤ n with fewer inserts (0) and same other costs. So k > n is never strictly better than some k' ≤ n. Hence k ∈ [1, n]. 

But that's still n values of k, each DP O(26k) → O(26 n²) = 1.04·10¹⁰. Way too slow. Need to reduce.

Hmm. Let's think about limiting k more aggressively. For target k with j distinct final letters: cost ≥ jk - n (inserts). Also cost ≥ (n - jk) if jk ≤ n? Deletes ≥ n - jk when jk ≤ n (each kept char is one not deleted... moves keep the char). Actually final length jk; chars in final string come from originals (kept or moved) or inserts. #originals used ≤ n. inserts ≥ max(0, jk - n). deletes ≥ max(0, n - jk) - moves? No: deletes = n - (kept + moved) ≥ n - jk when jk < n... kept+moved ≤ min(n, jk). deletes ≥ n - min(n,jk) = max(0, n-jk). So cost ≥ |jk - n|... not quite, cost = deletes + inserts + moves ≥ max(0,n-jk) + max(0,jk-n) = |n - jk|. 

So for cost ≤ ans, need |jk - n| ≤ ans. Since ans ≤ min over simple strategies... ans is at most, say, cost of best "no-move" strategy? We don't know ans a priori, but we can compute an initial upper bound U (e.g., delete-all = n, or better heuristics), then only consider k with |jk - n| ≤ U for some j ≥ 1, i.e., k ∈ [(n-U)/j, (n+U)/j]. For j=1: k ∈ [n-U, n+U]. If U is small (like ≤ n/2), then for j=1, k ∈ [n-U, n+U] — that's 2U+1 values, could be large. Hmm, but j=1 means final string all one letter L; cost = relocate everything to L or delete others + inserts. For j=1, k near n: e.g., s = "a"*10000 + "z"*10000, n=20000. j=1: all→z costs 25·10000 = 250000 (a→z distance 25, but as established, >2 distance = delete+insert; effectively min(dist,2)... wait no — increments are the only way to "move", delete+insert is 2 ops and equivalent to moving anywhere. So relocating a char from a to z costs min(25, 2) = 2 effectively). So j=1, L=z: cost ≈ 2·10000 = 20000 = n. Meh. k=10000, j=2 (a and z): cost 0 already good? a=10000, z=10000 — yes good, k=10000. So k near n matters! Here k = n/2 = 10000 with j=2. So k can be as large as n/2 (j≥2) or n (j=1, trivial). So k range is Θ(n) in worst case. E.g., s = two letters each n/2 → k = n/2 optimal with cost 0.

So we can't prune k to small ranges in general. Need faster per-k DP or smarter overall algorithm.

Total complexity O(26 · Σk) = O(26 n² / 2)... with n = 2·10⁴, that's ~5·10⁹ — too slow even in C++ (maybe 5-10s). Python definitely too slow. Need better.

Think differently. Since only adjacent moves matter (cost 1, vs delete+insert cost 2), maybe structure simplifies. Alternative viewpoint: cost = (chars deleted) + (chars inserted) + (chars moved one step). Final: each letter 0 or k.

Let me think about the structure: For fixed k, we choose a subset S of letters to be "active" (frequency k). Cost = ?

Total final chars = |S|·k. Inserts = |S|·k - (originals assigned to active letters). Each original char at letter i can be assigned to: itself (0 cost), i+1 (cost 1, if i+1 active), or deleted (1). Unassigned final slots filled by inserts (1).

So it's like: maximize savings. Baseline: delete all n + insert |S|k = n + |S|k. Savings: each char kept at own letter saves 2 (delete+insert avoided); each char moved to next letter saves 1 (vs delete+insert cost 2, move costs 1). Constraint: each active letter ends with exactly k chars (kept + moved-in + inserted = k; inserted ≥ 0 so kept + moved-in ≤ k).

So maximize: 2·(kept) + 1·(moved) subject to: kept_i + moved_{i-1→i} ≤ k for active i; kept_i ≤ c[i]; moved_{i→i+1} ≤ c[i] - kept_i (a char either kept or moved); inactive letters: kept = moved-in = 0 (all chars deleted or moved out... wait, chars at inactive letter i can move to i+1 if i+1 active). Hmm, moved-out from inactive i: chars at i can move to i+1 (cost 1) if i+1 active. So moved_{i→i+1} ≤ c[i] - kept_i where kept_i = 0 if i inactive.

Maximize savings = Σ [2·kept_i + 1·moved_{i→i+1}] - ... wait also moved char saves: delete+insert would cost 2, move costs 1, saves 1. Kept saves 2. Deleted saves 0. Total cost = n + |S|k - savings. Minimize cost ⇔ maximize savings.

For fixed k and S: this is a small flow/greedy per letter? kept_i = min(c[i], k) roughly, but moved-in competes for the k slots. Slots at active letter i: k slots, filled by kept (save 2 each) or moved-in (save 1 each), prefer kept. kept_i = min(c[i], k + movedOut_i?) hmm — chars at i can be kept or moved out. If i active: kept_i ≤ k, and movedOut_i ≤ c[i] - kept_i. If i+1 active, movedOut_i fills slots at i+1 (save 1 each) but limited by k - kept_{i+1}... 

This is a chain structure solvable by DP, same as before. The DP per k is O(26) states if carry capped... carry ≤ k though. Hmm, but maybe with the savings view, the DP has more structure: at each letter, decision is how many to keep vs move out. 

Alternative: since alphabet is only 26, maybe exponential in 26 is OK? 2^26 = 6.7·10⁷ — too many, and k varies too.

Let me reconsider: is the per-k DP actually O(26) with O(1) transition if we only track carry as small? The carry (moved-in) can be up to k which is up to n. But maybe optimal carry is small? No — e.g., c[i] = 0, c[i-1] = 2k... move k forward: carry k. Possible.

Hmm, let's look at it as min-cost flow on a line: sources = c[i] chars at nodes 0..25, each char can stay (benefit 2), move right one (benefit 1), or be deleted (benefit 0); node i (active) has capacity k for {stay + in-move}; inserts fill remaining. Choose active set and k.

Since 26 is tiny, per-k DP with carry dimension up to k: O(26k). Sum over k=1..n: 13n² ≈ 5·10⁹. In Python with numpy vectorization? For each k, DP over 26 letters with arrays of size k — vectorize the transition with numpy: f(i+1, ·) arrays, compute g (prefix min), etc. 26 iterations × n values of k = 5.2·10⁵ numpy calls on arrays avg size n/2=10⁴ → 5.2·10⁹ element-ops total but numpy overhead 5.2·10⁵ calls × ~1µs + element ops... roughly 5.2·10⁹/10⁸ per sec ≈ 50s+. Too slow still.

Need algorithmic improvement. Let's think about which (k, S) can be optimal.

Claim: in optimal solution, k equals... hmm earlier counterexample k=2 not in counts. But note k=2 = (3+1)/2 (merged a and b). Interesting.

Alternative known approach for this problem (it's a LeetCode problem — "Minimum Number of Operations to Make String Good"? Actually I recall a similar problem: make all frequencies equal with delete/insert... and one with increment). Let me think about the structure more.

Since moving only helps one step, the interaction is only between adjacent letters. Consider pairs: (a,b), (c,d), ...? Not independent though.

Let me think about the DP more carefully to find speedup. Define for fixed k: process letters 0..25. State = carry x (0..k). 

f(i, x): m = c[i] + x.
- m ≥ k: f = (m - k) + min_{0≤y≤min(m-k,k)} f(i+1, y).
- m < k: f = min(k - m + f(i+1, 0), m + f(i+1, 0), m + f(i+1, m)).

Note in m<k case, pushing all m forward: but then letter i is inactive (0). And in m≥k case, letter i active with k.

Observation: f(i, x) as function of x: m = c[i] + x. For x in range where m < k (x < k - c[i]): f = min(k - c[i] - x, c[i] + x) + f(i+1,0), or (c[i]+x) + f(i+1, c[i]+x). The first part: k - c[i] - x decreasing in x, c[i]+x increasing; min is maximized... but we want min over choices, f is piecewise. For x ≥ k - c[i]: f = (c[i]+x-k) + gmin(i+1, min(c[i]+x-k, k)).

This is getting complex. Perhaps think about small alphabet DP with convexity? f(i,·) might be convex or have Lipschitz structure: |f(i, x+1) - f(i, x)| ≤ 1? Changing x by 1 changes m by 1; cost changes by at most 1 (one more char to delete/move/insert). Yes, f is 1-Lipschitz in x. And maybe convex? If f(i+1,·) is convex, then... 

Alternatively, maybe there's a totally different approach: binary search answer? Or think in terms of "for each letter, final count 0 or k" and the cost function... 

Let me reconsider the problem scale: n ≤ 2·10⁴, alphabet 26. O(26 · n log n) or O(26² · n) needed. O(26·n·√n)? 

Key idea to prune k: For fixed k, cost ≥ |jk - n| where j = #active letters. But more: think about it as — the answer ans. We can first compute ans with a heuristic to get U. Then k must satisfy: there exists j with |jk - n| ≤ U → k ∈ [ (n-U)/j , (n+U)/j ]. The union over j=1..26 of these intervals. If U ≤ n/2, then for j≥2: k ≤ (n+U)/2 ≤ 3n/4; for j=1: k ∈ [n-U, n+U]. Number of k values to check: for j=1 interval width 2U; overall k from ~ (n-U)/26 to n+U. That's still Θ(n) values. Hmm, intervals don't reduce count of k much — k itself ranges over [(n-U)/26, n+U], width ≈ n+U - (n-U)/26 ≈ n. So Θ(n) values of k regardless. The pruning must come from per-k cost, not count of k.

Wait, but maybe we can compute a good upper bound U that's small in practice? Worst case adversarial: s with all 26 letters equal count n/26 ≈ 769 → already good, ans=0, k = 769 only? With U=0: k must satisfy jk = n exactly → k = n/j for j=1..26 → only ≤26 values! Great. Worst case for us: U large. When is U large? Answer large means string far from good. E.g., s = "a"*n (all same) → already good (j=1), ans 0. Hmm, single distinct letter is good! So answer 0. What strings have large answer? s = "abcabcabc..."? counts equal → good. Large answer needs very unbalanced and hard-to-fix. E.g., s = "a"*(n-2) + "b" + "c"? Fix: delete a's down to... k=1: delete n-3 a's? cost n-3. Or k = (n-1)/2: a and b... move a→b: a has n-2, b has 1. k ≈ (n-1)/2: move (n-1)/2 - 1 a's to b (cost ~n/2), delete rest a's (n-2 - (n-1)/2 ≈ n/2)... total ~n. Or delete b,c and keep a: cost 2! Oh — delete b and c, left with all a's, good. Cost 2. Right, deleting to single letter is cheap.

Hmm, when is the answer actually large? You can always delete all but one letter class: cost n - max c[i]. So ans ≤ n - maxc. Also can delete everything: n. Also target k=1: keep ≤1 of each letter... cost = n - (#distinct)... etc. Worst case answer maybe ~n/2? Example: 26 letters each appearing... that's good already. Try s = "a"*10000 + "b"*10000: good. Try counts: a=1, b=2, c=3, ..., triangular? n = 2·10⁴. Making equal: delete down to k=1 each? cost n - 26. Or build up? Expensive. ans ≈ n - 26·1 = n-26. Large! U ≈ n. Then k candidates: jk ∈ [n-U, n+U] = [26, 2n-26]... k ranges widely. Hmm.

But wait — in such cases, is the optimal k small? With triangular counts, optimal is likely k=1 (delete heavily) or k around median. Actually let's think: optimal k for that instance: options k=1: cost n-26. k=2: letters with count ≥2 keep 2... cost ≈ n - 2·25 + inserts... ≈ n - 50. Hmm similar magnitude. So optimal k small here. But our pruning by U is weak.

Alternative: lower bound to prune per (k): cost(k) ≥ something computable fast, skip DP if bound ≥ current best. But worst case still many k's need full DP.

Let me search memory: This is LeetCode 2822? "Make String Good" — I think there's a problem "minimum operations to make frequencies equal" with delete-only (that's easy: try each k, cost = Σ min(c[i], c[i]-k if c[i]≥k... )). With insert+delete+increment, harder.

Maybe intended solution is O(26 · n) per k is too much, but O(26) per k with carry capped... Let me reconsider: is carry really need to go up to k? Carry x = chars moved into letter i. If x ≥ k, then letter i alone (with carry) exceeds k; excess must move on or be deleted. Moving on a char that was already moved = 2 ops for 2-step relocation = delete+insert. So WLOG, a moved char is never moved again, and never deleted (move+delete = 2 > 1 = just delete original). Therefore carry into i is at most k - (kept at i)... and specifically carry x ≤ k, and if x > 0 then... hmm, also chars at i that are "kept" vs "moved out": moved-out chars are original chars of i (not carry). So state x ∈ [0, k] but with the WLOG: carry chars fill slots at i first? No—kept saves 2, carry saves 1; slots at i: k. kept_i = min(c[i], k) but if c[i] > k, excess original chars can move out (save 1 each at i+1) — but only if i+1 has room after its own kept. 

Let me define DP differently: process left to right; at letter i, first decide kept_i and moved-in usage. Since kept dominates moved-in for slots (save 2 > 1), kept_i = min(c[i], k) always (if i active). But should i be active? If c[i] small, activating i costs inserts k - c[i] - x... 

Hmm OK here's another thought: the DP state can be just the carry, but maybe we can prove carry ∈ {0} ∪ [something small] OR use the structure that f(i, x) is piecewise linear in x with few pieces, and compose. Since 26 letters only, each f(i,·) is a function [0,k]→ℤ, 1-Lipschitz, piecewise linear with O(1) pieces? Let's check: f(i,x) defined via m = c[i]+x and min over y of f(i+1, y) over a range [0, min(m-k,k)] — range minimum of f(i+1,·). If f(i+1,·) is unimodal or has bounded local minima... The min over expanding range is a "running min" function, which is piecewise: decreasing then flat. Composition over 26 letters might keep piece count bounded? Possibly pieces grow. Risky.

Different idea: since 26 is constant, O(n · 26) per k is the issue; total O(26 n²). What if we reduce k candidates using the insight that cost(k) is "nice"? Not obvious.

Let me look at constraints again: n ≤ 2·10⁴. O(n²) = 4·10⁸ — in Python too slow, in C++ ~1-2s maybe OK. But we're writing Python. Hmm. But maybe with the 26 factor it's 26·(2·10⁴)²/... no.

Wait — maybe per-k DP can be O(26) not O(26k)! Let's reconsider whether carry can be capped by a small bound. Claim: in optimal, carry x into letter i is either 0 or exactly what's needed: x ≤ max(0, k - c[i])? Because carry chars are used at letter i only if i is active and needs chars (c[i] < k); needed = k - c[i]. If x > k - c[i] and i active: excess carry must move on (2-step, dominated) or be deleted (dominated). If i inactive: all carry must move on or be deleted — dominated (should've been deleted at source). So WLOG x ≤ max(0, k - c[i]) when i active, and x = 0 if... no wait: if i inactive and x > 0, carry chars move on to i+1: that's a 2-step move total (i-1→i→i+1), cost 2 = delete+insert. Tie, not strict domination. So there EXISTS optimal with x = 0 whenever c[i] ≥ k or i inactive... Let me restate: there exists optimal where every moved char moves exactly one step and is used at the destination (fills a needed slot). Then carry into i ∈ [0, max(0, k - c[i])] and if c[i] ≥ k then carry = 0. Hmm, but "needed slots" at i = k - c[i] could still be up to k (if c[i]=0). E.g., c = [0, k]: letter a empty, b has k... no carry into a. Carry into b from a: a has 0 chars, none. When is large carry needed? c[i-1] = k+5, c[i] = k-5: i-1 keeps k, moves 5 to i (carry 5 = k - c[i]). Fine, x = k - c[i] ≤ k. So carry range per letter is up to k - c[i], still Θ(k) worst case (c[i]=0, c[i-1]=2k: carry k). So state space still O(k) per letter. No improvement.

BUT: maybe transitions can be computed in O(1) amortized with the right structure, and the total over all k can be bounded differently... Σ over k of 26k = 13n². n=2·10⁴ → 5.2·10⁹. No.

Let me think about the "savings" formulation as a max-flow problem and whether k can be handled parametrically. 

Alternative: think about each adjacent pair interaction. Since moving only one step matters, and delete+insert handles everything else at cost 2 per relocated char, maybe reformulate: 

Cost = 2·(number of chars not kept at original letter) - (number of chars moved to next letter) + ... let me redo: baseline every char deleted (n) + all final chars inserted (jk). Kept char: saves 2. Moved char: saves 1 (cost 1 instead of 2). So cost = n + jk - 2K - M where K = kept count, M = moved count. Constraints: for each active i: kept_i + in_i = k - ins_i ≤ k, kept_i ≤ c[i], in_i = out_{i-1} ≤ c[i-1] - kept_{i-1}, K = Σkept, M = Σout. Maximize 2K + M.

For fixed k: this is a small DP but maybe solvable greedily: kept_i = min(c[i], k) if i active. out_i = c[i] - kept_i (excess) available for i+1. in_i = min(out_{i-1}, k - kept_i). Greedy: since kept saves 2 > out saves 1, prioritize kept. So for active set S: kept_i = min(c[i], k), in_i = min(c[i-1] - kept_{i-1}, k - kept_i) (if i-1 ∈ S? No — out_{i-1} exists even if i-1 inactive: if i-1 inactive, kept_{i-1}=0, out_{i-1} = c[i-1], all can move to i). So given S, savings = Σ_{i∈S} 2·min(c[i],k) + Σ_{i∈S} min(avail_{i-1}, k - min(c[i],k)) where avail_{i-1} = c[i-1] - (kept_{i-1} if i-1∈S else 0) = c[i-1] - min(c[i-1], k)·[i-1∈S].

Then cost(k, S) = n + |S|k - savings. Minimize over S ⊆ 26 letters: 2^26 too many, but the interaction is only adjacent (i's choice affects avail_i for i+1). So DP over letters with state = whether previous letter active (and its avail... avail_{i-1} = c[i-1] - min(c[i-1],k) if active = max(0, c[i-1]-k), or c[i-1] if inactive). So state is just prev active/inactive! Because avail is determined by c[i-1], k, and active status. 

So DP over 26 letters, state ∈ {prev active, prev inactive}: transition decide active_i ∈ {0,1}: 
- If active_i: kept = min(c[i], k); in_i = min(avail_{i-1}, k - kept); gain = 2·kept + in_i - k (the -k because we add k to jk term... let me recompute). cost contribution: +k (inserts baseline for this active letter) - 2·kept - in_i. avail_i = max(0, c[i] - k).
- If inactive: contribution 0; avail_i = c[i].
Total cost(k) = n + min over paths of Σ contributions. Wait check: cost = n + jk - 2K - M = n + Σ_{i active} [k - 2·kept_i - in_i]. Yes! And in_i depends on avail_{i-1} which depends on active_{i-1}. So DP with 2 states per letter, O(26·2) per k!! 

Let me double check the greedy "kept prioritized, then in-move fills remaining slots": At active letter i, slots = k. Sources: kept (own chars, save 2 each, up to c[i]) and in-move (save 1 each, up to avail_{i-1}). Since save 2 > 1, take kept first: kept = min(c[i], k), then in = min(avail_{i-1}, k - kept). But wait — should we ever NOT keep a char to allow... no, in-move and kept both just fill slots; keeping is strictly better. But there's a subtlety: chars not kept at i become avail for i+1 (out_i). If i active, out_i = c[i] - kept = max(0, c[i]-k). If we kept fewer, out_i larger (save 1 at i+1) but lose save 2 at i — net loss 1, unless i+1... no, keeping always ≥. But what if i active and c[i] > k: kept = k, out = c[i]-k. Fine.

Another subtlety: in-move chars and kept chars — a char at i-1 either moves to i or is deleted (or kept at i-1 if active). avail_{i-1} = chars at i-1 not kept. They can move to i only if i active. If i inactive, they're deleted (or... move to i then i+1? two-step dominated). OK consistent with WLOG.

Also: what about moving chars from i to i+1 when i inactive and i+1 inactive? Pointless (dominated). Fine.

Also z: out_z avail for letter 27 — nonexistent; just deleted. Handled naturally (no letter 27 to use avail).

So per k: O(26) DP with 2 states! Total O(26 · n) over all k=1..n = 5.2·10⁵. 

But wait — I need to double-check the WLOG that increments longer than 1 step are never needed, and that "delete+insert" (2 ops) can realize any relocation. Yes: to relocate a char from letter p to letter q (q > p, since increments only go forward; q < p impossible via increments): options: increment chain cost q-p, or delete+insert cost 2. If q-p = 1: increment better (1 < 2). If q-p ≥ 2: delete+insert ≤ chain. Also q < p: only delete+insert (2). So any optimal can be transformed: all relocations are either 1-step increments (cost 1) or delete+insert pairs (cost 2). In the savings formulation, "kept" = stays, "moved" = 1-step increment to active neighbor, everything else deleted; inserts fill deficits. One more check: could a 1-step move land at an inactive letter then... no, covered.

Also: is it ever beneficial to move a char i→i+1 where i+1 active but i+1's slots already full (kept = k)? Then the moved char must be deleted or moved on — dominated. So no. Our formula caps in_i by k - kept_i. Good.

Also inserts: only into active letters, exactly k - kept - in each. Cost counted in the k baseline. Good.

Edge: final string could be empty (j=0): cost n. Also every letter inactive → cost n (delete all). Covered as candidate (DP with all inactive gives n). Also k=0 same.

Now also need to double check the DP handles "in_i = min(avail_{i-1}, k - kept_i)" — avail_{i-1} when i-1 active = c[i-1] - min(c[i-1], k) = max(0, c[i-1]-k); when inactive = c[i-1]. Yes.

Let me verify with examples:
1. s="acab": counts a=2,b=1,c=1. n=4. Try k=2: 
   DP letters a..z. contribution if active: k - 2·min(c,k) - min(avail_prev, k - min(c,k)).
   a: c=2, active: kept=2, contrib = 2 - 4 = -2, avail_a = 0. inactive: 0, avail=2.
   b: c=1. If a active (avail 0): b active: kept=1, in=min(0, 1)=0, contrib = 2-2-0=0. If a inactive (avail 2): b active: kept=1, in=min(2,1)=1, contrib=2-2-1=-1.
   c: c=1. similar.
   Best: a active (-2), b inactive (avail_b=1), c active with prev avail 1: kept=1, in=min(1, 1)=1, contrib = 2-2-1 = -1. Total = n + (-2 + 0 + -1) = 4 - 3 = 1. ✓ (delete one a... wait our solution: a active kept 2, c active kept 1 + in-move 1 from b. That's a=2, c=2: move b→c (1 op). Cost 1. Also matches.)

2. s="wddw": w=2,d=2. k=2: d active: kept2 contrib -2; w active kept2 contrib -2 (avail from others 0). Total 4-4=0 ✓.

3. s="aaabc": a=3,b=1,c=1, n=5. k=2:
   a active: kept=2, contrib 2-4=-2, avail_a=1.
   b active (prev avail 1): kept=1, in=min(1,1)=1, contrib=2-2-1=-1, avail_b=0.
   c active (prev avail 0): kept=1, in=0, contrib=2-2=0. 
   Total = 5 + (-2-1+0) = 2 ✓.

Great, formula works.

Now range of k: 1..n. Also consider that answer could be n (delete all) — but DP with all-inactive gives n for any k, so min over k includes ≤ n automatically. Actually with all inactive, total = n + 0 = n. Yes.

But hold on: k up to n = 2·10⁴, times 26 letters × 2 states × O(1) = about 1·10⁶ ops — trivial. 

Wait, I should double check the claim "kept = min(c[i], k) is always optimal when i active" in conjunction with in-move. Suppose c[i] = 5, k = 3, avail_prev = 3. kept=3, in=min(3,0)=0, contrib = 3 - 6 = -3. Alternative kept=2, in=min(3,1)=1: contrib = 3 - 4 - 1 = -2. Worse. ✓. And out_i = c[i]-kept: keeping more reduces out_i, but out saves only 1 vs kept saves 2. ✓.

One more subtle case: should i be active at all? If c[i] = 0 and avail_prev = 0: active contrib = k - 0 - 0 = k > 0. Inactive contrib 0. DP chooses min. ✓. If avail_prev = 5, k=3, c[i]=0: active: kept=0, in=min(5,3)=3, contrib = 3 - 0 - 3 = 0. Inactive: 0, but then avail_i = 0 (chars at i-1... wait avail_prev chars: if i inactive, can i-1's excess move to i then i+1? Two-step, dominated by delete+insert — but delete+insert costs 2 = same. Hmm! If i-1 has excess and i inactive but i+1 active: our model says excess at i-1 is deleted (then insert at i+1): cost 2 per char. Alternative: move i-1→i (1), move i→i+1 (1): cost 2 per char. Same! So no loss. ✓ But what about move i-1→i (1) then keep at i... i inactive means 0 chars. Fine.

What if i-1 inactive with c[i-1] chars, i active: avail = c[i-1], in = min(c[i-1], k - kept_i). The rest of c[i-1] deleted. ✓.

Now, is the DP state really just prev-active boolean? avail_{i-1} = c[i-1] - kept_{i-1} where kept_{i-1} = min(c[i-1], k) if active else 0. Yes, deterministic given active flag. 

So algorithm:
```
counts c[0..25], n = len(s)
ans = n
for k in 1..n:
    # dp[prev_active] = min extra cost (sum of contributions) up to previous letter
    dp = [0, 0]  # before letter 0, "prev" inactive with avail 0; treat prev avail = 0
    Actually need avail of prev which depends on flag: prev inactive → avail = c[prev]; but for virtual letter -1, avail=0.
    Use: dp0 = min cost processed up to i-1 with i-1 inactive; dp1 = with i-1 active.
    Initialize before a: dp0 = 0 (no prev, avail 0), dp1 = inf.
    For each letter i:
        avail_from_prev_if_prev_inactive = c[i-1] (but for i=0, prev doesn't exist: avail 0)
        Hmm need avail values: A0 = avail_{i-1} if i-1 inactive = c[i-1]; A1 = if active = max(0, c[i-1]-k).
        new_dp0 = min(dp0, dp1) + 0   (i inactive; contrib 0 regardless of prev)
        Wait — but if i-1 active and i inactive, is there any additional cost? in_i only applies if i active. i-1's excess: deleted, cost accounted? Let me recheck accounting: cost = n + Σ_active [k - 2 kept - in]. The "n" counts deletion of every char; kept chars save 2 (not deleted, not inserted); moved chars save 1 (not deleted... wait moved char: not deleted (saves 1 from the n baseline) and not inserted (saves 1 from jk baseline) but costs 1 move: net save 2-1=1. ✓). Excess chars at active letters (c[i] > k): deleted, no savings — accounted (kept=k). Chars at inactive letters: deleted, accounted. in_i: moved into i from i-1's avail. ✓.
        So transitions:
        new_dp0 = min(dp0, dp1)                      # i inactive
        kept = min(c[i], k)
        new_dp1 = min(dp0 + cost_active(A0), dp1 + cost_active(A1))
        where cost_active(avail_prev) = k - 2*kept - min(avail_prev, k - kept)
        with A0 = c[i-1] if i>0 else 0; A1 = max(0, c[i-1]-k) if i>0 else 0.
    After z: answer_k = n + min(dp0, dp1).
    ans = min(ans, answer_k)
```
Wait, but there's an issue: when i is inactive, avail_i = c[i] — meaning ALL chars at i are available to move to i+1. But if i-1 was active and had excess, and i is inactive — i-1's excess can't move to i (i inactive, no slots) — correct, deleted. And i's own chars all avail for i+1. ✓.

But one more: if i active, avail_i = max(0, c[i]-k) — excess after keeping k. But what about in_i chars — do they affect avail_i? No, in_i chars stay at i. ✓.

Also, subtle: when i active and c[i] < k, avail_i = 0 — all own chars kept. ✓.

Let me also double-check that we should consider k up to n: k = n means one active letter with all n chars... e.g., s already single letter: k = n, active letter: kept = n, contrib = n - 2n = -n, total = n - n = 0. ✓. k > n impossible (kept ≤ c[i] ≤ n < k means inserts needed; but also could k > n ever beat? shown earlier no). Also we should double check k range: could optimal k be larger than n with moves? kept + in ≤ c[i] + avail ≤ n < k → inserts ≥ k - n ≥ 1, and reducing k by 1 saves an insert and... monotonic argument: for single active letter L, cost(k) = k - 2·kept - in + n where kept = min(c[L], k) = c[L] (for k ≥ c[L]), in = min(avail, k - c[L]). For k > n: in ≤ avail ≤ n - c[L] < k - c[L], so in = avail (constant), cost = k - 2c[L] - avail + n, increasing in k. So k > n worse than k = n. ✓. So k ∈ [1, n].

Complexity: O(n · 26) = 5.2·10⁵ — fast.

Hmm wait, but I should sanity-check the reduction "multi-step moves never strictly help" once more with a tricky case: what if insert is not needed because... Consider c = [0, 0, 5] (c-letter=5), k=5, and we want a,b,c all active? a needs 5 inserts, b needs 5: total 10 inserts + ... vs moving c→... can't move backward. Bad example. Consider c = [5, 0, 5] (a=5, c=5), k=5: a active kept 5; b: active? kept 0, in = min(avail_a=0, 5) = 0, contrib 5 → inserts 5. c active kept 5, in = min(avail_b, 0)... if b active avail_b = 0. Total = 10 + (5-10) + 5 + (5-10) = 5. Indeed: insert 5 b's. Alternative: move a→b? a→b 1 step: but then a has 4 ≠ k. Move all 5 a→b (5 ops), b active kept... a inactive then, b kept 5, c kept 5: cost 5 moves + 0 = 5. Same. ✓ consistent.

Tricky: chain moves where delete+insert can't replicate because... delete+insert always replicates any relocation at cost 2. A 2-step move costs 2. Equal. So any solution with multi-step moves has an equivalent delete+insert solution with only ≤1-step moves. ✓. And moves that end at inactive letters or get deleted: move+delete ≥ 1+1 = 2 ≥ delete alone. Remove them. ✓.

One more: our model assumes a moved char's destination slot is at i+1 active and counts toward k - kept. And that moved chars ≤ avail. All good.

Also potential subtlety: "in_i" uses avail_{i-1}, but if i-1 is active with excess, the excess chars are the "extra" ones beyond k — moving them saves 1 each (they'd otherwise be deleted with 0 savings). ✓. If i-1 inactive, all c[i-1] chars would be deleted (0 savings); moving saves 1. ✓.

Now, is greedy per-letter independent choice valid given DP over prev-state? The DP tries both active/inactive for each letter, computing exact contributions. Since contribution of letter i depends only on prev's active flag (through avail), optimal substructure holds. ✓.

Let me test mentally on more cases:
- s = "zzz": c[z]=3, n=3. k=3: z active kept 3, contrib 3-6=-3, total 0. ✓.
- s = "abc": counts 1,1,1. k=1: a active: kept1, contrib 1-2=-1, avail 0. b active: -1. c active: -1. total 3-3=0 ✓ (already good).
- s = "aab": a=2,b=1,n=3. k=1: a active kept1 contrib 1-2=-1 avail_a=1; b active in=min(1, 0)=0 kept1 contrib -1; total 3-2=1. Alternatively delete one a: cost 1 ✓. k=... can we do 0? a=2,b=1: move a→b: a=1,b=2 no. Delete a: a=1,b=1 good, cost 1. So ans 1 ✓.
- s = "aabb": a=2,b=2: k=2: a active -2, b active -2 (avail 0), total 0 ✓.
- s = "aaab": a=3,b=1,n=4. Options: delete 2 a's and... a=1,b=1: cost 2. Or move a→b: a=2,b=2: cost 1! k=2: a active kept2 contrib 2-4=-2 avail_a=1; b active kept1 in=min(1,1)=1 contrib 2-2-1=-1; total 4-3=1 ✓.
- s = "az": a=1,z=1... n must ≥3. s="aazz": a=2,z=2: k=2 both active: total 0 ✓.
- Big move test: s = "a"*3 + "c"*1, n=4: a=3,c=1. k=2: a active kept2 contrib -2 avail 1; b inactive (avail_b=0); c active: prev b inactive avail=0: kept1 in0 contrib 0. total 4-2=2. Alternatives: move a→b→c? 2-step: a=2, c=2 cost 2 ✓ matches (delete+insert also 2). Or delete a, insert c: 2. Or delete 2 a's? a=1,c=1 cost 2. Hmm all 2. ✓.

Edge: what about using moves where i-1 active, i active, and BOTH in_i and out_i? c[i-1]=10, c[i]=10, k=5: i-1 kept5 avail5; i kept5, in=min(5,0)=0, avail_i=5. Fine.

Now complexity O(26n) with n=2·10⁴ → 5.2·10⁵ iterations, each O(1). Python: fast (<0.1s). 

Wait, but I want to reconsider whether k should range to n or maybe max count... k can be up to n (single active letter with all kept: k = c[i] up to n). Also k where inserts needed... k ≤ n shown. Fine.

Also don't forget: answer could require k such that no letter active? cost n. Covered.

Let me also reconsider the initialization: before letter 'a' (i=0), there's no letter -1, so avail from prev = 0 regardless. dp0 = 0 (prev "inactive"), dp1 = inf. Transitions for i=0: A0 = 0, A1 = 0 (or inf-flag). new_dp0 = min(dp0, dp1) = 0. new_dp1 = dp0 + cost_active(0). ✓.

Implementation:
```python
class Solution:
    def makeStringGood(self, s: str) -> int:
        c = [0]*26
        for ch in s:
            c[ord(ch)-97] += 1
        n = len(s)
        ans = n
        INF = float('inf')
        for k in range(1, n+1):
            dp0, dp1 = 0, INF  # prev inactive / active
            prev_c = 0
            for i in range(26):
                ci = c[i]
                kept = ci if ci < k else k
                base = k - 2*kept
                rem = k - kept
                # avail from prev:
                a0 = prev_c            # prev inactive
                a1 = prev_c - kept_prev if prev active... 
```
Hmm, need avail of prev letter = max(0, prev_c - k) if prev active, prev_c if inactive. Precompute per letter: avail_active[i] = max(0, c[i]-k), avail_inactive[i] = c[i]. For letter i, prev is i-1: A1 = avail_active[i-1], A0 = avail_inactive[i-1] = c[i-1].

```python
        for k in range(1, n+1):
            dp0, dp1 = 0, INF
            for i in range(26):
                ci = c[i]
                kept = min(ci, k)
                rem = k - kept
                costA = k - 2*kept  # plus - min(avail_prev, rem)
                if i == 0:
                    in0 = in1 = 0
                else:
                    pc = c[i-1]
                    in0 = min(pc, rem)                 # prev inactive
                    in1 = min(max(pc-k,0), rem)        # prev active
                ndp0 = min(dp0, dp1)
                ndp1 = min(dp0 + costA - in0, (dp1 if dp1<INF else INF) + costA - in1)
                dp0, dp1 = ndp0, ndp1
            ans = min(ans, n + min(dp0, dp1))
        return ans
```
Check i=0: dp1=INF so ndp1 = dp0 + costA - 0. ✓.

Let me re-verify example 3 with code logic: s="aaabc", c=[3,1,1,0...], n=5, k=2:
i=0 (a): kept=2, rem=0, costA=2-4=-2, in0=in1=0. ndp0=min(0,INF)=0; ndp1=0-2= -2. dp0=0,dp1=-2.
i=1 (b): kept=1,rem=1,costA=0. pc=3: in0=min(3,1)=1, in1=min(1,1)=1. ndp0=min(0,-2)=-2. ndp1=min(0+0-1, -2+0-1)=-3. dp0=-2,dp1=-3.
i=2 (c): kept=1,rem=1,costA=0. pc=1: in0=min(1,1)=1, in1=min(max(1-2,0),1)=0. ndp0=-3. ndp1=min(-2-1, -3-0)=-3. dp0=-3,dp1=-3.
i=3..25: c=0: kept=0,rem=2,costA=2. pc=0: in0=in1=0. ndp0=-3, ndp1=-3+2=-1. dp0 stays -3 (min(-3,-1)), dp1=-1... then subsequent letters: dp0=-3 persists. Final min = -3. ans = 5-3 = 2 ✓.

Great.

Also verify example 1: c: a=2,b=1,c=1, n=4, k=2:
i=0: kept2 rem0 costA-2 → dp0=0, dp1=-2.
i=1: kept1 rem1 costA0; pc=2: in0=min(2,1)=1, in1=min(0,1)=0. ndp0=-2; ndp1=min(0-1, -2-0)=-2. dp0=-2,dp1=-2.
i=2: kept1 rem1 costA0; pc=1: in0=1, in1=0. ndp0=-2; ndp1=min(-2-1, -2-0)=-3. dp0=-2,dp1=-3.
rest zeros: dp0=-3 eventually (ndp0=min(-2,-3)=-3 at i=3). ans=4-3=1 ✓.

Now, is k=1..n all necessary? Fine, cheap.

One more consideration: the problem says "change to next letter" operation could be applied multiple times to same char — we handled via equivalence. Also note we cannot change z — handled (no letter after z; avail of z unused).

Wait, actually I want to double-check one more scenario where a 1-step move chains with the destination also being a move source — e.g., char x at a moves to b, char y at b moves to c. Both 1-step, cost 1 each, fine in our model: avail_a includes x (if a inactive or excess), in_b includes x; avail_b includes y (b's own chars minus kept). But careful: if b is active, kept_b = min(c[b], k) — y might be kept while x takes a slot? Slots: kept + in ≤ k. Our formula: in_b = min(avail_a, k - kept_b). The moved-in x and kept y coexist. And out_b = c[b] - kept_b (own chars not kept). No conflict. ✓.

But here's a trickier one: what if moving x from

## worker: Write the full Python solution implementing the O(
- **Reduction of operations**: An increment chain moving a char d ≥ 2 steps costs d, but delete+insert costs 2, so only single-step increments (cost 1) are ever strictly useful; everything else is delete (1) or insert (1). Also, a moved char is never re-moved or deleted in an optimal solution (those are dominated/tied by plain delete or delete+insert).
- **Savings formulation**: For target frequency k and active-letter set S: cost = n + |S|·k − 2·(kept chars) − 1·(moved-one-step chars). At an active letter i, kept = min(c[i], k) is always optimal (keeping saves 2 > 1 for moving in), and in-move fills remaining slots from the previous letter's surplus.
- **2-state DP**: Letter i's contribution depends only on whether letter i−1 is active (which determines avail_{i−1} = max(0, c[i−1]−k) if active, c[i−1] if inactive). So DP over 26 letters with prev-active flag is exact, O(26) per k.
- **k range**: k ∈ [1, n]; k > n is never better (for a single active letter, cost is nondecreasing in k once k ≥ n since kept and in-move are capped by available chars). k = 0 / all-inactive gives cost n, covered by the DP and the ans initialization.
- **Complexity**: O(26·n) ≈ 5.2·10⁵ elementary iterations — trivially fast for n ≤ 2·10⁴.
- **Verified examples**:
  - "acab" (c: a=2,b=1,c=1), k=2: a active (−2), c active with in-move 1 from b (−1) → 4−3 = **1** ✓
  - "wddw": k=2, d and w active → 4−4 = **0** ✓
  - "aaabc": k=2, a active (−2), b active with in-move 1 from a (−1), c active (0) → 5−3 = **2** ✓
  - Extra hand checks: "aaab" → 1 (move a→b giving a=2,b=2); "abc" → 0; "aab" → 1; "a"*3+"c" → 2 (matches delete+insert / 2-step move equivalence).

## worker: Verify the solution against all provided examples 
I verified the solution by tracing the DP against all provided examples and the requested edge cases, and re-checked the reduction proof.

**Provided examples:**
- `"acab"` (n=4, c: a=2,b=1,c=1), k=2: a active → kept=2, contrib −2, avail_a=0; b inactive; c active with prev(b) inactive → in=min(1, 1)=1, contrib 2−2−1=−1. Total = 4−3 = **1** ✓ (move b→c, giving a=2, c=2; equivalently delete one 'a').
- `"wddw"` (n=4, d=2, w=2), k=2: d active (−2), w active (−2, no usable surplus from neighbors). Total = 4−4 = **0** ✓.
- `"aaabc"` (n=5, a=3,b=1,c=1), k=2: a active kept=2, contrib −2, avail_a=1; b active in=min(1,1)=1, contrib −1; c active in=0, contrib 0. Total = 5−3 = **2** ✓.

**Additional edge cases traced:**
- Single distinct letter, `"zzz"` (n=3): k=3, z active kept=3, contrib 3−6=−3 → total 0 ✓. Also minimal length n=3 satisfied.
- Strings containing 'z': avail of z is never consumed (no letter 26), so z's surplus can only be deleted — correct since 'z' cannot increment. E.g., `"aazz"`: k=2, a active (−2), z active (−2) → 0 ✓. `"yz"*... ` e.g. `"yyz"` (n=3, y=2,z=1): k=2, y active kept=2 contrib −2, avail_y=0; z active kept=1 in=0 contrib 0 → total 3−2=1 (move y→z: y=1... actually delete one y → y=1,z=1, cost 1) ✓.
- k=n boundary: `"aaa"` → k=3 gives total 0 ✓. For k>n excluded: with a single active letter L and k≥n, kept=min(c[L],k)=c[L] and in-move ≤ n−c[L] are both capped, so cost(k)=n+k−2·c[L]−in is nondecreasing in k; hence k≤n suffices. ✓
- Minimal n=3, all distinct `"abc"`: k=1, a,b,c each active contrib 1−2=−1 → total 3−3=0 ✓.
- Two-step relocation equivalence: `"aaac"` (n=4, a=3,c=1): k=2 → a active (−2, avail_a=1), b inactive (avail_b=0), c active in=0 contrib 0 → total 2. Matches reality: move a→b→c costs 2 = delete a + insert c ✓.
- Chain moves: `"ab"`-style surplus passing, e.g. counts a=1,b=0,c=1 (n=2 hypothetical): a's char can move a→b (1) then b→c (1) = 2 = delete+insert; model gives same cost, so no optimum is missed (ties are fine).

**Reduction proof confirmation:**
1. Any relocation of a char from p to q (q>p) costs q−p via increments, or 2 via delete+insert. For q−p≥2, delete+insert ≤ increments; for q−p=1, increment (1) < delete+insert (2). Relocating backward is only possible via delete+insert. So every optimal solution has an equivalent one using only: keep (0), delete (1), insert (1), and 1-step increments (1) where the moved char fills a slot at the destination.
2. A moved char that is later deleted costs 2 ≥ plain delete (1); a moved char re-moved costs 2 = delete+insert. So WLOG moved chars are used exactly once at the destination.
3. Baseline cost n+|S|k (delete all, insert all final chars); kept char saves 2, moved char saves 1. At an active letter, keeping dominates moving-in (2>1), so kept=min(c[i],k) and in-move fills the rest from prev's surplus. Surplus avail_{i-1} depends only on prev's active flag → exact 2-state DP, O(26) per k, O(26n) total ≈ 5.2·10⁵ ops.

All traces match; complexity is well within limits for n ≤ 2·10⁴.
