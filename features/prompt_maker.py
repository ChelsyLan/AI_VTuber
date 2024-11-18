import pandas as pd
from config import *

def get_identity(identity_path) -> str:
    with open(identity_path, "r", encoding="utf-8") as f:
        identity_context = f.read()
    
    return identity_context

def parse_product_data(csv_path="data/products/perfumes.csv", n_rows=10):
    df = pd.read_csv(csv_path,encoding="ISO-8859-1")
    df = df.head(n_rows)
    # format: list[dict[col: str, val: str]]
    product_json_string = df.to_json(orient='records')
    return product_json_string

def get_system_prompt(
    identity_path="characterConfig/Character/shopping_assistant.txt",
) -> dict[str, str]:
    identity_context = get_identity(identity_path)
    perfumes_list = parse_product_data()
    games_list = parse_product_data(csv_path="data/products/games.csv")
    product_prompt = f"\nHere is the product list:\n{perfumes_list} {games_list}"
    system_prompt_str = identity_context + product_prompt

    return {"role": "system", "content": system_prompt_str}
    
def get_prompt(history: list[str]):
    total_len = 0

    # Get Vtuber identity/role
    system_prompt = get_system_prompt()
    prompt = [system_prompt] + history

    # Step 3: Add a system message for response constraints
    if status_config == "VIEWER_MODE":
        prompt.append(
            {
                "role": "system",
                "content": f"Make sure your response is within {maxCharacters} characters. Avoid answering with more than {maxCharacters} characters by summarizing the response. Here is the latest conversation.",
            }
        )
        
        total_len = sum(len(d['content']) for d in prompt)
        while total_len > 4000:
            try:
                prompt.pop(1)  # Remove the third item (index 2) from prompt
                total_len = sum(len(d['content']) for d in prompt)
            except IndexError:
                print("Error: Prompt too long! Unable to remove more items.")
                break  # Exit the loop if no more items can be removed
    
    return prompt

if __name__ == "__main__":
    history = []
    prompt = get_prompt(history=history)
    print(prompt)
