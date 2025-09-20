// Clear database (optional for testing)
MATCH (n) DETACH DELETE n;

// Create a Cell Annotation
CREATE (ca:CellAnnotation {name: "CD8 T cell"});

// Create Genes
CREATE (g1:Gene {name: "CD8"})
CREATE (g2:Gene {name: "CD3"})
CREATE (g3:Gene {name: "CD4"});

// Connect CellAnnotation -> Genes
MATCH (ca:CellAnnotation {name: "CD8 T cell"})
MATCH (g1:Gene {name: "CD8"})
MATCH (g2:Gene {name: "CD3"})
MATCH (g3:Gene {name: "CD4"})
MERGE (ca)-[:MARKER]->(g1)
MERGE (ca)-[:MARKER]->(g2)
MERGE (ca)-[:MARKER]->(g3);

// Create Spots with spatial coordinates
CREATE (s1:Spot {id: "S1", x: 10, y: 20})
CREATE (s2:Spot {id: "S2", x: 15, y: 25});

// Connect Genes -> Spots with expression values
MATCH (g1:Gene {name: "CD8"}), (s1:Spot {id:"S1"})
MERGE (g1)-[:EXPRESSION {value: 5.2}]->(s1);

MATCH (g2:Gene {name: "CD3"}), (s1:Spot {id:"S1"})
MERGE (g2)-[:EXPRESSION {value: 3.8}]->(s1);

MATCH (g3:Gene {name: "CD4"}), (s2:Spot {id:"S2"})
MERGE (g3)-[:EXPRESSION {value: 7.1}]->(s2);

// Create Spatial Cluster
CREATE (c1:SpatialCluster {id: "ClusterA"});

// Connect Spots -> Cluster
MATCH (s1:Spot {id:"S1"}), (c1:SpatialCluster {id:"ClusterA"})
MERGE (s1)-[:IN_CLUSTER]->(c1);

MATCH (s2:Spot {id:"S2"}), (c1:SpatialCluster {id:"ClusterA"})
MERGE (s2)-[:IN_CLUSTER]->(c1);

// (Optional) Add distance relationship between spots
MATCH (s1:Spot {id:"S1"}), (s2:Spot {id:"S2"})
MERGE (s1)-[:DISTANCE {value: 7.07}]->(s2);
