// recursive spec: sum of squared diffs for first n coords
function Dist2Prefix(v1: array<real>, v2: array<real>, n: int): real
  requires v1.Length == v2.Length
  requires 0 <= n <= v1.Length
  reads v1, v2
  decreases n
{
  if n == 0 then 0.0
  else
    Dist2Prefix(v1, v2, n - 1) +
    (v1[n - 1] - v2[n - 1]) * (v1[n - 1] - v2[n - 1])
}

// full squared euclidean distance — just calls Dist2Prefix over all coords
function Dist2(v1: array<real>, v2: array<real>): real
  requires v1.Length == v2.Length
  reads v1, v2
{
  Dist2Prefix(v1, v2, v1.Length)
}

// imperative version of Dist2 — verified to match the recursive spec
method SquaredEuclideanDistance(v1: array<real>, v2: array<real>) returns (sum: real)
  requires v1.Length == v2.Length
  ensures sum == Dist2Prefix(v1, v2, v1.Length)
  ensures 0.0 <= sum
{
  var i := 0;
  sum := 0.0;

  while i < v1.Length
    invariant 0 <= i <= v1.Length
    invariant sum == Dist2Prefix(v1, v2, i)  // ties the running sum to the spec; postcondition is immediate when i == v1.Length
    invariant 0.0 <= sum
    decreases v1.Length - i
  {
    var diff := v1[i] - v2[i];
    sum := sum + diff * diff;
    i := i + 1;
  }
}

// assigns each point to its nearest centroid by squared euclidean distance
method AssignLabels(points: array<array<real>>, centroids: array<array<real>>) returns (labels: array<int>)
  requires points.Length >= 1 && centroids.Length >= 1
  requires forall i, j :: 0 <= i <= j < points.Length ==> points[i].Length == points[j].Length
  requires forall c :: 0 <= c < centroids.Length ==> centroids[c].Length == points[0].Length

  ensures labels.Length == points.Length
  ensures forall i :: 0 <= i < points.Length ==> 0 <= labels[i] < centroids.Length
  ensures forall i :: 0 <= i < points.Length ==>
            forall c :: 0 <= c < centroids.Length ==>
              Dist2(points[i], centroids[labels[i]]) <= Dist2(points[i], centroids[c])
{
  var n := points.Length;
  var k := centroids.Length;
  labels := new int[n];

  var p_i := 0;
  while p_i < n
    invariant 0 <= p_i <= n
    invariant labels.Length == n
    invariant forall i :: 0 <= i < p_i ==> 0 <= labels[i] < k
    invariant forall i :: 0 <= i < p_i ==>
              forall c :: 0 <= c < k ==>
                Dist2(points[i], centroids[labels[i]]) <= Dist2(points[i], centroids[c])
  {
    var i := p_i;           
    var p := points[i];

    var best_i := 0;
    var best_d := Dist2(p, centroids[0]);

    var c_i := 1;
    while c_i < k
      invariant 1 <= c_i <= k
      invariant 0 <= best_i < c_i  // best_i is always a centroid index we've already scanned
      invariant best_d == Dist2(p, centroids[best_i])  // keeps best_d in sync with best_i
      invariant forall c :: 0 <= c < c_i ==> best_d <= Dist2(p, centroids[c])
      decreases k - c_i
    {
      var d := Dist2(p, centroids[c_i]);
      if d < best_d {
        best_d := d;
        best_i := c_i;
      }
      c_i := c_i + 1;
    }

    labels[i] := best_i;

    p_i := p_i + 1;
  }
  return labels;
}

// Counts how many of the first n points have been assigned to cluster c
function CountCluster(labels: array<int>, c: int, n: int): int
  requires 0 <= n <= labels.Length
  reads labels
  decreases n
{
  if n == 0 then 0
  else CountCluster(labels, c, n - 1) + (if labels[n - 1] == c then 1 else 0)
}

