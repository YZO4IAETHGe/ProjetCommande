# Agent local répondant automatiquement aux mails - Utilisation avec Ollama (en local) ou GPT 

## Introduction

> Ce projet démontre l'utilisation du framework **CrewAI** pour automatiser la gestion des mails. CrewAI orchestre des agents d'IA autonomes, leur permettant de collaborer et d'exécuter des tâches complexes de manière efficace. Ce guide explique comment exécuter le script en local en utilisant **Ollama**.

## CrewAI Framework

> CrewAI facilite la collaboration d'agents clés dans la gestion des mails. Dans cet exemple, les agents vont travailler ensemble pour analyser les mails reçus et potentiellement rédiger une réponse tirée d'une base de données.


![Agent sécurité](https://github.com/user-attachments/assets/5893a013-816f-41b6-8f5e-f21dec4df30e)


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
- **Ollama** : Télécharger Ollama
1. Installez la dernière [version](https://ollama.com/).
2. Vérifiez la version :
  ```bash
  ollama version
  ```
3. Téléchargez un modèle compatible avec Ollama : 
   ```bash
   ollama pull llama3
   ```
4. Vérifier que le modèle est bien téléchargé :
    ```bash
    ollama list
    ```
5. Ajouter le chemin d'Ollama au PATH
- **CrewAI** : Installez Crewai
1. Ouvrir une Invite de commandes ou PowerShell (sur Windows)
  ```bash
  pip install crewai[tools]
```
2. Vérifier l'installation de crewAI
```bash
pip show crewai
```

## Utilisation du crew avec Ollama ou GPT 
> Le code est par défault écrit de sorte à fonctionnner avec ChatGPT, il faut pour cela rajouter une clé API dans le dossier .env (étape détaillée dans la prochaine partie). Le code est cependant théoriquement éxectuable de manière locale avec un modèle de Ollama comme llama3 si la puissance de calcul de votre machine est assez élevée. 

> Pour cela il faut décommenter l'ensemble des "llm" compris dans le script de chaque agent 
## Cloner et éxecuter  le dossier git
```bash
git clone https://github.com/YZO4IAETHGe/ProjetCommande
```
 - Récupérer une clé API OpenAI:
1. Connectez-vous sur la [page OpenAI](https://platform.openai.com/docs/overview)
2. Allez dans la section **API Keys**
3. Cliquez sur **Créer une nouvelle clé secrète**  
 - Configurer l’environnement :
> Ajouter une clé API pour OPENAI dans .env :
```
 OPENAI_API_KEY=clé
```
 - Alimenter la clé :
> L’utilisation de l’API ChatGPT et des clés API n’est pas gratuite. Vous payez un montant défini en fonction du nombre de mots générés par ChatGPT via l’API
 1. Allez dans Dashboard/Usage/Cost en cliquant [ici](https://platform.openai.com/settings/organization/usage)
 2. Les nouveaux utilisateurs doivent payer un capital initial d’environ 5 dollars grâce auquel ils pourront tester l’API. Pour obtenir ce capital, cliquer sur augmenter la limite
> Environ 750 mots correspondent à 1 000 jetons.
Avec GPT-4, 1 000 jetons coûtent environ 0,03 à 0,12 dollar américain (environ 3 à 12 centimes d’euro).
**Afin d’éviter des frais incontrôlables, il est possible de définir un plafond maximal du montant.**

- Lancer le script CrewAI (dans le dossier AgentAnalyste): 
1. Commande en cas de première utilisation
```bash
crewai update
```
2. Exécution du script
```
crewai run
```
- Inputs pour obtenir une réponse
1. Le programme contient une base de donnée ici sur les radiateurs (au format PDF). Cette base de donnée est modifiable et doit correspondre aux types des mails qui vont être traités par l'équipe d'agents
2. Par la suite, l'équipe d'agents va demander un mail auquel répondre (format PDF et **contenant l'adresse mail de l'expéditeur**), c'est ainsi que le mail rédigé par l'équipe sera envoyé au bon destinataire. 
## Problèmes possibles 
Date 10/01/2024 : Problème avec la dépendance uvloop
Correction : 
```
pip install litellm==1.57.4
```
```
pip install crewai --no-deps
```
```
pip install crewai[tools] --no-binary==uvloop
```






    

   

  
  
 
  
  





  
