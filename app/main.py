import re
from agents.agent import CSVAgent

def extract_python_code(text):
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else None

def run_generated_code(code):
    if code:
        try:
            print("🔧 Executing generated code...\n")
            exec(code, globals())
        except Exception as e:
            print(f"❌ Execution failed: {e}")
    else:
        print("⚠️ No Python code block found in agent response.")

if __name__ == "__main__":
    csv_agent = CSVAgent()
    # file_path = "./data.csv"
    file_path = "./support_tickets_data.csv"

    # plot_options = ["histogram", "scatter plot", "line plot", "bar chart", "heatmap"]
    # print("📊 Available plot types:", ", ".join(plot_options))

    # chosen_plot = input("🤔 Choose a plot type from the above options: "
    #                     ).strip().lower()
    # if chosen_plot not in plot_options:
    #     print(f"❌ Invalid choice. Please choose from {', '.join(plot_options)}.")
    #     exit(1)
    
    
    
    results = csv_agent.crew(file_path=file_path, chosen_plot="").kickoff()

    final_output = results.final_output if hasattr(results, "final_output") else str(results)
    code = extract_python_code(final_output)
    print("\n📄 Generated Python Code:\n", code)
    run_generated_code(code)