// Sums coordinate j over all points in first n points belonging to cluster c
function SumCoord(points: array<array<real>>, labels: array<int>, c: int, j: int, n: int): real
  requires 0 <= n <= points.Length
  requires points.Length == labels.Length
  requires 0 <= j
  requires forall i :: 0 <= i < points.Length ==> j < points[i].Length
  reads points, labels
  reads set i | 0 <= i < points.Length :: points[i]
  decreases n
{
  if n == 0 then 0.0
  else
    SumCoord(points, labels, c, j, n - 1) +
    (if labels[n - 1] == c then points[n - 1][j] else 0.0)
}

// recomputes each centroid as the mean of its assigned points; empty clusters keep the old centroid
method UpdateCentroids(points: array<array<real>>, labels: array<int>, k: int, old_centroids: array<array<real>>) returns (new_centroids: array<array<real>>)
  requires points.Length >= 1 && old_centroids.Length >= 1
  requires k == old_centroids.Length
  requires labels.Length == points.Length
  requires forall i, j :: 0 <= i <= j < points.Length ==> points[i].Length == points[j].Length
  requires forall c :: 0 <= c < old_centroids.Length ==> old_centroids[c].Length == points[0].Length
  requires forall i :: 0 <= i < labels.Length ==> 0 <= labels[i] < k
  
  ensures new_centroids.Length == k
  ensures forall c :: 0 <= c < k ==> new_centroids[c].Length == points[0].Length
  // Cluster assigning policy
  ensures forall c :: 0 <= c < k ==>
    forall j :: 0 <= j < points[0].Length ==>
      // Empty cluster: keep old centroid
      (CountCluster(labels, c, labels.Length) == 0 ==>
        new_centroids[c][j] == old_centroids[c][j])
      &&
      // Non-empty cluster: new centroid is the mean
      (CountCluster(labels, c, labels.Length) > 0 ==>
        new_centroids[c][j] == SumCoord(points, labels, c, j, points.Length) /
          (CountCluster(labels, c, labels.Length) as real))
{
  var n := points.Length;
  var d := points[0].Length;

  // Use mutable arrays
  var sums := new real[k, d];
  var counts := new int[k];

  // Initialize sums to 0.0 and counts to 0
  var c := 0;
  while c < k
    invariant 0 <= c <= k
    invariant forall x :: 0 <= x < c ==> counts[x] == 0
    invariant forall x, y :: 0 <= x < c && 0 <= y < d ==> sums[x, y] == 0.0
  {
    counts[c] := 0;
    var r := 0;
    while r < d
      invariant 0 <= r <= d
      invariant forall y :: 0 <= y < r ==> sums[c, y] == 0.0
      invariant forall x, y :: 0 <= x < c && 0 <= y < d ==> sums[x, y] == 0.0
      invariant forall x :: 0 <= x <= c ==> counts[x] == 0 
    {
      sums[c, r] := 0.0;
      r := r + 1;
    }
    c := c + 1;
  }

  // Accumulate sums and counts
  var i := 0;
  while i < n
    invariant 0 <= i <= n
    invariant forall c :: 0 <= c < k ==> counts[c] == CountCluster(labels, c, i)
    invariant forall c, j :: 0 <= c < k && 0 <= j < d ==>
      sums[c, j] == SumCoord(points, labels, c, j, i)
  {
    var lab := labels[i];
    counts[lab] := counts[lab] + 1;
    var j := 0;
    while j < d
      invariant 0 <= j <= d
      invariant forall c :: 0 <= c < k ==> counts[c] == CountCluster(labels, c, i) + (if c == lab then 1 else 0)
      invariant forall c, jj :: 0 <= c < k && 0 <= jj < d ==>
        sums[c, jj] == SumCoord(points, labels, c, jj, i) +
          (if c == lab && jj < j then points[i][jj] else 0.0)  // only coords < j have been added for point i so far
    {
      sums[lab, j] := sums[lab, j] + points[i][j];
      j := j + 1;
    }
    i := i + 1;
  }

  new_centroids := new array<real>[k];
  c := 0;
  while c < k
    invariant 0 <= c <= k
    invariant forall x :: 0 <= x < c ==> new_centroids[x].Length == d
    invariant forall x :: 0 <= x < k ==> counts[x] == CountCluster(labels, x, n)
    invariant forall x, j :: 0 <= x < k && 0 <= j < d ==>
      sums[x, j] == SumCoord(points, labels, x, j, n)
    invariant forall x :: 0 <= x < c ==>
      forall j :: 0 <= j < d ==>
        (CountCluster(labels, x, n) == 0 ==> new_centroids[x][j] == old_centroids[x][j])
        &&
        (CountCluster(labels, x, n) > 0 ==>
          new_centroids[x][j] == SumCoord(points, labels, x, j, n) /
            (CountCluster(labels, x, n) as real))
  {
    var centroid := new real[d];
    if counts[c] == 0 {
      // If cluster is empty, copy old centroid
      var j := 0;
      while j < d
        invariant 0 <= j <= d
        // Let dafny know that the inner loop does not modify new_centroids[x].Length
        invariant forall x :: 0 <= x < c ==> new_centroids[x].Length == d
        invariant forall x :: 0 <= x < k ==> counts[x] == CountCluster(labels, x, n)
        invariant forall x, jj :: 0 <= x < k && 0 <= jj < d ==>
          sums[x, jj] == SumCoord(points, labels, x, jj, n)
        invariant forall jj :: 0 <= jj < j ==> centroid[jj] == old_centroids[c][jj]
        // Let dafny know that centroid is a different object than already assigned new_centroids
        invariant forall x :: 0 <= x < c ==> new_centroids[x] != centroid
        invariant forall x :: 0 <= x < c ==>
          forall jj :: 0 <= jj < d ==>
            (CountCluster(labels, x, n) == 0 ==> new_centroids[x][jj] == old_centroids[x][jj])
            &&
            (CountCluster(labels, x, n) > 0 ==>
              new_centroids[x][jj] == SumCoord(points, labels, x, jj, n) /
                (CountCluster(labels, x, n) as real))
      {
        centroid[j] := old_centroids[c][j];
        j := j + 1;
      }
    } else {
      var inv := 1.0 / (counts[c] as real);
      var j := 0;
      while j < d
        invariant 0 <= j <= d
        // Let dafny know that the inner loop does not modify new_centroids[x].Length
        invariant forall x :: 0 <= x < c ==> new_centroids[x].Length == d
        invariant forall x :: 0 <= x < k ==> counts[x] == CountCluster(labels, x, n)
        invariant forall x, jj :: 0 <= x < k && 0 <= jj < d ==>
          sums[x, jj] == SumCoord(points, labels, x, jj, n)
        invariant inv == 1.0 / (CountCluster(labels, c, n) as real)
        invariant forall jj :: 0 <= jj < j ==>
          centroid[jj] == SumCoord(points, labels, c, jj, n) /
            (CountCluster(labels, c, n) as real)
        // Let dafny know that centroid is a different object than already assigned new_centroids
        invariant forall x :: 0 <= x < c ==> new_centroids[x] != centroid
        invariant forall x :: 0 <= x < c ==>
          forall jj :: 0 <= jj < d ==>
            (CountCluster(labels, x, n) == 0 ==> new_centroids[x][jj] == old_centroids[x][jj])
            &&
            (CountCluster(labels, x, n) > 0 ==>
              new_centroids[x][jj] == SumCoord(points, labels, x, jj, n) /
                (CountCluster(labels, x, n) as real))
      {
        centroid[j] := sums[c, j] * inv;
        j := j + 1;
      }
    }
    new_centroids[c] := centroid;
    c := c + 1;
  }
}

