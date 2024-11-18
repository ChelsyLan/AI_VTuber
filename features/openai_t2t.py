import os
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder    
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from pydantic import BaseModel,Field
from langchain_core.messages import BaseMessage,AIMessage
from typing import List


class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        self.messages.extend(messages)
    def clear(self) -> None:
        self.messages = []

def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    return OpenAI(api_key=api_key)

def get_openai_client_langchain(model_name="gpt-4o-mini"):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    return ChatOpenAI(
        api_key=api_key,
        model_name=model_name,
        streaming=True,
    )

client = get_openai_client_langchain()

store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]


history = get_by_session_id("1")
history.add_message(AIMessage(content="hello,I'm your shopping assistant"))

SYSTEM_CONTENT_TEMPLATE = """
You are a shopping assistant in retail selling {product_type}.
You answer customers' questions in a friendly and natural style using spoken English.
Your answer makes the shopping experience enjoyable and encourage customers to reach out if they have any questions or need assistance.
Feel free to ask customers about their preferences, recommend products, and inform them about any ongoing promotions.
You help humans find the best product or introduce products.
"""

prompt = ChatPromptTemplate.from_messages([
    ('system',SYSTEM_CONTENT_TEMPLATE),
    MessagesPlaceholder(variable_name="history"),
    ("human","{llm_input}")
])

chain  = prompt| client
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="llm_input",
    history_messages_key="history",
)


def openai_conversation():
    while True:
        user_input = input("Input: ")
        response = chain_with_history.invoke(
                    {"product_type":"perfume","llm_input":user_input},
                    config={"configurable": {"session_id": "foo"}}
                )
        print(response.content)
        yield response.content

# if __name__ == "__main__":
#     for response in openai_conversation():
#         pass


