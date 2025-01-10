# Agent local répondant automatiquement aux mails - Utilisation avec Ollama (en local) ou GPT 

## Introduction

> Ce projet démontre l'utilisation du framework **CrewAI** pour automatiser la gestion des mails. CrewAI orchestre des agents d'IA autonomes, leur permettant de collaborer et d'exécuter des tâches complexes de manière efficace. Ce guide explique comment exécuter le script en local en utilisant **Ollama**.

## CrewAI Framework

> CrewAI facilite la collaboration d'agents clés dans la gestion des mails. Dans cet exemple, les agents vont travailler ensemble pour analyser les mails reçus et potentiellement rédiger une réponse tirée d'une base de données.

![Agent sécurité](https://github.com/user-attachments/assets/339ef2ea-26c7-4e46-a5a3-8dd5073f8d8e)

## Prérequis
- **Exécution des commandes sous Windows** : Ouvrir une invite de commandes ou PowerShell

- **Python** : Installez Python
1. Rendez-vous sur le (site officiel de Python)[https://www.python.org/downloads/].
2. Téléchargez la version recommandée pour votre système d’exploitation.
3. Assurez-vous de cocher la case "Add Python to PATH" lors de l’installation sous Windows.
4. Version 3.10 à 3.13Vérifiez la version de python est entre 3.10 à 3.13 :
  ```bash
  python3 --version
```
- **Ollama** :
   Installez la dernière [version](https://ollama.com/).
   Vérifiez la version :
  ```bash
  ollama version
  ```
  Ajouter le chemin d'Ollama au PATH
- **CrewAI** : Installez Crewai
1. Ouvrir une Invite de commandes ou PowerShell (sur Windows)
  ```bash
  pip install crewai[tools]
```

## Configuration
 - Téléchargez un modèle compatible avec Ollama : 
   ```bash
   ollama pull llama3
 - Vérifier que le modèle est bien téléchargé :
    ```bash
    ollama list
  ## Cloner le dossier git
```bash
git clone https://github.com/YZO4IAETHGe/ProjetCommande
```
 - Récupérer une clé API OpenAI:
1. Connectez-vous sur la [page OpenAI](https://platform.openai.com/docs/overview)
2. Allez dans la section **API Keys**
3. Cliquez sur **Créer une nouvelle clé secrète**  
 - Configurer l’environnement :
 ```
> Ajouter une clé API pour OPENAI dans .env :
 OPENAI_API_KEY=clé
```
- Lancer le script CrewAI (dans le dossier AgentAnalyste): 
```bash
crewai update (la première fois)
crewai run 
```






    

   

  
  
 
  
  





  
