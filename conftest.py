import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--impl",
        action="store",
        default="simple",
        help="Implementation to use: simple, numpy-fft, cuda-fft",
    )
    parser.addoption(
        "--run-hard", action="store_true", default=False, help="run hard tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-hard"):
        return
    skip_slow = pytest.mark.skip(reason="need --run-hard option to run")
    for item in items:
        if "hard" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def implementation(request):
    impl_type = request.config.getoption("--impl")

    if impl_type == "simple":
        from src.simple_substrings import find_substrings as implementation
    elif impl_type == "numpy-fft":
        from src.numpy_fft_substrings import find_substrings as implementation
    elif impl_type == "cupy-fft":
        from src.cupy_fft_substrings import find_substrings as implementation
    elif impl_type == "cuda-fft":
        raise NotImplementedError("CUDA FFT implementation not yet available")
    else:
        raise ValueError(f"Unknown implementation: {impl_type}")
    return implementation
