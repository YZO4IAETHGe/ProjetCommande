from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task  
from crewai_tools import PDFSearchTool  # Assuming this tool is needed for document search
from crewai_tools import PDFSearchTool
#from latest_ai_development.tools.custom_tool import PDFReaderTool
#from latest_ai_development.tools.custom_tool import PDFSearchTool

from latest_ai_development.tools.custom_tool import PDFReaderTool
from latest_ai_development.tools.custom_tool import PDFSearchTool
from latest_ai_development.tools.custom_tool import EmailSenderTool

pdf_search_tool = PDFSearchTool()
pdf_reader_tool = PDFReaderTool()
#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
OLLAMA_LLM = LLM(model="ollama/llama3.1", base_url="http://localhost:11434")
OLLAMA_LLM_1b = LLM(model="ollama/llama3.2:1b", base_url="http://localhost:11434")
# Load model directly
#from transformers import AutoTokenizer, AutoModelForCausalLM

#tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3.5-mini-instruct", trust_remote_code=True)
#model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3.5-mini-instruct", trust_remote_code=True)
llm=LLM(model="ollama/qwen2.5:14b",
        base_url="http://localhost:11434")
@CrewBase
class CustomerServiceCrew:
    """Crew for Customer Service Operations"""
    @agent
    def text_analysis_agent(self) -> Agent:
        return Agent(
			#llm=llm,
			config=self.agents_config['text_analysis_agent'], # Example of custom tool, loaded on the beginning of file
			verbose=True
		)

    @agent
    def link_verification_agent(self) -> Agent:
        return Agent(
			#llm=llm,
			config=self.agents_config['link_verification_agent'],
			verbose=True

		)
	
    @agent
    def fraud_probability_calculator_agent(self) -> Agent:
        return Agent(
			#llm=llm,
			config=self.agents_config['fraud_probability_calculator_agent'],
			verbose=True
		)
    @agent
    def email_response_agent(self) -> Agent:
        """Agent for sending the response email to the customer."""
        return Agent(
            #llm=llm,
            config=self.agents_config['email_response_agent'],
            verbose=True
        )


    @agent
    def document_search_agent(self) -> Agent:
        """Agent for retrieving and analyzing documents."""
        return Agent(
            #llm=llm,
            config=self.agents_config['document_search_agent'],
            verbose=True
        )
    
    @agent
    def client_request_filter_agent(self) -> Agent:
        """Agent for filtering SAV mail."""
        return Agent(
            #llm=llm,
            config=self.agents_config['client_request_filter_agent'],
            verbose=True
        )


    @agent
    def client_request_analysis_agent(self) -> Agent:
        """Agent for analyzing customer requests to understand their needs."""
        return Agent(
            #llm=llm,
            config=self.agents_config['client_request_analysis_agent'],
            verbose=True
        )

    @agent
    def response_formulation_agent(self) -> Agent:
        """Agent for formulating and refining responses based on retrieved information."""
        return Agent(
            #llm=llm,
            config=self.agents_config['response_formulation_agent'],
            verbose=True
        )

    @agent
    def quality_assurance_agent(self) -> Agent:
        """Agent for quality control to ensure accuracy and relevance in responses."""
        return Agent(
            #llm=llm,
            config=self.agents_config['quality_assurance_agent'],
            verbose=True
        )

    @agent
    def email_extraction_agent(self) -> Agent:
        """Agent for extracting email addresses from documents."""
        return Agent(
            #llm=llm,
            config=self.agents_config['email_extraction_agent'],
            verbose=True
        )
    
    @task
    def read_task(self) -> Task:
        return Task(
			config=self.tasks_config['read_task'],
			tools=[pdf_reader_tool]
		)
	
    @task
    def weird_expressions_task(self) -> Task:
        return Task(
			config=self.tasks_config['weird_expressions_task'],
			context=[self.read_task()]
			
		)
	
    @task
    def link_verification_task(self) -> Task:
        return Task(
			config=self.tasks_config['link_verification_task'],
			context=[self.read_task()]
			
		)
	
    @task
    def reporting_task(self) -> Task:
        return Task(
			config=self.tasks_config['reporting_task'],
			context=[self.weird_expressions_task(),self.link_verification_task()]
		)


    @task
    def analyze_filter_task(self) -> Task:
        """Task to filter the mail."""
        return Task(
            config=self.tasks_config['filter_request_task'],
            tools=[pdf_reader_tool],
            agent=self.client_request_filter_agent(),
            context=[self.reporting_task()])
    
    @task
    def analyze_request_task(self) -> Task:
        """Task to analyze the customer's query for main issues and keywords."""
        return Task(
            config=self.tasks_config['analyze_request_task'],
            #tools=[pdf_reader_tool],
            agent=self.client_request_analysis_agent(),
            context=[self.analyze_filter_task(),self.read_task()]
        )
    
    @task
    def search_document_task(self) -> Task:
        """Task to search for relevant documents based on keywords and context."""
        return Task(
            config=self.tasks_config['search_document_task'],
            tools=[pdf_reader_tool],
            agent=self.document_search_agent(),
            context=[self.analyze_request_task()]
        )

    @task
    def retrieve_document_content_task(self) -> Task:
        """Task to retrieve specific content from identified documents."""
        return Task(
            config=self.tasks_config['retrieve_document_content_task'],
            tools=[pdf_reader_tool],
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

    @task
    def retrieve_client_email_task(self) -> Task:
        """Task to extract the client's email address from provided documents."""
        return Task(
            config=self.tasks_config['retrieve_client_email_task'],
            tools=[pdf_reader_tool],
            agent=self.email_extraction_agent()
        )

    @task
    def send_email_task(self) -> Task:
        """Task to send the email to the customer."""
        return Task(
            config=self.tasks_config['send_email_task'],
            tools=[EmailSenderTool()],
            agent=self.email_response_agent(),
            context=[self.quality_check_task(), self.retrieve_client_email_task()]
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
