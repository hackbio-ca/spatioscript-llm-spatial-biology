# app.py
import os
from dotenv import load_dotenv
from openai import OpenAI
from neo4j import GraphDatabase
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body
import json

load_dotenv()

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Neo4j driver
driver = GraphDatabase.driver("bolt://neo4j:7687", auth=("neo4j", "letmein"))

# FastAPI app
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for testing only, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_schema():
    with driver.session() as session:
        # node labels + properties
        nodes = session.run("CALL db.schema.nodeTypeProperties()").data()
        rels = session.run("CALL db.schema.relTypeProperties()").data()

    schema_info = {
        "nodes": nodes,
        "relationships": rels
    }
    return schema_info

def get_annotations():
    with driver.session() as session:
        result = session.run("MATCH (a:AnnotationLevel3) RETURN DISTINCT a.name AS name")
        return [r["name"] for r in result]

available_annotations = get_annotations()


def ask_gpt(prompt: str, schema_info: str = None) -> str:
    # system_role = "You have to answer in Cypher query format. Nothing else."
    # system_role = (
    # "You must answer with only the Cypher query, no explanations. "
    # "no code fences, no triple backticks, no language tags. "
    # "If asked to compute distance, always use `point.distance()` instead of `distance()`. "
    # "Direction is always: (AnnotationLevelX)-[:ANNOTATES]->(Spot). "
    # "Always return at most the top 10 results by appending `LIMIT 10` to the query. "
    # "Only return scalar projections (e.g., s.cell_id, a.name, distance). "
    # "Never return nodes. "
    # "Order by distance ASC when present and LIMIT 10. "
    # f"Valid AnnotationLevel3 names are ONLY: {', '.join(available_annotations)}. "
    # "If asking about tumour/non-tumour or cancer/non-cancer, use 'Neoplastic' or 'Non-neoplastic' as AnnotationLevel1 exactly. "
    # "Only Spot nodes have coord. Annotations (AnnotationLevel1/2/3) do not have coordinates. Distances must always be computed between Spot nodes. "
    # "The Cypher query must be syntactically correct and executable in Neo4j. " 
    # )
    system_role = (
    "You must answer with only the Cypher query, no explanations. "
    "Do not include APOC procedures, CALL statements, comments, code fences, or language tags. "
    "If asked to compute distance, always use `point.distance()` instead of `distance()`. "
    "Direction is always: (AnnotationLevelX)-[:ANNOTATES]->(Spot). "
    "Never assume or use the reverse direction. "
    "Always return at most the top 10 results by appending `LIMIT 10` to the query. "
    "Always include LIMIT 10 at the very end of the query, even if not requested. "
    "Only use explicit scalar property projections (e.g., .cell_id, .name, distance). "
    "Never return nodes, maps, or `*`. "
    "Order by distance ASC only when distance is returned. "
    f"Valid AnnotationLevel3 names are ONLY: {', '.join(available_annotations)}. "
    "If asking about tumour/non-tumour or cancer/non-cancer, use 'Neoplastic' or 'Non-neoplastic' as AnnotationLevel1 exactly. "
    "Annotation names must match exactly (case-sensitive). Do not normalize or pluralize. "
    "Only Spot nodes have coord. Annotations (AnnotationLevel1/2/3) do not have coordinates. "
    "Distances must always be computed between Spot nodes. "
    "Every WITH must include all variables required later in RETURN, ORDER BY, or WHERE. "
    "Never drop variables and then attempt to use them afterward. "
    "Do not redefine or shadow variables unnecessarily. "
    "Only use Cypher standard functions and point.distance. Do not invent new functions. "
    "The Cypher query must be syntactically correct and executable in Neo4j. "
    )
    if schema_info:
        # system_role += f" Schema: {schema_info}"
        system_role += "\nSchema:\n" + json.dumps(schema_info, indent=2)

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # use gpt-4 or gpt-3.5 depending on need
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()

# def run_cypher(query: str):
#     with driver.session() as session:
#         result = session.run(query)
#         return [record.data() for record in result]

def run_cypher(query: str):
    with driver.session() as session:
        result = session.run(query)
        # Neo4j returns Record objects → convert to plain dicts
        return [dict(record) for record in result]
    
@app.post("/ask")
def ask(prompt: str = Body(..., embed=True)):
    # Step 0: get schema info from Neo4j
    schema_info = get_schema()

    # Step 1: get Cypher query from GPT
    cypher_query = ask_gpt(prompt, schema_info)
    # cypher_query = ask_gpt(prompt)

    # Step 2: run Cypher query on Neo4j
    try:
        results = run_cypher(cypher_query)
    except Exception as e:
        return {"error": str(e), "cypher": cypher_query}

    # Step 3: return to frontend
    return {"cypher": cypher_query, "results": results}
