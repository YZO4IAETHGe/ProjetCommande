import os
import pickle
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from agentsecre.tools.custom_tool import PDFReaderTool

tool = PDFReaderTool()

# Les portées nécessaires pour interagir avec le calendrier Google
SCOPES = ['https://www.googleapis.com/auth/calendar']


@CrewBase
class EmailToCalendarCrew():
    """Email to Calendar Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @before_kickoff  # Optional hook to be executed before the crew starts
    def pull_data_example(self, inputs):
        # Example of pulling data from an external API, dynamically changing the inputs
        inputs['extra_data'] = "This is extra data"
        return inputs

    @after_kickoff  # Optional hook to be executed after the crew has finished
    def log_results(self, output):
        # Example of logging results, dynamically changing the output
        print(f"Results: {output}")
        return output

    @agent
    def email_parser_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['email_parser_agent'],
            verbose=True
        )

    @agent
    def event_conflict_checker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['event_conflict_checker_agent'],
            verbose=True
        )

    @agent
    def calendar_event_scheduler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['calendar_event_scheduler_agent'],
            verbose=True
        )

    @agent
    def notification_sender_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['notification_sender_agent'],
            verbose=True
        )

    @task
    def read_task(self) -> Task:
        return Task(
            config=self.tasks_config['read_task'],
            tools=[tool]
        )

    @task
    def email_parsing_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_parsing_task'],
            context=[self.read_task()]
        )

    @task
    def event_conflict_checking_task(self) -> Task:
        def check_conflicts(context):
            event_details = context['email_parsing_task']
            url = "https://www.googleapis.com/calendar/v3/calendars/primary/events"
            headers = {
                "Authorization": "Bearer YOUR_ACCESS_TOKEN",
                "Content-Type": "application/json"
            }

            # Check for conflicts
            check_url = f"{url}?timeMin={event_details['date']}T{event_details['time']}:00Z&timeMax={event_details['date']}T{event_details['time']}:59Z"
            check_response = requests.get(check_url, headers=headers)
            if check_response.status_code != 200:
                return {
                    "error": "Failed to check for conflicts"
                }

            events = check_response.json().get('items', [])
            if events:
                # Suggest alternative times
                alternative_times = []
                for i in range(1, 5):
                    alternative_times.append(f"{int(event_details['time'][:2]) + i:02d}:{event_details['time'][3:]}")
                return {
                    "conflict_status": "Conflict found",
                    "alternative_times": alternative_times
                }
            else:
                return {
                    "conflict_status": "No conflict"
                }

        return Task(
            config=self.tasks_config['event_conflict_checking_task'],
            context=[self.email_parsing_task()],
            action=check_conflicts
        )

    @task
    def event_scheduling_task(self) -> Task:
        def schedule_event(context):
            event_details = context['email_parsing_task']
            conflict_check = context['event_conflict_checking_task']

            if conflict_check['conflict_status'] == "Conflict found":
                return {
                    "error": "Conflict found with existing events",
                    "alternative_times": conflict_check['alternative_times']
                }

            # Authentification pour obtenir un jeton d'accès
            creds = None
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)

            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)

                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            # Appel à l'API Google Calendar pour ajouter l'événement
            service = build('calendar', 'v3', credentials=creds)

            event = {
                'summary': event_details['event_title'],
                'location': event_details['location'],
                'description': event_details['description'],
                'start': {
                    'dateTime': f"{event_details['date']}T{event_details['time']}:00",
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': f"{event_details['date']}T{event_details['time']}:00",
                    'timeZone': 'UTC',
                },
                'attendees': [{'email': email} for email in event_details['participants']],
            }

            event = service.events().insert(calendarId='primary', body=event).execute()

            print(f'Event created: {event.get("htmlLink")}')
            return {
                "event_id": event['id'],
                "confirmation_message": "Event successfully scheduled"
            }

        return Task(
            config=self.tasks_config['event_scheduling_task'],
            context=[self.email_parsing_task(), self.event_conflict_checking_task()],
            action=schedule_event
        )

    @task
    def notification_sending_task(self) -> Task:
        return Task(
            config=self.tasks_config['notification_sending_task'],
            context=[self.event_scheduling_task()]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EmailToCalendar crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
