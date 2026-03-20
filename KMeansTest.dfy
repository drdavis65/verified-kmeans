include "kmeans.dfy"
include "data.dfy"

// {:verify false} skips static verification; expect statements still check properties at runtime.
// Run with: dafny run KMeansTest.dfy --allow-warnings
method {:verify false} Main()
{
  var points := MakePoints();

  // expects matching DeterministicKMeansInitCentroids requires
  expect SameDim(points);         // points.Length >= 1 and all rows same length
  expect 1 <= K <= points.Length; // k is in bounds

  // Initial centroids via deterministic farthest-first seeding
  var initial_centroids := DeterministicKMeansInitCentroids(points, K);

  // expects matching DeterministicKMeansInitCentroids ensures
  expect initial_centroids.Length == K;
  expect initial_centroids[0] == points[0]; // fixed seed is always points[0]
  expect forall c :: 0 <= c < K ==> initial_centroids[c].Length == points[0].Length;
  expect forall c :: 0 <= c < K ==> exists i :: 0 <= i < points.Length && initial_centroids[c] == points[i];

  // expects matching kmeans requires
  expect initial_centroids.Length >= 1;
  expect points.Length >= K;
  expect forall i :: 0 <= i < points.Length ==>
           forall j :: 0 <= j < initial_centroids.Length ==>
             points[i].Length == initial_centroids[j].Length; // dimensions agree

  print "initial centroids:\n";
  var ii := 0;
  while ii < initial_centroids.Length {
    print "  cluster ", ii, ": ";
    var id := 0;
    while id < initial_centroids[ii].Length {
      print initial_centroids[ii][id], " ";
      id := id + 1;
    }
    print "\n";
    ii := ii + 1;
  }

  var centroids, labels, converged :=
    KMeans(points, K, initial_centroids, MaxIter);

  // expects matching kmeans ensures
  expect labels.Length == points.Length;
  expect centroids.Length == K;
  expect forall c :: 0 <= c < K ==> centroids[c].Length == points[0].Length;
  expect forall i :: 0 <= i < points.Length ==> 0 <= labels[i] < K;
  expect forall i :: 0 <= i < points.Length ==>
           forall c :: 0 <= c < K ==>
             Dist2(points[i], centroids[labels[i]]) <= Dist2(points[i], centroids[c]);
  expect converged ==>
           forall c :: 0 <= c < K ==>
             forall j :: 0 <= j < points[0].Length ==>
               CountCluster(labels, c, labels.Length) > 0 ==>
                 centroids[c][j] == SumCoord(points, labels, c, j, points.Length) /
                                    (CountCluster(labels, c, labels.Length) as real);

  print "converged: ", converged, "\n";
  print "labels: ";
  var pi := 0;
  while pi < labels.Length {
    print labels[pi], " ";
    pi := pi + 1;
  }
  print "\n";

  print "centroids:\n";
  var ci := 0;
  while ci < centroids.Length {
    print "  cluster ", ci, ": ";
    var di := 0;
    while di < centroids[ci].Length {
      print centroids[ci][di], " ";
      di := di + 1;
    }
    print "\n";
    ci := ci + 1;
  }
}
