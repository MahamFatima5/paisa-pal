import asyncio
import re

import streamlit as st
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_URL = "http://127.0.0.1:8000/mcp"
CATEGORIES = ["chai", "khana", "food", "transport", "bills", "shopping"]


async def call_tool(name, args):
    async with streamable_http_client(MCP_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, args)
            return result.content[0].text


def handle(message):
    text = message.lower()

    if "summary" in text or "hisaab" in text or "mahine" in text:
        return asyncio.run(call_tool("monthly_summary", {}))

    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    if not numbers:
        return "Amount samajh nahi aaya. Jaise likhein: chai pe 300 kharch kiye."

    amount = float(numbers[0])
    category = next((c for c in CATEGORIES if c in text), "other")
    return asyncio.run(
        call_tool("add_expense", {"amount": amount, "category": category, "note": message})
    )


st.title("Paisa Pal")
st.caption("Kharcha likhein, ya 'is mahine ka summary' poochein.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, text in st.session_state.messages:
    with st.chat_message(role):
        st.write(text)

user_input = st.chat_input("Jaise: chai pe 300 kharch kiye")

if user_input:
    st.session_state.messages.append(("user", user_input))
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        try:
            reply = handle(user_input)
        except Exception as e:
            reply = f"MCP server se connect nahi ho saka. Check karein ke server chal raha hai. ({e})"
        st.write(reply)

    st.session_state.messages.append(("assistant", reply))