method LabelsEqual(new_labels: array<int>, old_labels: array<int>) returns (result: bool)
requires new_labels.Length == old_labels.Length
ensures result <==> (forall i :: 0 <= i < new_labels.Length ==> new_labels[i] == old_labels[i])
{
  var n := new_labels.Length;
  var i := 0;
  while i < n
    invariant 0 <= i <= n
    // Loop exit/termination condition - all previously seen labels have been equal so far
    invariant forall x :: 0 <= x < i ==> new_labels[x] == old_labels[x]
  {
    if new_labels[i] != old_labels[i]
    {
      return false;
    }
    i := i + 1;
  }
  return true;
}

method KMeans(
  points: array<array<real>>,
  k: int,
  initial_centroids: array<array<real>>,
  max_iterations: int
) returns (centroids: array<array<real>>, labels: array<int>, converged: bool)
  requires points.Length >= 1
  requires initial_centroids.Length >= 1
  requires max_iterations >= 0
  requires initial_centroids.Length == k
  requires points.Length >= k
  requires forall i, j :: 0 <= i <= j < points.Length ==> points[i].Length == points[j].Length
  requires forall i :: 0 <= i < points.Length ==>
             forall j :: 0 <= j < initial_centroids.Length ==>
               points[i].Length == initial_centroids[j].Length

  ensures labels.Length == points.Length
  ensures centroids.Length == k
  ensures forall i :: 0 <= i < labels.Length ==> 0 <= labels[i] < k
  ensures forall c :: 0 <= c < k ==> centroids[c].Length == points[0].Length
  // Returned labels are always belong to returned centroids
  ensures forall i :: 0 <= i < points.Length ==>
            forall c :: 0 <= c < centroids.Length ==>
              Dist2(points[i], centroids[labels[i]]) <= Dist2(points[i], centroids[c])
  // Only guaranteed if we actually converged
  ensures converged ==>
            forall c :: 0 <= c < k ==>
              forall j :: 0 <= j < points[0].Length ==>
                (CountCluster(labels, c, labels.Length) > 0 ==>
                  centroids[c][j] ==
                    SumCoord(points, labels, c, j, points.Length) /
                    (CountCluster(labels, c, labels.Length) as real))
{
  centroids := initial_centroids;
  labels := AssignLabels(points, centroids);
  converged := false;

  var it := 0;
  while it < max_iterations
    invariant 0 <= it <= max_iterations
    invariant centroids.Length == k
    invariant labels.Length == points.Length
    invariant forall i :: 0 <= i < labels.Length ==> 0 <= labels[i] < k
    invariant forall c :: 0 <= c < k ==> centroids[c].Length == points[0].Length
    invariant forall i :: 0 <= i < points.Length ==>
                forall c :: 0 <= c < k ==>
                  Dist2(points[i], centroids[labels[i]]) <= Dist2(points[i], centroids[c])
    invariant converged == false  // converged is only set to true right before an early return, never through normal loop exit
  {
    var old_labels := labels;
    centroids := UpdateCentroids(points, old_labels, k, centroids);

    var new_labels := AssignLabels(points, centroids);
    converged := LabelsEqual(new_labels, old_labels);
    if converged {
      labels := old_labels;
      converged := true;
      return;
    }

    labels := new_labels;
    it := it + 1;
  }
}

