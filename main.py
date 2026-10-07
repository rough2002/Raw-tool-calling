import json
import os
from google.genai import Client
from dotenv import load_dotenv
from tool_declarations import TOOLS,TOOL_FUNCTIONS,expenses

load_dotenv()


client  = Client(api_key=os.getenv("GEMINI_API_KEY"))

def main():
    interaction = client.interactions.create(
    model="gemini-3.1-flash-lite",
    input="i spent 3200 on in starbucks coffee last yesterday can you add it",
    tools=TOOLS,
    )
    prev_interaction_id = interaction.id

    calls = [s for s in interaction.steps if s.type == "function_call"]

    tool =  TOOL_FUNCTIONS[calls[0].name]
    tool_output = tool(**calls[0].arguments)

    final_interaction = client.interactions.create(
    model="gemini-3.1-flash-lite",
    input=[
        {
            "type": "function_result",
            "name": calls[0].name,
            "call_id": calls[0].id,
            "result": [{"type": "text", "text": json.dumps(tool_output)}],
        }
    ],
    tools=TOOLS,
    previous_interaction_id=prev_interaction_id,
    )

    print(final_interaction.output_text)
    print("new expense value")
    print(expenses)
    


if __name__ == "__main__":
    main()
