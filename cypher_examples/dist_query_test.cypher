// Find all pairs of Spots annotated with CD8 within 50 microns
MATCH (a3:AnnotationLevel3 {name:"CD4/CD8"})-[:ANNOTATES]->(s1:Spot),
      (a3)-[:ANNOTATES]->(s2:Spot)
WHERE id(s1) < id(s2)  
  AND point.distance(s1.coord, s2.coord) <= 50

WITH s1, s2, point.distance(s1.coord, s2.coord) AS dist
ORDER BY dist ASC
LIMIT 10

RETURN s1.cell_id AS spot1, s2.cell_id AS spot2, dist
