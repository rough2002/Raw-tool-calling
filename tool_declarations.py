# --- Tool declarations -----------------------------------------------------
# Each dict tells the model what a tool does. "name" must match a key in
# TOOL_FUNCTIONS, because that is how we look up the real function to run.
add_expense_decl = {
    "type": "function",
    "name": "add_expense",
    "description": "Record a new expense. Use when the user says they spent money on something.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "Amount spent, in INR"},
            "category": {
                "type": "string",
                "enum": ["food", "travel", "groceries", "bills", "other"],
            },
            "note": {"type": "string", "description": "Short description, e.g. 'lunch'"},
        },
        "required": ["amount", "category", "note"],
    },
}
 
get_total_decl = {
    "type": "function",
    "name": "get_total",
    "description": "Get the total spent (in INR) in one category, or everything with 'all'.",
    "parameters": {
        "type": "object",
        "properties": {
            "category": {
                "type": "string",
                "enum": ["food", "travel", "groceries", "bills", "other", "all"],
            },
        },
        "required": ["category"],
    },
}
 
convert_currency_decl = {
    "type": "function",
    "name": "convert_currency",
    "description": "Convert an amount between currencies. Supports INR, USD and EUR only.",
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "from_currency": {"type": "string", "description": "Currency code, e.g. INR"},
            "to_currency": {"type": "string", "description": "Currency code, e.g. USD"},
        },
        "required": ["amount", "from_currency", "to_currency"],
    },
}

expenses = []

VALID_CATEGORIES = {"food", "travel", "groceries", "bills", "other"}

# Hardcoded rates: how many units of each currency equal 1 USD
RATES_PER_USD = {
    "USD": 1.0,
    "INR": 83.0,
    "EUR": 0.92,
}


def add_expense(amount, category, note):
    """Add one expense to the list. Returns a dict, never raises."""
    if not isinstance(amount, (int, float)) or amount <= 0:
        return {"error": f"Invalid amount {amount}. Amount must be greater than 0."}
    if category not in VALID_CATEGORIES:
        return {
            "error": f"Invalid category '{category}'. "
                     f"Must be one of: {', '.join(sorted(VALID_CATEGORIES))}."
        }
    expenses.append({"amount": amount, "category": category, "note": note})
    return {"status": "added", "amount": amount, "category": category, "note": note}


def get_total(category):
    """Total spent in one category, or 'all' for everything."""
    if category != "all" and category not in VALID_CATEGORIES:
        return {
            "error": f"Invalid category '{category}'. "
                     f"Use 'all' or one of: {', '.join(sorted(VALID_CATEGORIES))}."
        }
    if category == "all":
        total = sum(e["amount"] for e in expenses)
    else:
        total = sum(e["amount"] for e in expenses if e["category"] == category)
    return {"category": category, "total": total, "currency": "INR"}


def convert_currency(amount, from_currency, to_currency):
    """Convert between INR, USD and EUR using the hardcoded rates."""
    src, dst = str(from_currency).upper(), str(to_currency).upper()
    if src not in RATES_PER_USD:
        return {"error": f"Unsupported currency '{from_currency}'. Supported: INR, USD, EUR."}
    if dst not in RATES_PER_USD:
        return {"error": f"Unsupported currency '{to_currency}'. Supported: INR, USD, EUR."}
    in_usd = amount / RATES_PER_USD[src]
    result = in_usd * RATES_PER_USD[dst]
    return {
        "amount": amount,
        "from": src,
        "to": dst,
        "result": round(result, 2),
    }


# Lookup table: later, the loop uses this to run whatever the model asks for
TOOL_FUNCTIONS = {
    "add_expense": add_expense,
    "get_total": get_total,
    "convert_currency": convert_currency,
}

TOOLS = [add_expense_decl, get_total_decl, convert_currency_decl]