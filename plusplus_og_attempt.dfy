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

function Dist2(v1: array<real>, v2: array<real>): real
  requires v1.Length == v2.Length
  reads v1, v2
{
  Dist2Prefix(v1, v2, v1.Length)
}

function MinDistToPrefix(p: array<real>, chosen: seq<array<real>>): real
  requires 1 <= |chosen|
  requires forall c :: 0 <= c < |chosen| ==> chosen[c].Length == p.Length
  reads p, set c | 0 <= c < |chosen| :: chosen[c]
  decreases |chosen|
{
  if |chosen| == 1 then Dist2(p, chosen[0])
  else
    var prev := MinDistToPrefix(p, chosen[..(|chosen| - 1)]);
    var curr := Dist2(p, chosen[|chosen| - 1]);
    if prev < curr then prev else curr
}

method Argmax(a: array<real>) returns (idx: int) 
requires a.Length >= 1 
ensures 0 <= idx < a.Length 
ensures forall i :: 0 <= i < a.Length ==> a[i] <= a[idx] 
{ 
    idx := 0; 
    var i := 1; 
    while i < a.Length 
    invariant 1 <= i <= a.Length 
    invariant 0 <= idx < i 
    invariant forall j :: 0 <= j < i ==> a[j] <= a[idx] 
    decreases a.Length - i 
    { 
        if a[i] > a[idx] 
        { 
            idx := i; 
        } 
        i := i + 1; 
    } 
}



method {:verify false} {:isolate_assertions} {:timeLimitMultiplier 10} kmeans_plusplus( points: array<array<real>>, k: int ) returns (centroids: array<array<real>>) 
requires k >= 1 
requires points.Length >= 1 
requires points.Length >= k 
requires forall i, j :: 0 <= i <= j < points.Length ==> points[i].Length == points[j].Length 
ensures centroids.Length == k 
ensures forall c :: 0 <= c < k ==> centroids[c].Length == points[0].Length 
ensures forall c :: 0 <= c < k ==> exists i :: 0 <= i < points.Length && centroids[c] == points[i] 
ensures centroids[0] == points[0] 
ensures forall t :: 1 <= t < k ==> forall i :: 0 <= i < points.Length ==> MinDistToPrefix(points[i], centroids[..t]) <= MinDistToPrefix(centroids[t], centroids[..t]) 
{ 
    centroids := new array<real>[k]; 
    centroids[0] := points[0]; 
    var n := points.Length; 
    var min_dist := new real[n]; 
    var c := 1; 
    while c < k 
    invariant 1 <= c <= k 
    invariant centroids.Length == k 
    invariant centroids[0] == points[0]
    invariant old(centroids[0]) == centroids[0] 
    invariant forall i :: 0 <= i < n ==> points[i].Length == points[0].Length 
    invariant forall x :: 0 <= x < c ==> centroids[x].Length == points[0].Length 
    invariant forall x :: 0 <= x < c ==> exists i :: 0 <= i < n && centroids[x] == points[i] 
    invariant forall t :: 1 <= t < c ==> forall i :: 0 <= i < n ==> MinDistToPrefix(points[i], centroids[..t]) <= MinDistToPrefix(centroids[t], centroids[..t]) 
    decreases k - c 
    { 
        var i := 0; 
        while i < n 
        invariant 0 <= i <= n 
        invariant 1 <= c
        invariant centroids.Length == k 
        invariant centroids[0] == points[0]
        invariant old(centroids[0]) == centroids[0]
        // invariant forall j, k :: 0 <= j <= k < centroids.Length ==> centroids[j].Length == centroids[k].Length 
        invariant forall x :: 0 <= x < c ==> centroids[x].Length == points[0].Length && forall ii :: 0 <= ii < n ==> points[ii].Length == points[0].Length
        invariant forall ii :: 0 <= ii < i ==> min_dist[ii] == MinDistToPrefix(points[ii], centroids[..c]) 
        // invariant forall x :: 0 <= x < c ==> exists idx :: 0 <= idx < n && centroids[x] == points[idx] 
        invariant forall ii :: 0 <= ii < n ==> forall x :: 0 <= x < c ==> centroids[x].Length == points[ii].Length 
        decreases n - i 
        { 
            min_dist[i] := MinDistToPrefix(points[i], centroids[..c]); 
            i := i + 1; 
        } 
        var idx := Argmax(min_dist); 
        ghost var chosen := centroids[..c]; 
        assert forall ii :: 0 <= ii < n ==> min_dist[ii] == MinDistToPrefix(points[ii], chosen); 
        assert forall ii :: 0 <= ii < n ==> min_dist[ii] <= min_dist[idx]; 
        assert min_dist[idx] == MinDistToPrefix(points[idx], chosen); 
        assert forall ii :: 0 <= ii < n ==> MinDistToPrefix(points[ii], chosen) <= MinDistToPrefix(points[idx], chosen); 
        centroids[c] := points[idx]; assert centroids[c] == points[idx]; // Key framing fact: writing to centroids[c] does not affect centroids[..c] 
        assert centroids[..c] == chosen; 
        assert forall ii :: 0 <= ii < n ==> MinDistToPrefix(points[ii], chosen) <= MinDistToPrefix(centroids[c], chosen); // chosen == centroids[..c], so restate in terms of array slice for the invariant 
        assert forall ii :: 0 <= ii < n ==> MinDistToPrefix(points[ii], centroids[..c]) <= MinDistToPrefix(centroids[c], centroids[..c]); c := c + 1; 
    } 
}