// ============================================================
// Well-formedness predicates
// ============================================================

// all points exist and share the same number of dimensions
predicate SameDim(points: array<array<real>>)
  reads points, set i | 0 <= i < points.Length :: points[i]
{
  points.Length >= 1 &&
  forall i, j :: 0 <= i <= j < points.Length ==> points[i].Length == points[j].Length
}

// every index in the seq is a valid index into an array of length n
predicate ValidIdxs(n: int, idxs: seq<int>)
{
  forall t :: 0 <= t < |idxs| ==> 0 <= idxs[t] < n
}

// ============================================================
// Minimum distance from points[p] to any point in chosen
// ============================================================

// min squared distance from point p to any point in chosen — the greedy objective
function MinDistIdx(points: array<array<real>>, p: int, chosen: seq<int>): real
  requires SameDim(points)
  requires 0 <= p < points.Length
  requires 1 <= |chosen|
  requires ValidIdxs(points.Length, chosen)
  reads points, set i | 0 <= i < points.Length :: points[i]
  decreases |chosen|
{
  if |chosen| == 1 then
    Dist2(points[p], points[chosen[0]])
  else
    var prev := MinDistIdx(points, p, chosen[..(|chosen| - 1)]);
    var curr := Dist2(points[p], points[chosen[|chosen| - 1]]);
    if prev < curr then prev else curr
}

