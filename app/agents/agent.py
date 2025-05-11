from textwrap import dedent
from crewai import Agent, LLM, Crew, Process, Task
from crewai_tools import FileReadTool

from app.constants import LLM_NAME, BASE_URL, TEMPERATURE

llm = LLM(
    model=LLM_NAME, 
    base_url=BASE_URL, 
    temperature=TEMPERATURE
    ) 

class CSVAgent:
    def reader_agent(self, file_path) -> Agent:
        """
        Create a reader agent for reading CSV files.
        """
        return Agent(
            role="CSV Reader",
            goal="Read and summarize the CSV structure",
            backstory=("An expert in understanding datasets and identifying their purpose, "
                "You have a deep understanding of data science and Machine learning and data analysis"),
            verbose=True,
            tools=[FileReadTool(file_path=file_path)],
            # allow_delegation=True,
            llm=llm
        )
    
    def analyst_agent(self) -> Agent:
        """
        Create an analyst agent for analyzing CSV files.
        """
        return Agent(
            role="Data Analyst",
            goal="Extract insights from the dataset and suggest visualizations.",
            backstory="You specialize in statistics and pattern recognition.",
            verbose=True,
            llm=llm,
            allow_delegation=True,
        )
    
    def visualization_agent(self) -> Agent:
        """
        Create a visualization agent for visualizing CSV files.
        """
        return Agent(
            role="Data Visualization Expert",
            goal=(
                "Generate meaningful visualizations such as histograms, scatter plots, line plots, bar charts, "
                "and heatmaps to provide insights into the data."
            ),        
            backstory="You use matplotlib/seaborn to create graphs.",
            verbose=True,
            llm=llm
        )
    
    def read_csv_task(self, file_path):
        return Task(
        description=dedent(f"""
            Load the CSV file '{file_path}'.
            Summarize it: number of rows, columns, column names, and types. Read the column names correctly from the CSV file.
        """),
        expected_output="A short summary of the dataset's structure, including column names and data types.",
        agent=self.reader_agent(file_path=file_path),
    )

    def analyze_csv_task(self, file_path):
        return Task(
            description=dedent(f"""
                Analyze the dataset loaded from '{file_path}'.
                
                You already have a summary of the file structure from the CSV Reader agent.

                Based on the actual data:
                - Provide descriptive statistics for all numeric columns.
                - Point out correlations or patterns you notice.
                - Suggest 3-5 chart types that would be **most useful to visualize this specific dataset**.
                Use the actual column names in your suggestions.
                Examples: "Scatter plot of Age vs. Income", "Bar chart of Gender distribution"

                Format your output in markdown.
            """),
            expected_output=dedent("""
                1. Statistical summary of numeric columns
                2. Observed trends or correlations
                3. List of recommended visualizations using real column names (e.g., 'Scatter plot of Salary vs. Experience')
            """),
            context=[self.read_csv_task(file_path)],
            agent=self.analyst_agent(),
            # human_input=True
        )
    
    def visualize_csv_task(self, file_path):
        # plots = ', '.join(graph_types)
        return Task(
            description=dedent(f"""
                Based on the analysis, write Python code using matplotlib/seaborn to create plots for the file {file_path} based on the human input by analyst_agent:
                - The output must be inside a ```python ... ``` block.
                - Show the plots only for the columns mentioned in {file_path}.
                - Include `plt.show()` to render the plots
            """),
            expected_output="Python code wrapped in triple backticks for visualization",
            context=[self.read_csv_task(file_path), self.analyze_csv_task(file_path)],
            agent=self.visualization_agent(),
        )
    
    def crew(self, file_path, chosen_plot) -> Crew:
        return Crew(
            name="CSV Analysis Crew",
            description="A crew of agents specialized in reading, analyzing, and visualizing CSV files.",
            agents=[
                self.reader_agent(file_path),
                self.analyst_agent(),
                self.visualization_agent()
            ],
            tasks=[
                self.read_csv_task(file_path),
                self.analyze_csv_task(file_path),
                self.visualize_csv_task(file_path)
            ],
            llm=llm,
            process=Process.sequential,
            # verbose=True,
            # planning=True,
            # planning_llm=llm,
        )
