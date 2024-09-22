from pathlib import Path

import modal

app = modal.App("cuda-substring-demo")

ROOT_PATH = Path(__file__).parent

image = (
    modal.Image.from_registry("nvidia/cuda:12.4.0-devel-ubuntu22.04", add_python="3.11")
    .entrypoint([])
    .pip_install_from_requirements(ROOT_PATH / "requirements.txt")
    .copy_local_dir(ROOT_PATH / "src", "/root/src")
)


@app.function(gpu="a10g", image=image)
def run(string, pattern):
    from src.cupy_fft_substrings import find_substrings

    indices = find_substrings(string, pattern)
    print(indices)
    return indices