// ============================================================
// Simple sequence lemmas
// ============================================================

// appending a valid index keeps the seq valid — trivially true, dafny needs it spelled out
lemma AppendPreservesValidIdxs(n: int, idxs: seq<int>, next: int)
  requires ValidIdxs(n, idxs)
  requires 0 <= next < n
  ensures ValidIdxs(n, idxs + [next])
{
}

// appending next doesn't invalidate the greedy invariant at earlier positions — idxs[..t] is unchanged for t < |idxs|
lemma GreedyFactsPreservedByAppend(points: array<array<real>>, idxs: seq<int>, next: int)
  requires SameDim(points)
  requires 1 <= |idxs|
  requires ValidIdxs(points.Length, idxs)
  requires 0 <= next < points.Length
  requires forall t :: 1 <= t < |idxs| ==>
            forall i :: 0 <= i < points.Length ==>
              MinDistIdx(points, i, idxs[..t]) <= MinDistIdx(points, idxs[t], idxs[..t])
  ensures forall t :: 1 <= t < |idxs| ==>
            forall i :: 0 <= i < points.Length ==>
              MinDistIdx(points, i, (idxs + [next])[..t]) <=
              MinDistIdx(points, (idxs + [next])[t], (idxs + [next])[..t])
{
  forall t | 1 <= t < |idxs|
    ensures forall i :: 0 <= i < points.Length ==>
      MinDistIdx(points, i, (idxs + [next])[..t]) <=
      MinDistIdx(points, (idxs + [next])[t], (idxs + [next])[..t])
  {
    assert (idxs + [next])[..t] == idxs[..t];
    assert (idxs + [next])[t] == idxs[t];
    assert forall i :: 0 <= i < points.Length ==>
      MinDistIdx(points, i, idxs[..t]) <= MinDistIdx(points, idxs[t], idxs[..t]);
  }
}

// next was chosen by FindFarthestIndex so it satisfies the greedy condition at position |idxs|
lemma NewGreedyFactFromChoice(points: array<array<real>>, idxs: seq<int>, next: int)
  requires SameDim(points)
  requires 1 <= |idxs|
  requires ValidIdxs(points.Length, idxs)
  requires 0 <= next < points.Length
  requires forall i :: 0 <= i < points.Length ==>
            MinDistIdx(points, i, idxs) <= MinDistIdx(points, next, idxs)
  ensures forall i :: 0 <= i < points.Length ==>
            MinDistIdx(points, i, (idxs + [next])[..|idxs|]) <=
            MinDistIdx(points, (idxs + [next])[|idxs|], (idxs + [next])[..|idxs|])
{
  assert (idxs + [next])[..|idxs|] == idxs;
  assert (idxs + [next])[|idxs|] == next;
}

// ============================================================
// Find the farthest point from the currently chosen prefix
// ============================================================

