import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--impl",
        action="store",
        default="simple",
        help="Implementation to use: simple, numpy-fft, cuda-fft",
    )


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
