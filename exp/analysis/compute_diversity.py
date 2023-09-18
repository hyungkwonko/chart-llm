import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

from sklearn.metrics.pairwise import pairwise_distances
from sentence_transformers import SentenceTransformer

from exp.analysis.metric import (
    reduce_embedding_dimensionality,
    KNN_precision_and_recall,
    frechet_embedding_distance,
)
from sentence_transformers import SentenceTransformer


def embed_sentences(data, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    emb = model.encode(data)
    return emb


def calculate_across_distance(emb1, emb2, k_val=5, embedding=True, verbose=False):
    embs = [emb1, emb2]

    if embedding:
        embs = reduce_embedding_dimensionality(embs, method="UMAP")

    fd = frechet_embedding_distance(
        A=embs[0],
        B=embs[1],
    )
    precision, recall = KNN_precision_and_recall(
        real=embs[0],
        generated=embs[1],
        k=k_val,
    )

    if verbose:
        print(f"fd: {fd}, precision: {precision}, recall: {recall}")
    return fd, precision, recall


def mean_pairwise_distance(emb):
    """
    Calculate the average of mean pairwise distances between points in a 2-dimensional embedding vector.
    """
    distances = pairwise_distances(emb)

    # Set the diagonal elements to np.nan to exclude self-distances
    np.fill_diagonal(distances, np.nan)

    # Calculate the mean distance for each point
    mean_distances = np.nanmean(distances, axis=1)

    # Calculate the average of the mean distances
    avg_distance = np.mean(mean_distances)

    return avg_distance


def minimum_pairwise_distance(emb):
    """
    Calculate the average of minimum pairwise distances between points in a 2-dimensional embedding vector.
    """
    distances = pairwise_distances(emb)

    # Exclude diagonal values
    np.fill_diagonal(distances, np.inf)

    # Find the minimum distance for each point in the array
    min_distances = np.min(distances, axis=1)

    # Calculate the average of the minimum distances
    avg_distance = np.mean(min_distances)

    return avg_distance


def remote_mst(emb):
    """
    Calculate the sum of edge weights of a minimum spanning tree (MST) of a set of 2-dimensional points.
    """
    distances = pairwise_distances(emb)

    # Create a compressed sparse row matrix from the distance matrix
    dist_matrix_csr = csr_matrix(distances)

    # Calculate the minimum spanning tree of the distance matrix
    mst = minimum_spanning_tree(dist_matrix_csr)

    # Calculate the sum of edge weights of the MST
    mst_sum = mst.sum()

    return mst_sum


def percentile_distance_to_centroid(points, p=90):
    """
    Calculate the Pth percentile distance to the centroid of a 2-dimensional embedding vector.
    """
    # Calculate the centroid of the points
    centroid = np.mean(points, axis=0)

    # Calculate the distances from each point to the centroid
    distances = np.linalg.norm(points - centroid, axis=1)

    # Calculate the Pth percentile distance
    percentile_distance = np.percentile(distances, p)

    return percentile_distance


def sparsity_around_medoid(emb):
    """
    Calculate the sparsity of points positioned around the medoid of a 2-dimensional embedding vector.
    """
    distances = pairwise_distances(emb)

    # Find the index of the medoid
    medoid_idx = np.argmin(distances.sum(axis=0))

    # Calculate the distances from each point to the medoid
    medoid_distances = distances[:, medoid_idx]

    # Calculate the sparsity of points around the medoid
    sparsity = np.mean(medoid_distances)

    return sparsity


def shannon_wiener_index(embed, grid_size=5, eps=1e-9):
    """
    Calculate the Shannon-Wiener index for points in a 2-dimensional embedding vector.

    :param embed: 2-dimensional embedding vector
    :type embed: numpy.ndarray
    :param grid_size: Size of the grid partition
    :type grid_size: int
    :return: Shannon-Wiener index
    :rtype: float
    """
    # Calculate the min and max values for each dimension
    mins = np.min(embed, axis=0)
    maxs = np.max(embed, axis=0)

    # Create a grid partition of the space
    x_bins = np.linspace(mins[0], maxs[0], grid_size + 1)
    y_bins = np.linspace(mins[1], maxs[1], grid_size + 1)

    # Count the frequency of points in each bin
    freqs = np.histogram2d(embed[:, 0], embed[:, 1], bins=[x_bins, y_bins])[0]

    # Normalize the frequencies to get probabilities
    probs = freqs / np.sum(freqs)

    # Calculate the Shannon-Wiener index
    sw_index = -np.sum((probs + eps) * np.log(probs + eps))

    return sw_index


def calculate_within_distance(emb, verbose=False, p=90, grid_size=5):
    emb = reduce_embedding_dimensionality([emb], method="UMAP")
    emb = np.array(emb[0])

    remove_clique = mean_pairwise_distance(emb)
    chamfer = minimum_pairwise_distance(emb)
    mst_dispersion = remote_mst(emb)
    span = percentile_distance_to_centroid(emb, p=p)
    sparseness = sparsity_around_medoid(emb)
    entropy = shannon_wiener_index(emb, grid_size=grid_size)

    if verbose:
        print(
            f"rc: {remove_clique}, c: {chamfer}, mst: {mst_dispersion}, span: {span}, spars: {sparseness}, ent: {entropy}"
        )
    return (remove_clique, chamfer, mst_dispersion, span, sparseness, entropy)