// linear scan — returns the index that maximizes MinDistIdx over all points
method FindFarthestIndex(points: array<array<real>>, chosen: seq<int>) returns (best: int)
  requires SameDim(points)
  requires 1 <= |chosen|
  requires ValidIdxs(points.Length, chosen)
  ensures 0 <= best < points.Length
  ensures forall i :: 0 <= i < points.Length ==>
            MinDistIdx(points, i, chosen) <= MinDistIdx(points, best, chosen)
{
  best := 0;
  var i := 1;

  while i < points.Length
    invariant 1 <= i <= points.Length
    invariant 0 <= best < i
    invariant forall j :: 0 <= j < i ==>
              MinDistIdx(points, j, chosen) <= MinDistIdx(points, best, chosen)
    decreases points.Length - i
  {
    if MinDistIdx(points, best, chosen) < MinDistIdx(points, i, chosen) {
      assert forall j :: 0 <= j < i ==> MinDistIdx(points, j, chosen) <= MinDistIdx(points, i, chosen);
      best := i;
    }
    i := i + 1;
  }
}

// ============================================================
// Verified deterministic farthest-first initialization
// Returns indices only: this is the clean proof core
// ============================================================

// greedy farthest-first seeding — builds k indices where each new point maximizes
// its min-distance to the already chosen set; the loop invariant captures this property
// at every position t, and the three helper lemmas re-establish it after each append
method DeterministicInitIdxs(points: array<array<real>>, k: int) returns (idxs: seq<int>)
  requires SameDim(points)
  requires 1 <= k <= points.Length
  ensures |idxs| == k
  ensures idxs[0] == 0
  ensures ValidIdxs(points.Length, idxs)
  ensures forall t :: 1 <= t < |idxs| ==>
            forall i :: 0 <= i < points.Length ==>
              MinDistIdx(points, i, idxs[..t]) <= MinDistIdx(points, idxs[t], idxs[..t])
{
  idxs := [0];

  while |idxs| < k
    invariant 1 <= |idxs| <= k
    invariant idxs[0] == 0
    invariant ValidIdxs(points.Length, idxs)
    invariant forall t :: 1 <= t < |idxs| ==>
              forall i :: 0 <= i < points.Length ==>
                MinDistIdx(points, i, idxs[..t]) <= MinDistIdx(points, idxs[t], idxs[..t])
    decreases k - |idxs|
  {
    var oldIdxs := idxs;

    var next := FindFarthestIndex(points, oldIdxs);
    assert 0 <= next < points.Length;
    assert forall i :: 0 <= i < points.Length ==>
      MinDistIdx(points, i, oldIdxs) <= MinDistIdx(points, next, oldIdxs);

    GreedyFactsPreservedByAppend(points, oldIdxs, next);
    NewGreedyFactFromChoice(points, oldIdxs, next);
    AppendPreservesValidIdxs(points.Length, oldIdxs, next);

    idxs := oldIdxs + [next];
  }
}

// ============================================================
// Materialize centroid array from the chosen indices
// ============================================================

// copies point arrays at positions idxs into a fresh centroid array (same array objects, not deep copies)
method MaterializeCentroids(points: array<array<real>>, idxs: seq<int>) returns (centroids: array<array<real>>)
  requires SameDim(points)
  requires 1 <= |idxs|
  requires ValidIdxs(points.Length, idxs)
  ensures centroids.Length == |idxs|
  ensures forall t :: 0 <= t < |idxs| ==> centroids[t] == points[idxs[t]]
  ensures forall t :: 0 <= t < |idxs| ==> centroids[t].Length == points[0].Length
{
  centroids := new array<real>[|idxs|];
  var t := 0;

  while t < |idxs|
    invariant 0 <= t <= |idxs|
    invariant centroids.Length == |idxs|
    invariant forall j :: 0 <= j < t ==> centroids[j] == points[idxs[j]]
    invariant forall j :: 0 <= j < t ==> centroids[j].Length == points[0].Length
    decreases |idxs| - t
  {
    centroids[t] := points[idxs[t]];
    t := t + 1;
  }
}

// // ============================================================
// // Wrapper returning both indices and centroids
// // ============================================================

