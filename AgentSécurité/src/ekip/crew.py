from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai import LLM  


# Uncomment the following line to use an example of a custom tool
from ekip.tools.custom_tool import PDFReaderTool

# Check our tools documentations for more information on how to use them
from crewai_tools import PDFSearchTool
tool = PDFReaderTool() #commentraire thomas

#Si chatgpt mettre en commentaire la ligne suivante et toute les ligne "llm" et ajouter la clé api dans le .env
#llm=LLM(model="ollama/llama3.1", base_url="http://localhost:11434")


@CrewBase
class EkipCrew():
	"""Ekip crew"""

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

	@task
	def read_task(self) -> Task:
		return Task(
			config=self.tasks_config['read_task'],
			tools=[tool]
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
	
	

	@crew
	def crew(self) -> Crew:
		"""Creates the Ekip crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)