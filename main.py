from all_case_handling import robust_tool_call


def main():
    prompts = [
    "hi",
    "I spent 250 on lunch",
    "Add 120 for an auto and 400 for groceries",
    "How much have I spent on food, in USD?",
    "Convert 100 INR to XYZ",
    "I spent -50 on snacks",
    ]

    for p in prompts:
     print(f"\n=== {p} ===")
     robust_tool_call(p)
    
    


if __name__ == "__main__":
    main()
