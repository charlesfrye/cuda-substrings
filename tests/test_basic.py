def test_exact_match(implementation):
    assert implementation("abcde", "abc") == [0]


def test_multiple_matches(implementation):
    assert implementation("abcabcabc", "abc") == [0, 3, 6]


def test_no_match(implementation):
    assert implementation("abcde", "xyz") == []


def test_pattern_with_wildcard(implementation):
    assert implementation("abcde", "a.c") == [0]


def test_empty_pattern(implementation):
    assert implementation("abcde", "") == [0, 1, 2, 3, 4]


def test_pattern_longer_than_text(implementation):
    assert implementation("abc", "abcd") == []


def test_text_with_pattern_char(implementation):
    assert implementation("a.cdef", "abc") == []


def test_empty_text(implementation):
    assert implementation("", "abc") == []
