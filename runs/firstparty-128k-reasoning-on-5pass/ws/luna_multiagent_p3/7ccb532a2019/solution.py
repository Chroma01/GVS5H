class Solution:
    def makeStringGood(self, s: str) -> int:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1

        n = len(s)
        answer = n

        for k in range(1, n + 1):
            # Costs after processing the current prefix:
            # absent_cost: current letter is absent
            # kept_cost: current letter occurs exactly k times
            absent_cost = counts[0]
            kept_cost = abs(counts[0] - k)

            for i in range(1, 26):
                c = counts[i]

                # Do not retain the current letter.
                new_absent = min(absent_cost, kept_cost) + c

                # Retain the current letter with frequency k, without
                # using a change from the previous letter.
                node_cost = abs(c - k)
                new_kept = min(
                    absent_cost + node_cost,
                    kept_cost + node_cost,
                )

                # A surplus occurrence of the previous letter can be
                # changed directly into a missing occurrence of this
                # letter, saving one operation over delete + insert.
                deficit = max(k - c, 0)
                if deficit:
                    # Previous letter absent: all of its original
                    # occurrences are available as surplus.
                    saving = min(counts[i - 1], deficit)
                    new_kept = min(
                        new_kept,
                        absent_cost + node_cost - saving,
                    )

                    # Previous letter retained: only its surplus can move.
                    surplus = max(counts[i - 1] - k, 0)
                    saving = min(surplus, deficit)
                    new_kept = min(
                        new_kept,
                        kept_cost + node_cost - saving,
                    )

                absent_cost, kept_cost = new_absent, new_kept

            # A nonempty good string is represented because the last
            # letter is retained in this state.
            answer = min(answer, kept_cost)

        return answer