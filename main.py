ALPHABET = 'abcdefghijklmnopqrstuvwxyz '


def caesar(text: str, k: int) -> str:
    text = text.lower()

    result = ""
    for letter in text:
        new_index = ALPHABET.find(letter) + k
        result += ALPHABET[new_index % 27]
    return result


class FrequencyAnalysis:
    def find_caesar_key(self, encoded_text: str) -> int:

        encoded_text = encoded_text.lower()

        probs = list(map(float, "0.0651738 0.0124248 0.0217339 0.0349835 0.1041442 0.0197881 0.0158610 0.0492888 0.0558094 0.0009033 0.0050529 0.0331490 0.0202124 0.0564513 0.0596302 0.0137645 0.0008606 0.0497563 0.0515760 0.0729357 0.0225134 0.0082903 0.0171272 0.0013692 0.0145984 0.0007836 0.1918182".split()))
        letter_probabilities = {ALPHABET[i]: probs[i] for i in range(27)}

        scores = []
        for k in range(27):
            attempt = caesar(encoded_text, -k)

            letter_counts = {}
            for letter in ALPHABET:
                letter_counts[letter] = 0
            for letter in attempt:
                letter_counts[letter] += 1

            score = 0
            for letter in letter_counts:
                o_i = letter_counts[letter]
                e_i = len(encoded_text) * letter_probabilities[letter]
                score += (o_i - e_i) ** 2 / e_i
            scores.append(score)

        most_likely_key = 0
        lowest_score = scores[0]
        for i, score in enumerate(scores):
            if score < lowest_score:
                lowest_score = score
                most_likely_key = i
        return most_likely_key

    def decrypt_by_frequency(self, encoded_text: str) -> str:
        likely_key = self.find_caesar_key(encoded_text)
        decrypted = caesar(encoded_text, likely_key * -1)

        return decrypted
