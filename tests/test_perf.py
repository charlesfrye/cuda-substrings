import random
import string

import pytest


def on_really_long_ascii(implementation, inpt):
    random_string, random_match, random_index = (
        inpt["random_string"],
        inpt["random_match"],
        inpt["random_index"],
    )
    result = implementation(random_string, random_match)
    assert result[0] == random_index


@pytest.fixture
def inpt():
    random_string = "".join(random.choices(string.ascii_lowercase, k=2**16))
    random_index = random.randint(len(random_string) // 4, len(random_string) // 2)
    length = (
        len(random_string) // 2
    )  # long sequence -> high probability of only one match

    random_match = random_string[random_index : random_index + length]
    random_match = "".join(
        "." if random.random() > 0.5 else random_char for random_char in random_match
    )

    return {
        "random_string": random_string,
        "random_match": random_match,
        "random_index": random_index,
    }


def test_performance(benchmark, implementation, inpt):
    benchmark(on_really_long_ascii, implementation, inpt)
