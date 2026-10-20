import json
from datetime import datetime
from pathlib import Path

from mcp.server.mcpserver import MCPServer

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "expenses.json"

mcp = MCPServer("Paisa Pal")


def load_expenses():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def save_expenses(items):
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


@mcp.tool()
def add_expense(amount: float, category: str, note: str = "") -> str:
    """Kharcha save karta hai. amount rupees mein hota hai. category jaise food, transport, bills."""
    items = load_expenses()
    items.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": amount,
        "category": category.lower(),
        "note": note,
    })
    save_expenses(items)
    return f"Saved: {amount} rupees for {category}."


@mcp.tool()
def monthly_summary() -> str:
    """Is mahine ka total kharcha aur category wise breakdown batata hai."""
    month = datetime.now().strftime("%Y-%m")
    items = [e for e in load_expenses() if e["date"].startswith(month)]
    if not items:
        return "Is mahine koi kharcha nahi likha gaya."

    totals = {}
    for e in items:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]

    total = sum(totals.values())
    lines = [f"{cat}: {amt:.0f}" for cat, amt in sorted(totals.items(), key=lambda x: -x[1])]
    return f"Is mahine total {total:.0f} rupees kharch hue.\n" + "\n".join(lines)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")