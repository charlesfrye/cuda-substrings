import numpy as np


def char_to_num(c):
    return ord(c) if c != "." else 0


def checkcubesum(pattern_n):
    """Compute a check value for the pattern by summing the cube of each character's numerical encoding."""
    return np.sum(pattern_n**3)


def find_substrings(text: str, pattern: str) -> list[int]:
    """Substring matching using the Cliffords' approach (convolution).

    Args:
    - text: Input text to search in.
    - pattern: The pattern to search for, may contain wildcards ('.').

    Returns:
    - A list of indices where the pattern matches in the text.

    >>> find_substrings("abra kadabra", "abra")
    [0, 8]

    >>> find_substrings("abc", "b.")
    [1]

    >>> find_substrings("team", "i")
    []
    """
    text_len, pattern_len = len(text), len(pattern)

    if pattern_len > text_len:
        return []  # no match possible
    if pattern_len == 0:  # all positions match
        return list(range(text_len))

    # convert pattern to numeric encoding
    pattern_n = np.array([char_to_num(c) for c in pattern])

    # compute p^2 and sum(p^3) aka checkcubesum
    pattern_num_squared = pattern_n**2
    pattern_check_value = checkcubesum(pattern_n)

    # reverse the pattern before convolution so that we compute correlation
    pattern_reversed = pattern_n[::-1]
    pattern_reversed_squared = pattern_num_squared[::-1]

    text_num = np.array([char_to_num(c) for c in text])
    text_num_squared = text_num**2

    matches, size = [], pattern_len

    # step through n/m chunks of size m
    for index in range(0, text_len, size + 1):
        chunk_size = min(  # double size to get a sliding window
            size * 2, text_len - index
        )
        text_num_chunk = text_num[index : index + chunk_size]
        text_num_chunk_squared = text_num_squared[index : index + chunk_size]

        # two convolutions: t^2 (*) p and t (*) p^2
        pt2 = fast_convolve(text_num_chunk_squared, pattern_reversed)
        p2t = fast_convolve(text_num_chunk, pattern_reversed_squared)

        # D' = p^3 - 2t^2*p + p*t^2
        sum_of_squared_diffs = pattern_check_value - 2 * p2t + pt2

        matches_in_chunk = (
            np.where(sum_of_squared_diffs[size - 1 : chunk_size] == 0)[0] + index
        )

        matches.extend(list(matches_in_chunk))

    return matches


def fast_convolve(a, b):
    """Perform convolution using FFT, O(n log n)."""
    n = len(a) + len(b) - 1
    n_fft = 2 ** compute_log(n)

    fft_a = np.fft.fft(a, n_fft)
    fft_b = np.fft.fft(b, n_fft)

    # pointwise multiplication in frequency domain is convolution in time domain
    result_fft = fft_a * fft_b
    result = np.fft.ifft(result_fft).real
    return np.round(result).astype(int)


# pad to a power of 2 for Cooley-Tukey FFT
def compute_log(n):
    """Compute log base 2 of the next power of 2 greater than or equal to n."""
    return int(np.ceil(np.log2(n)))
