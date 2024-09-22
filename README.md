# Substring Matching with Fast Fourier Transforms in O(n log n)

This repo demonstrates how to use FFTs to perform substring matching in O(n log n) time.

The base implementation is in pure Python.

It includes a NumPy implementation
and a CuPy implementation that runs on NVIDIA GPUs.

In our testing, on a beefy H100 node on Modal,
the base implementation achieved ~50 OPS as measured by `pytest-benchmark`
for input strings of size `65_536 == 2 ** 16`
with single matches of size roughly `4_096 == 2 ** 12`.

The NumPy implementation was slower than the base implementation by a factor of ~3,
or ~15 OPS.

The CuPy implemementation was faster than the base implementation by a factor of ~1.5,
or ~80 OPS.
Overhead was dominated by the conversion of Python

## Usage

The `src.ci::benchmark` task runs benchmarking on [Modal](https://modal.com).
When executed via the `ci` file's `local-entrypoint`,
it saves an SVG file with a `py-spy` flame graph to `/tmp`.

```bash
modal run src.ci --impl simple
modal run src.ci --impl numpy-fft
modal run src.ci --impl cupy-fft
```
