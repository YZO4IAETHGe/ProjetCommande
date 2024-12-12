# Agent local répondant automatiquement aux mails - Utilisation avec Ollama

## Introduction

> Ce projet démontre l'utilisation du framework **CrewAI** pour automatiser la gestion des mails. CrewAI orchestre des agents d'IA autonomes, leur permettant de collaborer et d'exécuter des tâches complexes de manière efficace. Ce guide explique comment exécuter le script en local en utilisant **Ollama**.

## CrewAI Framework

> CrewAI facilite la collaboration d'agents clés dans la gestion des mails. Dans cet exemple, les agents vont travailler ensemble pour analyser les mails reçus et potentiellement rédiger une réponse tirée d'une base de données.

![Agent sécurité](https://github.com/user-attachments/assets/339ef2ea-26c7-4e46-a5a3-8dd5073f8d8e)

## Prérequis

- **Python** : Version 3.10 à 3.13.
  Vérifiez la version avec la commande :
  ```bash
  python3 --version
- **Ollama** :
   Installez la dernière [version](https://ollama.com/).
   Vérifiez la version :
  ```bash
  ollama version
- **CrewAI** : Installez Crewai
  ```bash
  pip install 'crewai[tools]'

## Configuration
 - Téléchargez un modèle compatible avec Ollama : 
   ```bash
   ollama pull lama2
 - Vérifier que le modèle est bien téléchargé :
    ```bash
    ollama list
 - Configurer l’environnement :
 > Copiez le fichier .env.example
 ```bash
 cp .env.example .env
 ```

> Modifiez les variables dans .env :
 ```bash
 MODEL_API_URL=http://localhost:11434
 MODEL_NAME=llama2
```
## Cloner le dossier git
```bash
git clone <https://github.com/YZO4IAETHGe/ProjetCommande>
```
## Installer les Dépendances
- Installer Poetry
``` bash
pip install poetry
```
- Installer les dépendances du projet  **dans le dossier du projet** :
``` bash
poetry lock && poetry install
```
## Exécuter le Projet en Local
- Lancer Ollama :
``` bash
ollama serve
```
- Lancer le script CrewAI ( Exécutez le script principal avec Poetry ) : 
```bash
poetry run latest_ai_development
```






    

   

  
  
 
  
  





  
