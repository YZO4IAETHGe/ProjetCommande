#!/usr/bin/env python
import sys
from latest_ai_development.crew import CustomerServiceCrew
import tkinter as tk
from tkinter import filedialog

# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    root = tk.Tk()
    root.withdraw() 

    file_path = filedialog.askopenfilename(title="Sélectionnez un mail")
    root = tk.Tk()
    root.withdraw() 

    sol_path = filedialog.askopenfilename(title="Sélectionnez le fichier des solutions")
    inputs = {
        'pdf_path': file_path,
        'solution_path' : sol_path
    }
    CustomerServiceCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CustomerServiceCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CustomerServiceCrew().crew().replay(task_id=sys.argv[1])

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
        CustomerServiceCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
