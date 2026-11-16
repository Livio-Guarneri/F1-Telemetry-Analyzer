# F1 Telemetry Analyzer

Application Python utilisant FastF1 pour récupérer et comparer les données de télémétrie de Formula 1.

## Fonctionnalités actuelles

- Sélection d'une saison (1950-2026)
- Sélection d'un Grand Prix
- Sélection d'une session :
  - FP1
  - FP2
  - FP3
  - Qualifications
  - Course
- Sélection d'un ou plusieurs pilotes
- Récupération automatique des données FastF1
- Affichage du graphique de vitesse
- Affichage du graphique du temps au tour
- Comparaison de plusieurs pilotes sur les mêmes graphiques
- Validation des entrées utilisateur

## Technologies utilisées

- Python
- FastF1
- Matplotlib
- NumPy

## Installation

### Cloner le dépôt

```bash
git clone https://github.com/Livio-Guarneri/F1-Telemetry-Analyzer.git
```

### Installer les dépendances

```bash
pip install fastf1 matplotlib numpy
```

### Lancer l'application

```bash
python main.py
```

## Comment utiliser le programme

1. Choisir une saison.
2. Choisir un Grand Prix.
3. Choisir une session.
4. Choisir un ou plusieurs pilotes.
5. Sélectionner le graphique souhaité.
6. Visualiser les résultats.

## Exemple

Le programme permet de comparer plusieurs pilotes lors d'une même séance afin d'analyser :

- leur vitesse sur le circuit ;
- leur temps au tour ;
- leurs performances respectives.

## Améliorations prévues

- Calcul automatique du delta de temps
- Statistiques détaillées
- Export PDF
- Sauvegarde automatique des graphiques
- Interface graphique
- Dashboard interactif
- Analyse avancée des performances

## Objectif du projet

Ce projet a été créé afin d'améliorer mes compétences en :

- développement Python ;
- manipulation de données ;
- visualisation de données ;
- analyse de données sportives.

Il s'inscrit dans un parcours d'apprentissage orienté vers le développement logiciel et le sport automobile.

## Auteur

Projet personnel développé par **Livio Guarneri**.
