from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task  
from crewai_tools import PDFSearchTool  # Assuming this tool is needed for document search
from crewai_tools import PDFSearchTool
#from latest_ai_development.tools.custom_tool import PDFReaderTool
#from latest_ai_development.tools.custom_tool import PDFSearchTool

from latest_ai_development.tools.custom_tool import PDFReaderTool
from latest_ai_development.tools.custom_tool import PDFSearchTool

pdf_search_tool = PDFSearchTool()
pdf_reader_tool = PDFReaderTool()

@CrewBase
class CustomerServiceCrew:
    """Crew for Customer Service Operations"""

    @agent
    def document_search_agent(self) -> Agent:
        """Agent for retrieving and analyzing documents."""
        return Agent(
            #llm=LLM(model="ollama/llama3.1", base_url="http://localhost:11434"),
            config=self.agents_config['document_search_agent'],
            verbose=True
        )

    @agent
    def client_request_analysis_agent(self) -> Agent:
        """Agent for analyzing customer requests to understand their needs."""
        return Agent(
            #llm=LLM(model="ollama/llama3.1", base_url="http://localhost:11434"),
            config=self.agents_config['client_request_analysis_agent'],
            verbose=True
        )

    @agent
    def response_formulation_agent(self) -> Agent:
        """Agent for formulating and refining responses based on retrieved information."""
        return Agent(
            #llm=LLM(model="ollama/llama3.1", base_url="http://localhost:11434"),
            config=self.agents_config['response_formulation_agent'],
            verbose=True
        )

    @agent
    def quality_assurance_agent(self) -> Agent:
        """Agent for quality control to ensure accuracy and relevance in responses."""
        return Agent(
            #llm=LLM(model="ollama/llama3.1", base_url="http://localhost:11434"),
            config=self.agents_config['quality_assurance_agent'],
            verbose=True
        )

    @task
    def analyze_request_task(self) -> Task:
        """Task to analyze the customer's query for main issues and keywords."""
        return Task(
            config=self.tasks_config['analyze_request_task'],
            tools=[],
            agent=self.client_request_analysis_agent()
        )

    @task
    def search_document_task(self) -> Task:
        """Task to search for relevant documents based on keywords and context."""
        return Task(
            config=self.tasks_config['search_document_task'],
            tools=[pdf_search_tool],
            agent=self.document_search_agent(),
            context=[self.analyze_request_task()]
        )

    @task
    def retrieve_document_content_task(self) -> Task:
        """Task to retrieve specific content from identified documents."""
        return Task(
            config=self.tasks_config['retrieve_document_content_task'],
            tools=[pdf_search_tool],
            agent=self.document_search_agent(),
            context=[self.search_document_task()]
        )

    @task
    def formulate_response_task(self) -> Task:
        """Task to draft a response based on extracted document content."""
        return Task(
            config=self.tasks_config['formulate_response_task'],
            agent=self.response_formulation_agent(),
            context=[self.retrieve_document_content_task()]
        )

    @task
    def quality_check_task(self) -> Task:
        """Task to review the response for accuracy and relevance."""
        return Task(
            config=self.tasks_config['quality_check_task'],
            agent=self.quality_assurance_agent(),
            context=[self.formulate_response_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Customer Service Crew for handling support requests."""
        return Crew(
            agents=self.agents,  # Agents are defined by @agent decorators
            tasks=self.tasks,  # Tasks are defined by @task decorators
            process=Process.sequential,  # Executes tasks in a sequential order
            verbose=True,
        )
