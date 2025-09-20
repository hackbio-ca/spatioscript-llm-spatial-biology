CALL apoc.periodic.iterate(
  'CALL apoc.load.csv("file:///var/lib/neo4j/import/gbm_obs_with_annotations_level_3.csv", {sep: ",", header: true}) YIELD map as row',
  '
  // Level 1 annotation (broad category)
  MERGE (a1:AnnotationLevel1 {name: row.annotation_level_1})

  // Level 3 annotation (fine subtype)
  MERGE (a3:AnnotationLevel3 {name: row.annotation_level_3})

  // Create Spot (cell) with spatial point
  MERGE (s:Spot {cell_id: row.cell_id})
    ON CREATE SET 
      s.coord = point({x: toFloat(row.x), y: toFloat(row.y)}),
      s.x = toFloat(row.x),
      s.y = toFloat(row.y)

  // Connect annotations separately to Spot
  MERGE (a1)-[:ANNOTATES]->(s)
  MERGE (a3)-[:ANNOTATES]->(s)
  ',
  {batchSize:5000, iterateList:true, parallel:true}
);
