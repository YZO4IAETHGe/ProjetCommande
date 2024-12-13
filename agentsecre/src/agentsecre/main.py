#!/usr/bin/env python
import sys
import warnings
from tkinter import filedialog

from agentsecre.crew import EmailToCalendarCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    file_path = filedialog.askopenfilename(title="Selectionnez un fichier")
    # Exemple d'input personnalisé
    inputs = {
        'email_content': 'The email body content goes here',  # Exemple de contenu d'email à analyser
        'calendar_id': 'primary',  # ID du calendrier à utiliser pour la planification
        'pdf_path': file_path,  # Chemin du fichier PDF à lire
    }

    # Demarre l'execution du crew avec les entrées personnalisees
    EmailToCalendarCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Agentsecre().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Agentsecre().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Agentsecre().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
