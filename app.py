# ------------------------------------------------------------------------------------
# A basic Shiny Chat example powered by OpenAI via LangChain.
# To run it, you'll need OpenAI API key.
# To get one, follow the instructions at https://platform.openai.com/docs/quickstart
# To use other providers/models via LangChain, see https://python.langchain.com/v0.1/docs/modules/model_io/chat/quick_start/
# ------------------------------------------------------------------------------------
import os

from app_utils import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

from shiny.express import ui
from src.think import (
    extract_thinking,
    display_thinking,
    display_message
)
# Either explicitly set the OPENAI_API_KEY environment variable before launching the
# app, or set them in a file named `.env`. The `python-dotenv` package will load `.env`
# as environment variables which can later be read by `os.getenv()`.
load_dotenv()
# llm = ChatOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))  # type: ignore
llm = ChatGroq(temperature=0, model="deepseek-r1-distill-llama-70b")

# Set some Shiny page options
ui.page_opts(
    title="Hello LangChain Chat Models",
    fillable=True,
    fillable_mobile=True,
)

# Create and display an empty chat UI
system_message = {
  "content": "You are a helpful assistant.",
  "role": "system"
}
chat = ui.Chat(id="chat", messages=[system_message])
chat.ui()


# Define a callback to run when the user submits a message
@chat.on_user_submit
async def _():
    # Get messages currently in the chat
    messages = chat.messages(format="langchain")
    # Create a response message stream
    response = llm.astream(messages)
    # Append the response stream into the chat
    await chat.append_message_stream(response)


@chat.transform_assistant_response
def _(content: str) -> ui.HTML:
    return ui.markdown(display_message(content))