// wrapper that returns both the index sequence (useful for proofs) and the centroid array (needed by kmeans)
method DeterministicKMeansInit(
  points: array<array<real>>,
  k: int
) returns (idxs: seq<int>, centroids: array<array<real>>)
  requires SameDim(points)
  requires 1 <= k <= points.Length

  ensures |idxs| == k
  ensures idxs[0] == 0
  ensures ValidIdxs(points.Length, idxs)

  ensures centroids.Length == k
  ensures forall c :: 0 <= c < k ==> centroids[c] == points[idxs[c]]
  ensures forall c :: 0 <= c < k ==> centroids[c].Length == points[0].Length
  ensures centroids[0] == points[0]

  ensures forall t :: 1 <= t < k ==>
            forall i :: 0 <= i < points.Length ==>
              MinDistIdx(points, i, idxs[..t]) <= MinDistIdx(points, idxs[t], idxs[..t])
{
  idxs := DeterministicInitIdxs(points, k);
  centroids := MaterializeCentroids(points, idxs);
}

// ============================================================
// Distance non-negativity and self-distance lemmas
// (exported for use by voronoi.dfy via include "kmeans.dfy")
// ============================================================

// Dist2Prefix(v1, v2, n) >= 0 by induction.
// The squared-difference step d*d >= 0 is the same nonlinear fact
// that SquaredEuclideanDistance's loop invariant already relies on.
// If Z3 cannot discharge `d * d >= 0.0` here, replace the assert
// with `assume {:axiom} d * d >= 0.0;`.
lemma Dist2PrefixNonNeg(v1: array<real>, v2: array<real>, n: int)
  requires v1.Length == v2.Length
  requires 0 <= n <= v1.Length
  ensures Dist2Prefix(v1, v2, n) >= 0.0
  decreases n
{
  if n == 0 { }
  else {
    Dist2PrefixNonNeg(v1, v2, n - 1);
    var d := v1[n-1] - v2[n-1];
    assert d * d >= 0.0;
  }
}

lemma Dist2NonNeg(v1: array<real>, v2: array<real>)
  requires v1.Length == v2.Length
  ensures Dist2(v1, v2) >= 0.0
{
  Dist2PrefixNonNeg(v1, v2, v1.Length);
}

// Dist2Prefix(v, v, n) == 0 by induction:
// each term is (v[i]-v[i])^2 = 0^2 = 0.
lemma Dist2PrefixSelf(v: array<real>, n: int)
  requires 0 <= n <= v.Length
  ensures Dist2Prefix(v, v, n) == 0.0
  decreases n
{
  if n == 0 { }
  else {
    Dist2PrefixSelf(v, n - 1);
    var d := v[n-1] - v[n-1];
    assert d == 0.0;
    assert d * d == 0.0;
  }
}

lemma Dist2Self(v: array<real>)
  ensures Dist2(v, v) == 0.0
{
  Dist2PrefixSelf(v, v.Length);
}

// public entry point for deterministic init — same as DeterministicKMeansInit but drops the index sequence
// the forall-exists postcondition needs an explicit witness proof since dafny can't find it automatically
method DeterministicKMeansInitCentroids(
  points: array<array<real>>,
  k: int
) returns (centroids: array<array<real>>)
  requires SameDim(points)
  requires 1 <= k <= points.Length

  ensures centroids.Length == k
  ensures forall c :: 0 <= c < k ==> centroids[c].Length == points[0].Length
  ensures forall c :: 0 <= c < k ==> exists i :: 0 <= i < points.Length && centroids[c] == points[i]
  ensures centroids[0] == points[0]
{
  var idxs := DeterministicInitIdxs(points, k);
  centroids := MaterializeCentroids(points, idxs);

  forall c | 0 <= c < k
    ensures exists i :: 0 <= i < points.Length && centroids[c] == points[i]
  {
    assert 0 <= idxs[c] < points.Length;
    assert centroids[c] == points[idxs[c]];
  }
}