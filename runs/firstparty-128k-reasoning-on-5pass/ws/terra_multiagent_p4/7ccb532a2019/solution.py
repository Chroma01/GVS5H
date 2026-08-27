class Solution:
    def makeStringGood(self, s: str) -> int:
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1

        n = len(s)
        answer = n  # Delete every character, if needed.

        for k in range(1, n + 1):
            # Minimum cost after processing the previous letter, where it is
            # respectively absent or present exactly k times in the target.
            dp0 = counts[0]
            dp1 = abs(counts[0] - k)

            for i in range(1, 26):
                cur_absent = counts[i]
                cur_present = abs(counts[i] - k)

                # Current letter is absent, so all current occurrences are
                # deleted and no useful incoming conversion can be used.
                next0 = min(dp0, dp1) + cur_absent

                deficit = max(0, k - counts[i])

                # If previous letter is absent, all of its originals are
                # surplus and may be changed into the current letter.
                save_from_absent = min(counts[i - 1], deficit)

                # If previous letter is present k times, only its excess is
                # available for conversion to the current letter.
                save_from_present = min(
                    max(0, counts[i - 1] - k),
                    deficit
                )

                next1 = min(
                    dp0 + cur_present - save_from_absent,
                    dp1 + cur_present - save_from_present
                )

                dp0, dp1 = next0, next1

            answer = min(answer, dp0, dp1)

        return answer