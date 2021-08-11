"""
Algorithms for computing temporal degree centrality for temporal graph objects.
"""


def temporal_degree_centrality(graph, labels=None, intervals=None, normalize=True):
    """
        Returns the temporal degree centralities of nodes in a temporal graph.

        Parameter(s):
        -------------
        graph : TemporalGraph
            An undirected temporal graph.
        labels: list
            A list of node labels to calculate centralities for. Default is all nodes in the temporal graph.
            Example: ["A", "B", "C", ...]
        intervals : tuple/List
            A tuple of intervals (pairs of start and end times) for the temporal graph to be restricted to.
            Example: ((0,3), (5,7))
        normalize : bool
            Whether to apply normalization to the produced centrality values.

        Returns:
        --------
        temporal_degree : dict
            The temporal degrees of the nodes.
            For example: {A: 1.3, B:1.2, C:2.5, ...}

        Example(s):
        -----------
            graph = TemporalGraph('test_network', data=CsvInput('./network.csv'))
            degree_values = degree_centrality(graph, labels=["A", "B", "C"], intervals=((1, 5), (8, 10)))

        Notes:
        ------
        This implementation for calculating temporal degree centrality is adapted from an algorithm detailed in
        "Temporal Node Centrality in Complex Networks" (Kim and Anderson, 2011), found here:
        https://www.cl.cam.ac.uk/~rja14/Papers/TemporalCentrality.pdf. Our algorithm does not use a static expansion
        as they have outlined, and so is adapted accordingly. Here, temporal degree centrality is the average of a nodes'
        degree over the snapshots of the graph in a given time interval.

        TODO:
        -----
        - Implement directed versions (in-degree centrality, out-degree centrality)
        - Implement "centrality evolution" (Kim and Andersen, 2011)
        - Test validity on dummy data + debug
        - Test with bigger datasets, e.g. those included in overtime + debug
        - Write unit tests

    """
    # Restrict graph to specified time interval
    if intervals:
        graph = graph.get_temporal_subgraph(intervals)

    # Only calculate for specified labels
    if not labels:
        labels = graph.nodes.labels()   # If labels not specified, set labels to all nodes in input graph

    # Initialize
    node_count = {label: 0 for label in labels}

    # Calculate total degree for each node
    for edge in graph.edges.aslist():       # Increment temporal degree every time node is seen as endpoint of edge

        node_count[edge.node1.label] += 1
        node_count[edge.node2.label] += 1

    # Apply normalization
    if normalize:
        normalization_factor = (graph.nodes.count() - 1) * (graph.edges.end() - graph.edges.start())
        temporal_degree = {label: value / normalization_factor for label, value in node_count.items()}

    # Sort by descending centrality value
    sorted_temporal_degree = {label: value for label, value in sorted(temporal_degree.items(),
                                                                      key=lambda item: item[1],
                                                                      reverse=True)}

    return sorted_temporal_degree