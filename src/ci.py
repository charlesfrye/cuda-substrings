from pathlib import Path

import modal

ROOT_PATH = Path(__file__).parent.parent

image = (
    modal.Image.from_registry("nvidia/cuda:12.4.0-devel-ubuntu22.04", add_python="3.11")
    .entrypoint([])
    .copy_local_file("requirements.txt")
    .pip_install_from_requirements(ROOT_PATH / "requirements.dev.txt")
    .copy_local_file("conftest.py")
    .copy_local_file("pytest.ini")
)

app = modal.App("cuda-substrings-ci", image=image)

# mount: add local files to the remote container
tests = modal.Mount.from_local_dir(ROOT_PATH / "tests", remote_path="/root/tests")
perf_volume = modal.Volume.from_name("fft-perf", create_if_missing=True)
volume_dir = Path("/root/perf")


@app.function(gpu="any", mounts=[tests])
def pytest(impl: str = None, run_hard: bool = False):
    import subprocess

    subprocess.run(
        ["pytest", "-vs"]
        + (["--impl", impl] if impl else [])
        + (["--run-hard"] if run_hard else []),
        check=True,
        cwd="/root",
    )


@app.function(
    gpu="h100", mounts=[tests], volumes={volume_dir: perf_volume}, cloud="oci"
)
def benchmark(strlen: int = None, impl: str = None):
    import os
    import subprocess

    impl = impl or "simple"
    strlen = strlen or 2**20
    output_dir = volume_dir / impl / str(strlen).zfill(10)
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["py-spy", "record", "-o", output_dir / "trace.svg", "--"]
        + ["pytest"]
        + ["--impl", impl]
        + ["--benchmark-enable"]
        + [f"--benchmark-storage={output_dir}", "--benchmark-autosave"]
        + ["tests/test_perf.py"],
        check=False,
        cwd="/root",
        env=os.environ | {"CUDA_SS_STRINGLEN": str(strlen)},
    )

    return Path(output_dir / "trace.svg").read_bytes()


@app.local_entrypoint()
def main(impl: str = None, strlen_min: int = None, strlen_max: int = None):
    if strlen_min is None:
        strlen_min = 10
    if strlen_max is None:
        strlen_max = 20
    if impl is None:
        impl = "simple"
    strlens = [2**strlen for strlen in range(strlen_min, strlen_max + 1)]
    results = []
    for strlen in strlens:
        handle = benchmark.spawn(strlen=strlen, impl=impl)
        results += [{"strlen": strlen, "handle": handle}]

    for result in results:
        bytes_svg = result["handle"].get()
        with open(Path("/tmp") / f"{impl}-{result['strlen']}-results.svg", "wb") as f:
            f.write(bytes_svg)

        print(f.name)
