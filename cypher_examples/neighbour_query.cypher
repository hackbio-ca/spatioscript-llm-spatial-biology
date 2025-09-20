// For each CD8 cell, find nearby spots and their annotations
MATCH (cd8:AnnotationLevel3 {name:"CD4/CD8"})-[:ANNOTATES]->(s:Spot)

// Find all neighbors within 50 microns
MATCH (neighbor:Spot)
WHERE s <> neighbor
  AND point.distance(s.coord, neighbor.coord) <= 50

// Get neighbor annotations (level 1 or 3, both allowed)
OPTIONAL MATCH (neighbor)<-[:ANNOTATES]-(ann)

WITH s, s.cell_id AS cd8_id,
     collect(DISTINCT ann.name) AS neighbor_annotations,
     count(DISTINCT neighbor) AS neighbor_count

RETURN cd8_id, neighbor_count, neighbor_annotations
ORDER BY neighbor_count DESC
LIMIT 20;
