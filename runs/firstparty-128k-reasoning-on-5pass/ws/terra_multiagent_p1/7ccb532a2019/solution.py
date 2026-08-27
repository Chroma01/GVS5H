class Solution:
    def makeStringGood(self, s: str) -> int:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1

        max_count = max(count)
        answer = len(s)

        for freq in range(1, max_count + 1):
            # dp0: minimum cost through current letter if it is absent.
            # dp1: minimum cost through current letter if it occurs `freq` times.
            dp0 = count[0]
            dp1 = abs(count[0] - freq)

            for i in range(1, 26):
                current_count = count[i]
                previous_count = count[i - 1]

                cur0_base = current_count
                cur1_base = abs(current_count - freq)

                # If previous letter was removed, all of its original
                # occurrences are available as conversion surplus.
                previous_surplus_removed = previous_count

                # If it was retained, only occurrences beyond `freq`
                # can be converted to the current letter.
                previous_surplus_kept = max(0, previous_count - freq)

                deficit = max(0, freq - current_count)

                new0 = min(dp0, dp1) + cur0_base

                new1 = min(
                    dp0 + cur1_base
                    - min(previous_surplus_removed, deficit),
                    dp1 + cur1_base
                    - min(previous_surplus_kept, deficit),
                )

                dp0, dp1 = new0, new1

            answer = min(answer, dp0, dp1)

        return answer