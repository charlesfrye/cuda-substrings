# Substring Matching with Fast Fourier Transforms in O(n log n)

This repo demonstrates how to use FFTs to perform substring matching in O(n log n) time.

The base implementation is in pure Python.

It includes a NumPy implementation
and a CuPy implementation that runs on NVIDIA GPUs.

## Usage

The `src.ci::benchmark` task runs benchmarking.
It returns an SVG file with a `py-spy` flame graph.

```bash
modal run src.ci::benchmark --impl simple
modal run src.ci::benchmark --impl numpy-fft
modal run src.ci::benchmark --impl cupy-fft
```
