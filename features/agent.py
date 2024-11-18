from pydantic import BaseModel
from openai import OpenAI

from config import status_config, max_token
from features.expressions import ExpressionEnum
from features.prompt_maker import get_prompt

class AIChatResponse(BaseModel):
    message: str
    expression: ExpressionEnum

# answer from OpenAI
def get_openai_answer(conversation, client: OpenAI,
) -> tuple[str, ExpressionEnum]:
    
    if status_config == "VIEWER_MODE":
        total_characters = sum(len(d['content']) for d in conversation)
        
        while total_characters > 4000:
            try:
                # print(total_characters)
                # print(len(conversation))
                conversation.pop(1)
                total_characters = sum(len(d['content']) for d in conversation)
            except Exception as e:
                print("Error removing old messages: {0}".format(e))

    prompt = get_prompt(conversation)

    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=prompt,
        max_tokens=max_token,
        temperature=1,   # More creative and engaging responses
        top_p=0.9,       # Balances diversity
        frequency_penalty=0.2,  # Avoids repetitive responses
        presence_penalty=0.5,    # Encourages introducing new topics
        response_format=AIChatResponse,
    )
    message = response.choices[0].message.parsed.message
    expression_value = response.choices[0].message.parsed.expression

    prompt_tokens = response.usage.completion_tokens
    completion_tokens = response.usage.prompt_tokens
    total_tokens = response.usage.total_tokens

    # Print the token usage and cost
    print(f"Prompt: {prompt}")
    print(f"Prompt Tokens: {prompt_tokens}")
    print(f"Completion Tokens: {completion_tokens}")
    print(f"Total Tokens: {total_tokens}")
    print(f"Expression: {expression_value}")
    print(f"___________")
    
    return message, expression_value
