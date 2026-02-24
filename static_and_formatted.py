# THIS VERSION IS FORMATTED TO MATCH THAT WHICH IS REQUIRED BY THE INSTRUCTIONS


# 1 -----

ALPHABET = 'abcdefghijklmnopqrstuvwxyz '
def caesar(text: str, k: int) -> str:
    """
    Adds a certain step to each letter of a string.

    :param text: The string for which the caesar cipher should be applied to.
    :param k: The step for each letter.
    :return: The altered string.
    """
    text = text.lower()

    result = ""
    for letter in text:
        new_index = ALPHABET.find(letter) + k
        result += ALPHABET[new_index % 27]
    return result

# End of 1 -----


# 2 ------

def calculate_probability_score(text: str) -> float:
    """
    Calculate the probability score for a string.

    :param text: The text for which to calculate the probability score.
    :return: The score calculated for the input text.
    """
    probs = list(map(float,
                     "0.0651738 0.0124248 0.0217339 0.0349835 0.1041442 0.0197881 0.0158610 0.0492888 0.0558094 0.0009033 0.0050529 0.0331490 0.0202124 0.0564513 0.0596302 0.0137645 0.0008606 0.0497563 0.0515760 0.0729357 0.0225134 0.0082903 0.0171272 0.0013692 0.0145984 0.0007836 0.1918182".split()))
    letter_probabilities = {ALPHABET[i]: probs[i] for i in range(27)}

    letter_counts = {}
    for letter in ALPHABET:
        letter_counts[letter] = 0
    for letter in text:
        letter_counts[letter] += 1

    score = 0
    for letter in letter_counts:
        o_i = letter_counts[letter]
        e_i = len(text) * letter_probabilities[letter]
        score += (o_i - e_i) ** 2 / e_i

    return score

def find_caesar_key(encodedText: str) -> int:
    """
    Attempt to find the most likely caesar key for a string using frequency analysis.

    :param encoded_text: The encoded text for which the most likely caesar key should be found.
    :return: The most likely caesar key for that text.
    """
    encodedText = encodedText.lower()

    scores = []
    for k in range(27):
        attempt = caesar(encodedText, -k)

        score = calculate_probability_score(attempt)

        scores.append(score)

    most_likely_key = 0
    lowest_score = scores[0]
    for i, score in enumerate(scores):
        if score < lowest_score:
            lowest_score = score
            most_likely_key = i
    return most_likely_key

def decrypt_by_frequency(encoded_text: str) -> str:
    """
    Attempt to decrypt a caesar encoded string by finding its most likely caesar key
    and then decrypting it.

    :param encoded_text: The caesar encoded text for which to try and decrypt.
    :return: The estimated decrypted text.
    """
    likely_key = find_caesar_key(encoded_text)
    decrypted = caesar(encoded_text, likely_key * -1)

    return decrypted

# End of 2 -----


# 3 -----

import math
def vigenere(plaintext: str, key: str, decrypt: bool = False) -> str:
    """
    Apply a vigenere cipher to a string using a certain key.

    :param plaintext: The text for which the vigenere cipher should be applied.
    :param key: The vigenere keyword.
    :param decrypt: Should the key be used to decrypt the text instead of encrypt it?
    :return: The newly encrypted/decrypted string.
    """
    plaintext = plaintext.lower()

    # Repeats the keyword to match the length of the plaintext
    wrapped_key = \
        key * math.floor(len(plaintext) / len(key)) + key[:len(plaintext) % len(key)]

    ciphertext = ""
    for index, letter in enumerate(plaintext):
        key_equivalent = wrapped_key[index]
        shift = ALPHABET.find(key_equivalent)

        if decrypt:
            new_letter = ALPHABET[(ALPHABET.find(letter) - shift) % len(ALPHABET)]
        else:
            new_letter = ALPHABET[(ALPHABET.find(letter) + shift) % len(ALPHABET)]

        ciphertext += new_letter
    return ciphertext

# End of 3 -----


# 4 -----

def decrypt_vigenere(ciphertext, key) -> str:
    """
    Vigenere() wrapper for decrypting text.

    :param ciphertext: The encrypted text.
    :param key: The decryption key.
    :return: The decrypted text.
    """
    plaintext = vigenere(ciphertext, key, decrypt=True)
    return plaintext

# End of 4 -----


# 5 -----

def ioc(s: str) -> float:
    """
    Calculate the index of coincidence for a given string.

    :param s: The text for which the IOC should be calculated.
    :return: The index of coincidence for the string.
    """
    text = s.lower()
    letter_counts = {}

    for letter in ALPHABET:
        letter_counts[letter] = 0
    for letter in text:
        letter_counts[letter] += 1

    numerator = 0
    for letter in ALPHABET:
        numerator += letter_counts[letter] * (letter_counts[letter] - 1)
    denominator = len(text) * (len(text) - 1)

    index_of_coincidence = numerator / denominator
    return float(index_of_coincidence)

# End of 5 -----


# 6 -----

IOC_ENGLISH = 0.079
def estimated_key_length(c: str) -> float:
    """
    Estimate the key length of a given vigenere-encrypted string.

    :param c: The vigenere-encrypted string.
    :return: The estimated key length of the given string.
    """
    numerator = IOC_ENGLISH - 1/27
    denominator = ioc(c) - 1/27
    estimate = numerator/denominator

    return float(estimate)

# End of 6 -----


# 7 -----

def break_vigenere(ciphertext: str) -> None:
    """
    Attempt to break a vigenere-encrypted string using
    Index of Coincidence and print the result.

    :param ciphertext: The vigenere-encrypted text.
    """
    estimated_key_length_value = round(estimated_key_length(ciphertext))

    potential_keys = {}
    for potential_key_length in range(estimated_key_length_value - 4, estimated_key_length_value + 4):

        if potential_key_length < 1:
            continue

        potential_key = ""
        for i in range(potential_key_length):
            sliced = "".join(ciphertext[i::potential_key_length])

            shift_index = find_caesar_key(sliced)
            potential_key += ALPHABET[shift_index]

        plaintext = decrypt_vigenere(ciphertext, potential_key)
        score = calculate_probability_score(plaintext)

        potential_keys[str(potential_key)] = (plaintext, score)


    most_likely_key = list(potential_keys.keys())[0]
    most_likely_key_values = potential_keys[most_likely_key]
    lowest_score = most_likely_key_values[1]

    for potential_key, values in potential_keys.items():
        if values[1] < lowest_score:
            lowest_score = values[1]
            most_likely_key = potential_key
            most_likely_key_values = values

    print(f"Potential key: {most_likely_key}\nCorresponding plaintext: {most_likely_key_values[0]}")

# End of 7 -----
