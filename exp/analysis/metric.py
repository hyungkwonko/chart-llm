import scipy
import numpy as np
from sklearn.neighbors import NearestNeighbors

from sklearn.manifold import TSNE
from sklearn.decomposition import PCA


def reduce_embedding_dimensionality(embeddings, num_dimensions=5, method="PCA"):
    """
    Author: Perttu Hämäläinen
    Source: https://dl.acm.org/doi/10.1145/3544548.3580688
    """
    all_emb = np.concatenate(embeddings, axis=0)

    # cosine distance
    all_emb = all_emb / np.linalg.norm(all_emb, axis=1, keepdims=True)

    if method == "PCA":
        pca = PCA(n_components=num_dimensions)
        x = pca.fit_transform(all_emb)
    elif method == "TSNE":
        tsne = TSNE(n_components=num_dimensions)
        x = tsne.fit_transform(all_emb)
    elif method == "UMAP":
        import umap

        reducer = umap.UMAP(
            n_components=num_dimensions, metric="cosine", n_neighbors=5, random_state=42
        )
        x = reducer.fit_transform(all_emb)
    else:
        raise Exception("Invalid dimensionality reduction method!")

    row = 0
    result = []
    for e in embeddings:
        N = e.shape[0]
        result.append(x[row : row + N])
        row += N

    return result


def KNN_support(A, B, k, knn_algorithm):
    """
    Author: Perttu Hämäläinen
    Source: https://dl.acm.org/doi/10.1145/3544548.3580688

    For each vector in A, checks whether it lies within the support of the distribution of B vectors.
    This is implemented by checking whether the vector lies within a hypersphere centered at the closest B vector,
    hypersphere radius set equal to the distance between the B vector and its k:th nearest neighbor in B.
    This is the core of the Kynkäänniemi et al. method for precision and recall estimation of generative models.
    WARNING: you shouldn't call this with a B matrix that has vectors replicated based on frequencies, as this will mess up
    the k:th nearest neighbor distance measures, which may become zero for replicated vectors.
    """
    # Build KNN lookup structure for B
    nbrs = NearestNeighbors(n_neighbors=k, algorithm=knn_algorithm).fit(B)
    distances, _ = nbrs.kneighbors(B, n_neighbors=k)
    kth_b_dist = distances[:, -1]  # distance to k-th NN
    ab_distances, indices = nbrs.kneighbors(A, n_neighbors=1)  # distance to 1-th NN
    ab_closest_dist = ab_distances[:, 0]  # torch.squeeze
    b_search_ball_radiuses = kth_b_dist[indices[:, 0]]  # torch.squeeze

    assert ab_closest_dist.shape == b_search_ball_radiuses.shape

    return ab_closest_dist <= b_search_ball_radiuses


def KNN_precision_and_recall(
    generated, real, generated_counts=None, real_counts=None, k=5, knn_algorithm="brute"
):
    """
    Author: Perttu Hämäläinen
    Source: https://dl.acm.org/doi/10.1145/3544548.3580688

    Kynkäänniemi et al. precision and recall estimation for generated data.

    :param generated: generated data, shape [num_vectors,dim]
    :param real: real data (ground truth), shape [num_vectors,dim]
    :param generated_counts: counts (frequencies) for each generated vector
    :param real_counts: counts (frequencies) for each real vector
    :param k: number of nearest neighbors to use. Low values are noisy, but high values may provide optimistic results
    :param knn_algorithm: the nearest neighbors algorithm to use (see sklearn.neighbors.NearestNeighbors)
    :return: tuple: (precision,recall)
    """

    if generated_counts is None:
        generated_counts = np.ones(generated.shape[0])
    if real_counts is None:
        real_counts = np.ones(real.shape[0])

    # print(f"generated.shape: {generated.shape}")
    # print(f"real.shape: {real.shape}")

    precision = KNN_support(A=generated, B=real, k=k, knn_algorithm=knn_algorithm)
    # print(f"precision.shape: {precision.shape}")
    # exit()
    precision = np.average(precision, weights=generated_counts)

    recall = KNN_support(A=real, B=generated, k=k, knn_algorithm=knn_algorithm)
    recall = np.average(recall, weights=real_counts)

    return precision, recall


def frechet_embedding_distance(A, B, A_counts=None, B_counts=None):
    """
    Author: Perttu Hämäläinen
    Source: https://dl.acm.org/doi/10.1145/3544548.3580688

    Frechet distance calculation adapted from (https://machinelearningmastery.com/how-to-implement-the-frechet-inception-distance-fid-from-scratch/)

    :param A: Numpy array of embedding vectors, shape [num_vectors,num_embedding_dimensions]
    :param B: Numpy array of embedding vectors, shape [num_vectors,num_embedding_dimensions]
    :param A_counts: Numpy array of counts (frequencies) for each A vector
    :param B_counts: Numpy array of counts (frequencies) for each B vector
    :return:
    """

    if A_counts is None:
        A_counts = np.ones(A.shape[0])
    if B_counts is None:
        B_counts = np.ones(B.shape[0])

    # calculate mean and covariance statistics
    mu1, sigma1 = np.average(A, axis=0, weights=A_counts), np.cov(
        A, rowvar=False, fweights=A_counts
    )
    mu2, sigma2 = np.average(B, axis=0, weights=B_counts), np.cov(
        B, rowvar=False, fweights=B_counts
    )

    # calculate sum squared difference between means
    ssdiff = np.sum((mu1 - mu2) ** 2.0)

    # calculate sqrt of product between cov
    covmean = scipy.linalg.sqrtm(sigma1.dot(sigma2))

    # check and correct imaginary numbers from sqrt
    if np.iscomplexobj(covmean):
        covmean = covmean.real

    # calculate score
    fd = ssdiff + np.trace(sigma1 + sigma2 - 2.0 * covmean)

    return fd
