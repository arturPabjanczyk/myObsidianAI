import chainlit as cl
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")


@cl.on_message
async def main(message: cl.Message):
    response = model.invoke([HumanMessage(content=message.content)])

    # Wyciągamy statystyki z odpowiedzi
    usage = response.response_metadata.get('token_usage', {})
    input_tokens = usage.get('prompt_tokens', 0)
    output_tokens = usage.get('completion_tokens', 0)

    # Wyświetlamy w terminalu PyCharma
    print(f"--- KOSZT ZAPYTANIA ---")
    print(f"Input: {input_tokens} tokenów | Output: {output_tokens} tokenów")

    await cl.Message(content=response.content).send()