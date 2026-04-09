# Nom du projet
 
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cet outil permet de charger un fichier de données, d'entraîner un modèle de régression et de générer automatiquement un graphique ainsi qu'un fichier CSV de résultats exploitables.
 
---
 
## 1. Installation & Lancement
 
### Prérequis
- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/en/latest/miniconda.html)
 
### Étapes
 
**1. Cloner le repository**
```bash
git clone https://github.com/votre-repo/nom-du-projet.git
cd nom-du-projet
```
 
**2. Créer l'environnement Python**
```bash
conda create -n nom_env python=3.10
conda activate nom_env
pip install -r requirements.txt
```
 
**3. Lancer le script**
```bash
python run.py
```
 
Le script vous guidera ensuite interactivement dans la console.
 
---
 
## 2. Fonctionnement
 
### a) Préparer ses données
 
Placez votre fichier de données dans le dossier `data/input/` :
 
```
nom-du-projet/
└── data/
    └── input/
        └── votre_fichier.csv   ← ici
```
 
Le fichier peut être au format `.csv` ou `.txt`. Les colonnes doivent correspondre aux paramètres définis dans `config.yaml` (voir section 3).
 
> **Format supporté :** colonnes séparées par des tabulations ou des espaces, avec ou sans header commenté (lignes commençant par `#`).
 
### b) Configurer `config.yaml`
 
Avant de lancer le script, ouvrez `config.yaml` et renseignez les paramètres selon vos besoins. Les paramètres sont détaillés dans la section 3 ci-dessous.
 
### c) Outputs générés
 
Le script génère automatiquement deux fichiers dans le dossier `output/` :
 
| Fichier | Description |
|---|---|
| `results.pdf` | Graphique des résultats |
| `results.csv` | Données brutes pour vos propres analyses |
 
```
nom-du-projet/
└── output/
    ├── results.pdf
    └── results.csv
```
 
---
 
## 3. Paramètres du fichier `config.yaml`
 
```yaml
data_path: "votre_fichier.csv"     # Nom du fichier dans data/input/
Param_names: ["col1", "col2"]      # Colonnes utilisées comme variables d'entrée
Predict_names: ["col3"]            # Colonne à prédire
test_indices: [0, 10]              # Indices des lignes utilisées pour le test
output_csv: "results.csv"          # Nom du fichier CSV de sortie
output_pdf: "results.pdf"          # Nom du fichier PDF de sortie
```
 
| Paramètre | Type | Description |
|---|---|---|
| `data_path` | `string` | Nom du fichier de données dans `data/input/` |
| `Param_names` | `liste` | Noms des colonnes utilisées comme features |
| `Predict_names` | `liste` | Nom de la colonne cible à prédire |
| `test_indices` | `liste [début, fin]` | Intervalle de lignes réservé au test. Si absent, un split aléatoire est utilisé |
| `output_csv` | `string` | Nom du fichier CSV généré dans `output/` |
| `output_pdf` | `string` | Nom du fichier PDF généré dans `output/` |
 
---
 
## 4. Conseils d'utilisation
 
**Vérifier les colonnes reconnues**
Au lancement, le script affiche les colonnes détectées dans votre fichier. Assurez-vous qu'elles correspondent exactement aux noms dans `config.yaml` (sensible à la casse).
 
**En cas de colonne manquante**
Le script affichera un message d'erreur explicite indiquant quelle colonne est introuvable ainsi que la liste des colonnes disponibles.
 
**Choisir ses indices de test**
`test_indices: [0, 10]` réserve les lignes 0 à 9 pour le test. Si vous ne spécifiez pas cet argument, le script effectue un split aléatoire automatiquement.
 
**Réutiliser les données de sortie**
Le fichier `output/results.csv` contient toutes les données nécessaires pour reproduire ou personnaliser le graphique avec l'outil de votre choix (Excel, Python, R...).
 
**Modifier la configuration sans relancer**
Vous pouvez modifier `config.yaml` entre deux lancements sans toucher au code. C'est le seul fichier à éditer pour changer le comportement du script.
 