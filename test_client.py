import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    url = "http://127.0.0.1:8000/mcp"
    async with streamable_http_client(url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool(
                "add_expense",
                {"amount": 150, "category": "food", "note": "lunch"},
            )
            print("add_expense:", result.content[0].text)

            result = await session.call_tool("monthly_summary", {})
            print("monthly_summary:", result.content[0].text)


asyncio.run(main())