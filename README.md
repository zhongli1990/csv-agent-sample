# CSV Agent

Check this out in [Medium Article](https://medium.com/@wriddhirupd/csv-agent-using-mcp-with-langgraph-and-llama3-2-26652717db31)

## About the Agent
The CSV agent in this project acts as a Data Analyst that can read, describe and visualize based on the user input. Its a conversational agent that can store the older messages in its memory.

<img width="716" alt="image" src="https://github.com/user-attachments/assets/446240a1-e6bf-4574-b87e-d15cdbd80090" />


## Prerequisites for the setup:
- Install Ollama - https://ollama.com/download
- Install Python 3.12 - https://www.python.org/downloads/release/python-3120/

For this agent, we are using `Llama3.2:latest` from Ollama and connecting it through LangChain library.

## Install dependencies:
```
pip install -r requirements.txt
```

## Run:
```
python app/main.py
```
OR 
```
uv run app/main.py
```

## Results:

1. User ask: For /Users/{user}/Downloads/excel-agent-main/data.csv draw a line chart of income

    ```bash
    % uv run app/main.py
    Enter your command for the CSV Agent (type 'exit' to exit the agent): 
    > For /Users/{user}/Downloads/excel-agent-main/data.csv draw a line chart of income
    Intent: Based on the user's command, I would determine that the intent is "visualize". The mention of drawing a line chart and referencing a specific CSV file suggests that the user wants to visualize data from the CSV file.
    [05/16/25 14:41:42] INFO     Processing request of type ListToolsRequest                                                                                                                                     server.py:545
                        INFO     Processing request of type GetPromptRequest                                                                                                                                     server.py:545
    Prompt: 
           **System**: You are a data visualization assistant. Your task is to generate Python scripts wrapped in ```python...``` that visualize data using matplotlib and pandas.
    
            Visualize the csv file with matplotlib based on the plot type specified.
            Load the csv file from the filepath specified in the user message and use the data to create a plot.
            The needed libraries are already part of the running environment, so you don't need to install them.
    
            Always import the necessary libraries at the top:
                ```python
                import matplotlib.pyplot as plt
                import pandas as pd
                ```
    
            **User**: For /Users/{user}/Downloads/excel-agent-main/data.csv draw a line chart of income
        
    [05/16/25 14:41:44] INFO     Processing request of type CallToolRequest                                                                                                                                      server.py:545
    Extracted Python code... 
     import matplotlib.pyplot as plt
    import pandas as pd
    
    # Load the csv file from the filepath specified in the user message
    df = pd.read_csv('/Users/{user}/Downloads/excel-agent-main/data.csv')
    
    # Filter the data for 'income' column
    filtered_df = df[df['income'] != '']
    
    # Create a line chart of income
    plt.figure(figsize=(10,6))
    plt.plot(filtered_df['income'], marker='o')
    plt.title('Line Chart of Income')
    plt.xlabel('Income')
    plt.ylabel('Value')
    plt.show()
    agent_message:  ```python
    import matplotlib.pyplot as plt
    import pandas as pd
    
    # Load the csv file from the filepath specified in the user message
    df = pd.read_csv('/Users/{user}/Downloads/excel-agent-main/data.csv')
    
    # Filter the data for 'income' column
    filtered_df = df[df['income'] != '']
    
    # Create a line chart of income
    plt.figure(figsize=(10,6))
    plt.plot(filtered_df['income'], marker='o')
    plt.title('Line Chart of Income')
    plt.xlabel('Income')
    plt.ylabel('Value')
    plt.show()
    ```
    ![image](https://github.com/user-attachments/assets/e0994a98-db1f-4861-9b1f-620b8ae52c75)

2. User ask: Give some insights on /Users/{user}/Downloads/excel-agent-main/data.csv

   ```
    Enter your command for the CSV Agent (type 'exit' to exit the agent): 
    > Give some insights on /Users/{user}/Downloads/excel-agent-main/data.csv
    Intent: Based on the user's command, I would determine that the intent is "describe". The mention of analyzing a specific CSV file suggests that the user wants to gain insights into its contents.
    [05/16/25 14:45:42] INFO     Processing request of type ListToolsRequest                                                                                                                                     server.py:545
    Prompt: 
    [05/16/25 14:45:43] INFO     Processing request of type CallToolRequest                                                                                                                                      server.py:545
    agent_message:  The data.csv file contains information about three different variables: age, income, and score.
    
    Here are some key insights from the data:
    
    1. **Age Distribution**: The ages range from 20 to 60, with a mean of 39.94 years old. This suggests that the dataset is likely representing adults or young adults.
    2. **Income Range**: The incomes vary widely, ranging from $41,874 to $117,919. The mean income is approximately $77,847.
    3. **Score Distribution**: The scores range from 62 to 99, with a mean of 81.58 and a standard deviation of 9.98. This suggests that the scores are likely representing some kind of assessment or evaluation.
    
    Overall, the data appears to be diverse and representative of different aspects of an individual's life. However, without more context, it is difficult to draw any further conclusions about the specific characteristics       or behaviors represented in the dataset.
    None
    Enter your command for the CSV Agent (type 'exit' to exit the agent): 
    >
   ```

