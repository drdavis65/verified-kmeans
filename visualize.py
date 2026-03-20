#!/usr/bin/env python3
"""
visualize.py
Runs the Dafny-compiled kmeans and visualizes the results.

Usage:
  python visualize.py [options]

All options must match what you passed to gen_dafny_test.py so the same
data is reproduced:
  --k N               Number of clusters          (default: 3)
  --max-iter N        Max kmeans iterations        (default: 100)
  --n-samples N       Points to generate           (default: 100)
  --n-features N      Dimensions (only 2 plots)    (default: 2)
  --center-box LO HI  Bounding box for centers     (default: -10 10)
  --cluster-std S     Cluster spread               (default: 1.0)
  --random-state N    Random seed                  (default: 0)
  --output FILE       Save plot to file instead of showing interactively
"""

import sys
import os
import argparse
import numpy as np

# add kmeans_out-py/ to the path so module_ can be imported from any working directory
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "kmeans_out-py"))


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--k",            type=int,   default=3)
    p.add_argument("--max-iter",     type=int,   default=100)
    p.add_argument("--init",         choices=["dafny", "first-k"], default="dafny",
                   help="Centroid init: 'dafny' calls DeterministicKMeansInitCentroids, "
                        "'first-k' uses the first k points (default: dafny)")
    p.add_argument("--n-samples",    type=int,   default=100)
    p.add_argument("--n-features",   type=int,   default=2)
    p.add_argument("--center-box",   type=float, default=(-10, 10), nargs=2, metavar=("LO", "HI"))
    p.add_argument("--cluster-std",  type=float, default=1.0)
    p.add_argument("--random-state", type=int,   default=0)
    p.add_argument("--output",       default=None, metavar="FILE",
                   help="Save plot to this file (png/pdf/svg) instead of displaying")
    return p.parse_args()


# ── Dafny interop helpers ─────────────────────────────────────────────────────

def to_dafny_array(points_list):
    """Convert a list-of-lists of floats to a _dafny.Array of _dafny.Arrays of BigRationals."""
    try:
        import _dafny
    except ImportError:
        sys.exit("Error: _dafny module not found. Make sure you're running from the "
                 "directory that contains the Dafny-compiled output (kmeans_out-py/).")

    n, d = len(points_list), len(points_list[0])
    outer = _dafny.Array(_dafny.Array(None, 0), n)
    for i, pt in enumerate(points_list):
        inner = _dafny.Array(_dafny.BigRational(), d)
        for j, v in enumerate(pt):
            # Convert float → exact rational via string to avoid float rounding
            inner[j] = float_to_bigrat(v)
        outer[i] = inner
    return outer


def float_to_bigrat(v):
    """Convert a Python float to _dafny.BigRational without going through inexact repr."""
    import _dafny
    # Express as integer numerator / 10^10 to preserve 10 decimal places
    scaled = round(v * 1e10)
    return _dafny.BigRational(scaled, 10**10)


def dafny_array_to_list(arr):
    """Flatten a 1-D _dafny.Array to a plain Python list."""
    return [arr[i] for i in range(arr.length(0))]


def dafny_bigrat_to_float(r):
    """Convert _dafny.BigRational to Python float."""
    return float(r)


# ── Data generation ───────────────────────────────────────────────────────────

def make_data(args):
    try:
        from sklearn.datasets import make_blobs
    except ImportError:
        sys.exit(f"scikit-learn not found. Run: {sys.executable} -m pip install scikit-learn")

    X, y_true = make_blobs(
        n_samples=args.n_samples,
        centers=args.k,
        n_features=args.n_features,
        center_box=tuple(args.center_box),
        cluster_std=args.cluster_std,
        random_state=args.random_state,
    )
    return X, y_true  # numpy arrays


# ── Run Dafny kmeans ──────────────────────────────────────────────────────────

def run_dafny_kmeans(X, args):
    try:
        import module_ as dafny_module
    except ImportError:
        sys.exit("Error: module_.py not found. Make sure kmeans_out.py and kmeans_out-py/ "
                 "are in the current directory.\n"
                 "Build with: dafny build KMeansTest.dfy --input kmeans.dfy --target py --output kmeans_out")

    points_list = X.tolist()
    dafny_points = to_dafny_array(points_list)

    if args.init == "dafny":
        dafny_centroids = dafny_module.default__.DeterministicKMeansInitCentroids(
            dafny_points, args.k
        )
    else:
        dafny_centroids = to_dafny_array(points_list[:args.k])  # first-k initialisation

    # Capture initial centroids as numpy before kmeans mutates state
    k0 = dafny_centroids.length(0)
    d0 = dafny_centroids[0].length(0)
    init_centroids = np.array([
        [dafny_bigrat_to_float(dafny_centroids[c][j]) for j in range(d0)]
        for c in range(k0)
    ])

    out_centroids, out_labels, converged = dafny_module.default__.KMeans(
        dafny_points, args.k, dafny_centroids, args.max_iter
    )

    # Convert results back to numpy
    labels = np.array(dafny_array_to_list(out_labels), dtype=int)

    k = out_centroids.length(0)
    d = out_centroids[0].length(0)
    centroids = np.array([
        [dafny_bigrat_to_float(out_centroids[c][j]) for j in range(d)]
        for c in range(k)
    ])

    return labels, centroids, init_centroids, converged


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot(X, labels, centroids, init_centroids, converged, args):
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        sys.exit(f"matplotlib not found. Run: {sys.executable} -m pip install matplotlib")

    d = X.shape[1]
    if d < 2:
        sys.exit("Need at least 2 features to plot.")

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    cmap = plt.get_cmap("tab10")
    status = "converged" if converged else f"stopped at {args.max_iter} iterations"

    # ── left: Dafny kmeans result ─────────────────────────────────────────────
    ax = axes[0]
    for c in range(args.k):
        mask = labels == c
        ax.scatter(X[mask, 0], X[mask, 1], s=30, alpha=0.7,
                   color=cmap(c), label=f"cluster {c}")
    ax.scatter(init_centroids[:, 0], init_centroids[:, 1],
               s=150, marker="o", facecolors="none", edgecolors="black",
               linewidths=1.5, zorder=4, label="initial centroids")
    ax.scatter(centroids[:, 0], centroids[:, 1],
               s=100, marker="o", c="black", zorder=5, label="final centroids")
    init_label = "det. init" if args.init == "dafny" else "first-k init"
    ax.set_title(f"Dafny k-means  (k={args.k}, {init_label}, {status})")
    ax.set_xlabel("feature 0")
    ax.set_ylabel("feature 1")
    ax.legend(fontsize=8)

    # ── right: raw points, no coloring ───────────────────────────────────────
    ax = axes[1]
    ax.scatter(X[:, 0], X[:, 1], s=30, alpha=0.6, color="black")
    ax.set_title("Raw data")
    ax.set_xlabel("feature 0")
    ax.set_ylabel("feature 1")

    plt.tight_layout()
    if args.output:
        plt.savefig(args.output, dpi=150)
        print(f"Plot saved to {args.output}")
    else:
        plt.show()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    print(f"Generating {args.n_samples} points with make_blobs (k={args.k}, seed={args.random_state})...")
    X, _ = make_data(args)

    print("Running Dafny kmeans...")
    labels, centroids, init_centroids, converged = run_dafny_kmeans(X, args)
    status = "converged" if converged else f"did not converge within {args.max_iter} iterations"
    print(f"Done — {status}")
    print(f"Initial centroids:\n{init_centroids}")
    print(f"Final centroids:\n{centroids}")

    plot(X, labels, centroids, init_centroids, converged, args)


if __name__ == "__main__":
    main()
