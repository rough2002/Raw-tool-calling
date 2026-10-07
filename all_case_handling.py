'''this version of function calling handles all versions including multistep , parallel , single tool call ,  and general prompts'''


import json
import os
from google.genai import Client
from dotenv import load_dotenv
from tool_declarations import TOOLS,TOOL_FUNCTIONS,expenses

load_dotenv()


client  = Client(api_key=os.getenv("GEMINI_API_KEY"))

def robust_tool_call(prompt :str):

    output_text = None

    interaction = client.interactions.create(
    model="gemini-3.1-flash-lite",
    input=prompt,
    tools=TOOLS,
    )

    output_text = interaction.output_text


    while not output_text : 
      prev_interaction_id = interaction.id

      calls = [s for s in interaction.steps if s.type == "function_call"]

      tool_results = []

      for call in calls :
          tool = TOOL_FUNCTIONS[call.name]
          tool_output = tool(**call.arguments)
          tool_results.append({
                          "type": "function_result",
                          "name": call.name,
                          "call_id": call.id,
                          "result": [{"type": "text", "text": json.dumps(tool_output)}],
          })


      interaction = client.interactions.create(
      model="gemini-3.1-flash-lite",
      input=tool_results,
      tools=TOOLS,
      previous_interaction_id=prev_interaction_id,
      )
      output_text = interaction.output_text

    print(output_text)
    print("new expense value")
    print(expenses)
    

