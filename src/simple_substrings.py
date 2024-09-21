def find_substrings(text: str, pattern: str) -> list[int]:
    """The usual way to find matches for the pattern p in a string of text t is quadratic:
    for each position in the string, loop through the pattern and check whether the pattern is present at that position.

    We also allow for single-character wildcards with the "." character.


    >>> find_substrings("abra kadabra", "abra")
    [0, 8]

    >>> find_substrings("abc", "b.")
    [1]

    >>> find_substrings("team", "i")
    []
    """
    n, m, matches = len(text), len(pattern), []
    if not m:  # empty string matches everywhere
        return list(range(n))
    for i in range(n - m + 1):
        for j in range(m):
            if pattern[j] not in (".", text[i + j]):
                break
        else:  # if inner for-loop reaches end, we matched
            matches.append(i)
    return matches
