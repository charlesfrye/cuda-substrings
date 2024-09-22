# Substring Matching with Fast Fourier Transforms in O(n log n)

This repo demonstrates how to use FFTs to perform substring matching in O(n log n) time.

The base implementation is in pure Python.

It includes a NumPy implementation
and a CuPy implementation that runs on NVIDIA GPUs.

In our testing, on a beefy H100 node on Modal,
the base implementation achieved ~50 OPS as measured by `pytest-benchmark`
for input strings of size `65_536 == 2 ** 16`
(roughly the length of a Shakespeare play).
with single matches of size roughly `4_096 == 2 ** 12`.

The NumPy implementation was slower than the base implementation by a factor of ~3,
or ~15 OPS.
This was only intended as a reference implementation for building the CuPy implementation, so no further optimization was attempted.

The initial CuPy implemementation was faster than the base implementation by a factor of ~1.5,
or ~80 OPS.
Profiling showed that the CuPy implementation's runtime was dominated by overhead
from the conversion of Python strings into ints for the FFT.
Reading the string into CuPy from a `utf32-le` buffer relieved this bottleneck
and boosed the OPS to >500, or >10x the speed of the base implementation.

For larger strings, the superior asymptotics of the FFT-based approach
become more apparent.
The base implementation's OPS drops to <4 for input strings of size `1_048_576 == 2 ** 20`, a ~10x slowdown for a 4x increase in input size.
That's a string roughly the length of the _Harry Potter and the Deathly Hallows_.
Meanwhile, the CuPy implementation's OPS drops to ~250, a 2x slowdown for a 4x increase in input size.


## Usage

The `src.ci::benchmark` task runs benchmarking on [Modal](https://modal.com).
When executed via the `ci` file's `local-entrypoint`,
it saves an SVG file with a `py-spy` flame graph to `/tmp`.

```bash
modal run src.ci --impl simple
modal run src.ci --impl numpy-fft
modal run src.ci --impl cupy-fft
```
