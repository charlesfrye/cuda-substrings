"""These are tests that an FP32 FFT implementation should fail."""


def make_high_unicode_code_points_text():
    return "".join([chr(i) for i in range(20_000, 25_000)])


def test_large_encodings(implementation):
    large_text = make_high_unicode_code_points_text()
    large_pattern = "." + large_text[1:-1] + "."

    result = implementation(large_text, large_pattern)
    assert result == [0]


def test_hangul_matching(implementation):
    """이 테스트는 부분 문자열 매칭이 한글 문자에서 작동하는지 확인합니다.

    FFT 기반 알고리즘은 숫자 문제로 인해 실패할 것입니다. 한글 문자는 유니코드에서 높은 코드 포인트를
    가지고 있기 때문입니다. 특히 FFT 기반 알고리즘에서는 이러한 높은 코드 포인트들이 오버플로를
    발생시킬 수 있으며, 이는 매칭 오류를 유발할 수 있습니다.

    O(n²) 알고리즘은 이러한 문제에 민감하지 않지만, 더 복잡한 알고리즘, 특히 FFT와 같은 것들은
    숫자 크기와 직접적으로 연관된 문제를 겪을 가능성이 큽니다. 이는 특히 긴 문서나 텍스트에 대한
    매칭을 시도할 때 문제가 됩니다. 예를 들어, 아주 긴 한글 문서에서 작은 패턴을 찾는 경우,
    코드 포인트의 값이 비정상적으로 커져 매칭 오류가 발생할 수 있습니다.

    이 테스트에서는 문서 길이가 늘어나면서 이러한 문제가 더욱 두드러지게 나타날 가능성이 큽니다.
    FFT 기반 알고리즘은 이런 긴 텍스트에서 더 자주 실패할 것입니다. 한글의 유니코드 범위는
    대체로 매우 넓고, 이로 인해 FFT 기반 알고리즘의 실패 가능성이 더 높습니다."""

    docstring_text = test_hangul_matching.__doc__
    search_pattern = "이 테스트에서는 문서 길이가 늘어나면서 이러한 문제가 더욱 두드러지게 나타날 가능성이 큽니다"
    result = implementation(docstring_text, search_pattern)
    assert result == [424]


def test_emoji_matching(implementation):
    emoji_text = "".join([chr(i) for i in range(128_512, 128_516)])
    emoji_pattern = emoji_text[1:-1] + "."

    result = implementation(emoji_text, emoji_pattern)
    assert result == [1]
