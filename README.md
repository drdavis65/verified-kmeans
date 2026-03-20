# Verified K-Means Clustering in Dafny

A formally verified implementation of Lloyd's k-means algorithm with deterministic
farthest-first centroid initialization, written in Dafny.

## Prerequisites

- [Dafny](https://github.com/dafny-lang/dafny) 4.x — `dafny` must be on your PATH
- Python 3.8+ (for visualization and test generation only)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Verifying the code

To check that all proofs pass:

```bash
dafny verify kmeans.dfy
```

Expected output: all methods verify with no errors.

## Running the code

### Option 1: Dafny run (quickest)

The test harness `KMeansTest.dfy` calls `MakePoints()` from `data.dfy`, runs
`DeterministicKMeansInitCentroids` and `KMeans`, and prints the convergence flag,
per-point labels, and final centroids.

```bash
python3 gen_dafny_test.py
dafny run KMeansTest.dfy --allow-warnings
```

Sample output:
```
initial centroids:
  cluster 0: 2.631858338 0.6893649044 
  cluster 1: -0.7300001121 6.2545627227 
  cluster 2: -2.5271193606 1.3731111646 
converged: true
labels: 0 1 0 1 1 1 2 1 0 1 ...
centroids:
  cluster 0: (738832643126.0 / 330000000000.0) (448776023750.0 / 330000000000.0) 
  cluster 1: 0.894123123640625 4.340318742609375 
  cluster 2: (-552015330439.0 / 350000000000.0) (998870051865.0 / 350000000000.0) 
```

### Option 2: Python visualization

First, compile the Dafny code to Python:

```bash
dafny build KMeansTest.dfy --target py --output kmeans_out --allow-warnings
```

Then run the visualization script:

```bash
python3 visualize.py
```

This generates a plot comparing the Dafny k-means result against the raw data.
To save the plot to a file instead of displaying it:

```bash
python3 visualize.py --output ../Figure_1.png
```

Key options for `visualize.py`:

| Flag | Default | Description |
|------|---------|-------------|
| `--k N` | 3 | Number of clusters |
| `--n-samples N` | 100 | Number of points |
| `--max-iter N` | 100 | Max k-means iterations |
| `--init dafny\|first-k` | `dafny` | Initialization strategy |
| `--random-state N` | 0 | Random seed for data generation |
| `--output FILE` | (show) | Save plot to file |

## Generating a new dataset

`KMeansTest.dfy` is a static harness — only `data.dfy` changes when you use different data.
To regenerate `data.dfy` with different parameters:

```bash
python3 gen_dafny_test.py <k> <max_iter> [options]
```

Example — 5 clusters, 200 points:

```bash
python3 gen_dafny_test.py 5 100 --n-samples 200 --random-state 42
dafny run KMeansTest.dfy --allow-warnings
```

Options for `gen_dafny_test.py`:

| Flag | Default | Description |
|------|---------|-------------|
| `--n-samples N` | 100 | Number of points |
| `--n-features N` | 2 | Dimensions per point |
| `--random-state N` | 0 | Random seed |
| `--output FILE` | data.dfy | Output filename |

## File overview

| File | Description |
|------|-------------|
| `kmeans.dfy` | Verified core: distance, assign, update, convergence, deterministic init |
| `KMeansTest.dfy` | Static test harness with runtime `expect` checks; never needs editing |
| `data.dfy` | Generated dataset (`K`, `MaxIter`, `MakePoints()`); regenerate with `gen_dafny_test.py` |
| `gen_dafny_test.py` | Generates a new `data.dfy` from `sklearn.make_blobs` data |
| `kmeans_out-py/visualize.py` | Runs compiled Dafny module and plots results |
| `kmeans.py` | Unverified Python re-implementation (for cross-validation) |
