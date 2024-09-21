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
def pytest(impl: str = None):
    import subprocess

    subprocess.run(
        ["pytest", "-vs"] + ["--impl", impl] if impl else [], check=True, cwd="/root"
    )


@app.function(gpu="h100", mounts=[tests], volumes={volume_dir: perf_volume})
def benchmark(impl: str = None):
    import subprocess

    impl = impl or "simple"
    output_dir = volume_dir / impl
    output_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["py-spy", "record", "-o", volume_dir / impl / "results.svg", "--"]
        + ["pytest"]
        + ["--impl", impl]
        + ["--benchmark-enable"]
        + ["tests/test_perf.py"],
        check=False,
        cwd="/root",
    )

    return Path(output_dir / "results.svg").read_bytes()


@app.local_entrypoint()
def main(impl: str = None):
    bytes_svg = benchmark.remote(impl)
    with open(Path("/tmp") / f"{impl}-results.svg", "wb") as f:
        f.write(bytes_svg)

    print(f.name)
