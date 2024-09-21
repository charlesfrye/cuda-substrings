# Substring Matching with Fast Fourier Transforms in O(n log n)

This repo demonstrates how to use FFTs to perform substring matching in O(n log n) time.

The base implementation is in pure Python.

It includes a NumPy implementation
and a CuPy implementation that runs on NVIDIA GPUs.

In our testing,
the NumPy implementation was slower than the base implementation.

The CuPy implemementation was faster than the base implementation by a factor of 8
for input strings of size `65_536 == 2 ** 16`
with single matches of size roughly `4_096 == 2 ** 12`.

## Usage

The `src.ci::benchmark` task runs benchmarking on [Modal](https://modal.com).
When executed via the `ci` file's `local-entrypoint`,
it saves an SVG file with a `py-spy` flame graph to `/tmp`.

```bash
modal run src.ci --impl simple
modal run src.ci --impl numpy-fft
modal run src.ci --impl cupy-fft
```
