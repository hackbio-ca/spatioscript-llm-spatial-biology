import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def ask_gpt(prompt, system_role="You have to asnwer in Cypher query format. Nothing else."):
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