import os
from dotenv import load_dotenv
from openai import OpenAI
# from neo4j import GraphDatabase

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

#--------- Graph Database -------------------------
# driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

# def get_schema():
#     schema = []
#     with driver.session() as session:
#         result = session.run("CALL db.schema.visualization()")
#         for record in result:
#             schema.append(record.data())
#     return schema

# schema_info = str(get_schema())


#def ask_gpt(prompt, system_role=f"You have to asnwer in Cypher query format. Nothing else. Schema: {schema_info}"):
#--------------------------------------------------
def ask_gpt(prompt, system_role=f"You have to asnwer in Cypher query format. Nothing else."):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    user_prompt = "Write a Cypher query to find all nodes with the label 'Person'."
    refined_answer = ask_gpt(user_prompt)
    print(refined_answer)