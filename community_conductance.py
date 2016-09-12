from __future__ import division

from itertools import chain

import networkx as nx

__all__ = ['boundary_expansion', 'conductance', 'cut_size', 'edge_expansion',
           'mixing_expansion', 'node_expansion', 'normalized_cut_size',
           'volume']

def cut_size(G, S, T=None, weight=None):
    """Returns the size of the cut between two sets of nodes.

    A *cut* is a partition of the nodes of a graph into two sets. The
    *cut size* is the sum of the weights of the edges "between" the two
    sets of nodes.

    Parameters
    ----------
    G : NetworkX graph

    S : sequence
        A sequence of nodes in `G`.

    T : sequence
        A sequence of nodes in `G`. If not specified, this is taken to
        be the set complement of `S`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    number
        Total weight of all edges from nodes in set `S` to nodes in
        set `T` (and, in the case of directed graphs, all edges from
        nodes in `T` to nodes in `S`).

    Examples
    --------
    In the graph with two cliques joined by a single edges, the natural
    bipartition of the graph into two blocks, one for each clique,
    yields a cut of weight one::

        >>> G = nx.barbell_graph(3, 0)
        >>> S = {0, 1, 2}
        >>> T = {3, 4, 5}
        >>> nx.cut_size(G, S, T)
        1

    Each parallel edge in a multigraph is counted when determining the
    cut size::

        >>> G = nx.MultiGraph(['ab', 'ab'])
        >>> S = {'a'}
        >>> T = {'b'}
        >>> nx.cut_size(G, S, T)
        2

    Notes
    -----
    In a multigraph, the cut size is the total weight of edges including
    multiplicity.

    """
    edges = nx.edge_boundary(G, S, T)
    if G.is_directed():
        edges = chain(edges, nx.edge_boundary(G, T, S))
    return sum(1 for u, v in edges)




def volume(G, S):
    """Returns the volume of a set of nodes.

    """
    degree = G.degree
    #return sum(d for v, d in degree(S))
    return len(S)





def conductance(G, S, T=None, weight=None):
    """Returns the conductance of two sets of nodes.

    The *conductance* is the quotient of the cut size and the smaller of
    the volumes of the two sets. [1]

    Parameters
    ----------
    G : NetworkX graph

    S : sequence
        A sequence of nodes in `G`.

    T : sequence
        A sequence of nodes in `G`.

    weight : object
        Edge attribute key to use as weight. If not specified, edges
        have weight one.

    Returns
    -------
    number
        The conductance between the two sets `S` and `T`.

    See also
    --------
    cut_size
    edge_expansion
    normalized_cut_size
    volume

    References
    ----------
    .. [1] David Gleich.
           *Hierarchical Directed Spectral Graph Partitioning*.
           <https://www.cs.purdue.edu/homes/dgleich/publications/Gleich%202005%20-%20hierarchical%20directed%20spectral.pdf>

    """
    if T is None:
        T = set(G) - set(S)
    num_cut_edges = cut_size(G, S, T)
    volume_S = volume(G, S)
    volume_T = volume(G, T)
    return num_cut_edges / min(volume_S, volume_T)
